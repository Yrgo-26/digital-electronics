/**
 * @brief Run an assembled ATmega328P program in simavr and print the machine state.
 *
 * This is the instrument behind `make test`. It loads an Intel hex file written by avra,
 * runs it for a number of cycles (or until a label is reached), and prints the registers,
 * SREG, the stack pointer and the I/O registers as `key=value` lines. It knows nothing about
 * what the program was supposed to do: ci/simtest.py compares the output against the
 * `; @expect` lines in the source.
 *
 * Usage:
 *   simcheck <program.hex> [options]
 *
 * Options:
 *   --cycles N              Run for at most N cycles (default 1000000).
 *   --until LABEL           Stop the first time the program counter reaches LABEL.
 *   --between A B           Report the cycles from the first arrival at A to the next arrival
 *                           at B, as `between=N`.
 *   --pin P=L               Drive pin P (e.g. D2) to level L (0 or 1) before the first cycle.
 *   --event C:P=L           Drive pin P to level L once C cycles have elapsed.
 *   --watch P               Record every change of output pin P, as `watch P=L@cycle` lines.
 *   --clock HZ              Clock frequency in Hz (default 16000000). Only affects reports.
 *
 * Labels are read from the avra map file sharing the hex file's stem (program.map).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <simavr/avr_ioport.h>
#include <simavr/sim_avr.h>
#include <simavr/sim_hex.h>

/** Maximum number of labels, pin drives, events and watched pins. */
#define MAX_LABELS 512U
#define MAX_PINS 32U
#define MAX_EVENTS 64U
#define MAX_WATCH 16U
#define MAX_LOG 4096U

/** Data space address of SREG and the stack pointer. */
#define SREG_ADDR 0x5FU
#define SPL_ADDR 0x5DU
#define SPH_ADDR 0x5EU

/** One label from the map file: its name and its byte address in flash. */
typedef struct
{
    char name[64];
    uint32_t address;
} label_t;

/** One pin level: which port, which bit, which level, and when (for events). */
typedef struct
{
    char port;
    uint8_t bit;
    uint8_t level;
    uint64_t cycle;
    int done;
} pin_t;

/** One recorded pin change. */
typedef struct
{
    char port;
    uint8_t bit;
    uint8_t level;
    uint64_t cycle;
} change_t;

static label_t labels[MAX_LABELS];
static size_t labelCount = 0U;
static change_t changes[MAX_LOG];
static size_t changeCount = 0U;
static avr_t* avr = NULL;

/**
 * @brief Report a fatal error and exit.
 */
static void fail(const char* message, const char* detail)
{
    fprintf(stderr, "simcheck: %s%s%s\n", message, detail ? ": " : "", detail ? detail : "");
    exit(2);
}

/**
 * @brief Silence simavr's own logging; the output of this tool is parsed by a script.
 */
static void quiet(avr_t* core, const int level, const char* format, va_list args)
{
    (void)core;
    if (level <= LOG_ERROR) { vfprintf(stderr, format, args); }
}

/**
 * @brief Read the labels (type L) from the avra map file beside the hex file.
 *
 * avra writes one line per symbol: name, type, word address in hex, and the value in decimal.
 * Only L rows are labels; the device file contributes thousands of C rows (constants).
 */
static void readLabels(const char* hexPath)
{
    char mapPath[1024];
    const char* dot = strrchr(hexPath, '.');
    const size_t stem = dot ? (size_t)(dot - hexPath) : strlen(hexPath);
    if (stem + 5U >= sizeof(mapPath)) { fail("path too long", hexPath); }
    memcpy(mapPath, hexPath, stem);
    strcpy(mapPath + stem, ".map");

    FILE* map = fopen(mapPath, "r");
    if (!map) { return; } /* Labels are optional; --until and --between will report it. */

    char line[256];
    while (fgets(line, sizeof(line), map) && labelCount < MAX_LABELS)
    {
        char name[64], type[8];
        unsigned int word;
        if (3 == sscanf(line, "%63s %7s %x", name, type, &word) && 0 == strcmp(type, "L"))
        {
            strcpy(labels[labelCount].name, name);
            labels[labelCount].address = word * 2U; /* Words in the map, bytes in simavr. */
            labelCount++;
        }
    }
    fclose(map);
}

/**
 * @brief Look up a label's byte address, or exit if it does not exist.
 */
static uint32_t labelAddress(const char* name)
{
    for (size_t i = 0U; i < labelCount; ++i)
    {
        if (0 == strcasecmp(labels[i].name, name)) { return labels[i].address; }
    }
    fail("no such label in the map file", name);
    return 0U;
}

/**
 * @brief Parse a pin name such as "D2" into a port letter and a bit number.
 */
static void parsePin(const char* text, char* port, uint8_t* bit)
{
    if (strlen(text) < 2U || text[0] < 'B' || text[0] > 'D' || text[1] < '0' || text[1] > '7')
    {
        fail("pin must be written as B0-B7, C0-C7 or D0-D7", text);
    }
    *port = text[0];
    *bit = (uint8_t)(text[1] - '0');
}

/**
 * @brief Parse "P=L" (a pin and a level) into a pin_t.
 */
static pin_t parseLevel(const char* text)
{
    pin_t pin = {0};
    const char* equals = strchr(text, '=');
    if (!equals || (equals[1] != '0' && equals[1] != '1')) { fail("expected PIN=0|1", text); }
    parsePin(text, &pin.port, &pin.bit);
    pin.level = (uint8_t)(equals[1] - '0');
    return pin;
}

/**
 * @brief Drive an input pin from outside the chip.
 */
static void drive(const pin_t* pin)
{
    avr_irq_t* irq = avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ(pin->port), pin->bit);
    if (irq) { avr_raise_irq(irq, pin->level); }
}

/**
 * @brief Record a change of a watched output pin, with the cycle it happened on.
 */
static void onChange(avr_irq_t* irq, uint32_t value, void* param)
{
    (void)irq;
    const pin_t* pin = (const pin_t*)param;
    if (changeCount < MAX_LOG)
    {
        changes[changeCount].port = pin->port;
        changes[changeCount].bit = pin->bit;
        changes[changeCount].level = value ? 1U : 0U;
        changes[changeCount].cycle = avr->cycle;
        changeCount++;
    }
}

/**
 * @brief Pack simavr's one-byte-per-flag SREG into the device's layout.
 */
static uint8_t sreg(void)
{
    uint8_t packed = 0U;
    for (uint8_t bit = 0U; bit < 8U; ++bit)
    {
        if (avr->sreg[bit]) { packed |= (uint8_t)(1U << bit); }
    }
    return packed;
}

int main(int argc, char** argv)
{
    if (argc < 2) { fail("usage: simcheck <program.hex> [options]", NULL); }

    const char* hexPath = argv[1];
    uint64_t maxCycles = 1000000U;
    uint32_t clockHz = 16000000U;
    const char* until = NULL;
    const char* betweenA = NULL;
    const char* betweenB = NULL;
    pin_t pins[MAX_PINS];
    size_t pinCount = 0U;
    pin_t events[MAX_EVENTS];
    size_t eventCount = 0U;
    pin_t watched[MAX_WATCH];
    size_t watchCount = 0U;

    for (int i = 2; i < argc; ++i)
    {
        if (0 == strcmp(argv[i], "--cycles") && i + 1 < argc)
        {
            maxCycles = strtoull(argv[++i], NULL, 0);
        }
        else if (0 == strcmp(argv[i], "--clock") && i + 1 < argc)
        {
            clockHz = (uint32_t)strtoul(argv[++i], NULL, 0);
        }
        else if (0 == strcmp(argv[i], "--until") && i + 1 < argc) { until = argv[++i]; }
        else if (0 == strcmp(argv[i], "--between") && i + 2 < argc)
        {
            betweenA = argv[++i];
            betweenB = argv[++i];
        }
        else if (0 == strcmp(argv[i], "--pin") && i + 1 < argc && pinCount < MAX_PINS)
        {
            pins[pinCount++] = parseLevel(argv[++i]);
        }
        else if (0 == strcmp(argv[i], "--event") && i + 1 < argc && eventCount < MAX_EVENTS)
        {
            const char* text = argv[++i];
            const char* colon = strchr(text, ':');
            if (!colon) { fail("expected CYCLE:PIN=0|1", text); }
            events[eventCount] = parseLevel(colon + 1);
            events[eventCount].cycle = strtoull(text, NULL, 0);
            events[eventCount].done = 0;
            eventCount++;
        }
        else if (0 == strcmp(argv[i], "--watch") && i + 1 < argc && watchCount < MAX_WATCH)
        {
            parsePin(argv[++i], &watched[watchCount].port, &watched[watchCount].bit);
            watchCount++;
        }
        else { fail("unknown or incomplete option", argv[i]); }
    }

    avr_global_logger_set(quiet);
    avr = avr_make_mcu_by_name("atmega328p");
    if (!avr) { fail("simavr does not know the atmega328p", NULL); }
    avr_init(avr);
    avr->frequency = clockHz;

    /* Chunks rather than one blob: a program with .org directives is not contiguous. */
    ihex_chunk_p chunks = NULL;
    const int count = read_ihex_chunks(hexPath, &chunks);
    if (count <= 0) { fail("cannot read hex file", hexPath); }
    uint32_t codeEnd = 0U;
    for (int i = 0; i < count; ++i)
    {
        if (chunks[i].baseaddr + chunks[i].size > avr->flashend + 1U)
        {
            fail("program does not fit in flash", hexPath);
        }
        memcpy(&avr->flash[chunks[i].baseaddr], chunks[i].data, chunks[i].size);
        if (chunks[i].baseaddr + chunks[i].size > codeEnd)
        {
            codeEnd = chunks[i].baseaddr + chunks[i].size;
        }
    }
    free_ihex_chunks(chunks);
    avr->codeend = codeEnd;
    readLabels(hexPath);

    for (size_t i = 0U; i < pinCount; ++i) { drive(&pins[i]); }
    for (size_t i = 0U; i < watchCount; ++i)
    {
        avr_irq_t* irq =
            avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ(watched[i].port), watched[i].bit);
        if (irq) { avr_irq_register_notify(irq, onChange, &watched[i]); }
    }

    const uint32_t untilAddress = until ? labelAddress(until) : 0xFFFFFFFFU;
    const uint32_t addressA = betweenA ? labelAddress(betweenA) : 0xFFFFFFFFU;
    const uint32_t addressB = betweenB ? labelAddress(betweenB) : 0xFFFFFFFFU;
    int reachedUntil = 0;
    int seenA = 0;
    int64_t between = -1;
    uint64_t cycleA = 0U;

    /* Bounded by instructions as well as by cycles, so a core that stops counting cycles
     * (a crash, a sleep with nothing to wake it) cannot keep this loop running for ever. */
    uint64_t executed = 0U;
    while (avr->cycle < maxCycles && executed < maxCycles * 2U)
    {
        for (size_t i = 0U; i < eventCount; ++i)
        {
            if (!events[i].done && avr->cycle >= events[i].cycle)
            {
                drive(&events[i]);
                events[i].done = 1;
            }
        }
        if (avr->pc == untilAddress)
        {
            reachedUntil = 1;
            break;
        }
        if (betweenA && !seenA && avr->pc == addressA)
        {
            seenA = 1;
            cycleA = avr->cycle;
        }
        else if (betweenB && seenA && between < 0 && avr->pc == addressB)
        {
            between = (int64_t)(avr->cycle - cycleA);
        }
        const int state = avr_run(avr);
        executed++;
        if (state == cpu_Done || state == cpu_Crashed) { break; }
    }

    printf("cycles=%llu\n", (unsigned long long)avr->cycle);
    printf("pc=0x%04X\n", (unsigned int)(avr->pc / 2U));
    if (until) { printf("reached=%d\n", reachedUntil); }
    if (betweenA) { printf("between=%lld\n", (long long)between); }
    for (unsigned int r = 0U; r < 32U; ++r) { printf("r%u=0x%02X\n", r, avr->data[r]); }
    const uint8_t flags = sreg();
    printf("SREG=0x%02X\n", flags);
    const char* names = "CZNVSHTI";
    for (unsigned int bit = 0U; bit < 8U; ++bit)
    {
        printf("%c=%u\n", names[bit], (flags >> bit) & 1U);
    }
    printf("SP=0x%04X\n", (unsigned int)(avr->data[SPL_ADDR] | (avr->data[SPH_ADDR] << 8)));
    for (unsigned int addr = 0x20U; addr < 0x100U; ++addr)
    {
        if (addr == SREG_ADDR) { continue; }
        printf("d[0x%02X]=0x%02X\n", addr, avr->data[addr]);
    }
    for (unsigned int addr = 0x100U; addr <= avr->ramend; ++addr)
    {
        if (avr->data[addr]) { printf("d[0x%04X]=0x%02X\n", addr, avr->data[addr]); }
    }
    for (size_t i = 0U; i < changeCount; ++i)
    {
        printf("watch %c%u=%u@%llu\n", changes[i].port, changes[i].bit, changes[i].level,
               (unsigned long long)changes[i].cycle);
    }
    avr_terminate(avr);
    return 0;
}
