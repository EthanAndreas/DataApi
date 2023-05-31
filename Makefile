CC = gcc
CFLAGS = -Og -pipe -Wall -Werror -Wextra -g 

BINDIR = bin

all: client server

client: src/client.c
	mkdir -p $(BINDIR)
	gcc -o $(BINDIR)/client src/client.c

server: src/server.c
	gcc -o $(BINDIR)/server src/server.c

	@echo "\033[92mCompiled\033[0m"

.PHONY: clean
clean:
	rm -rf build/*.o
	rm -rf bin/*
	@echo "\033[92mCleaned\033[0m"

	