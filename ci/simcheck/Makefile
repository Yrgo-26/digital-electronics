# Build the simulator harness ci/simtest.py runs every tested program on.
#
# Needs simavr's library and headers, and libelf, which libsimavr links against:
#   sudo apt -y install gcc make simavr libsimavr-dev libelf-dev
CC := gcc
CFLAGS := -std=c11 -D_GNU_SOURCE -O2 -Wall -Wextra -Werror
LDLIBS := -lsimavr -lelf

simcheck: simcheck.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f simcheck

.PHONY: clean
