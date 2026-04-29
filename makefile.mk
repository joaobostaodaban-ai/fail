# Makefile para 0x0 Malware Suite
CC = gcc
CFLAGS = -Wall -O2 -lpthread -lcurl -lcrypto

all: nexusworm phantompayload abyssrat voidroot shadowkernel

nexusworm:
	$(CC) -o 0x0-NexusWorm 0x0-NexusWorm.c $(CFLAGS)

phantompayload:
	$(CC) -o 0x0-PhantomPayload 0x0-PhantomPayload.c $(CFLAGS)

abyssrat:
	$(CC) -o 0x0-AbyssRat 0x0-AbyssRat.c $(CFLAGS)

voidroot:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

shadowkernel:
	$(CC) -o 0x0-ShadowKernel 0x0-ShadowKernel.c $(CFLAGS)

clean:
	rm -f 0x0-* *.o *.ko