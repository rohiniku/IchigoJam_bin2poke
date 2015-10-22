TARGET_ARCH=arm-none-eabi-
CC=$(TARGET_ARCH)gcc
OBJCOPY=$(TARGET_ARCH)objcopy
RM=rm
PYTHON=python
BIN2POKE=bin2poke.py
CFLAGS=-c -mthumb -mlittle-endian -mno-unaligned-access -Os
BIN2POKE_OPT=-a 0x700 -s 100 -d 10
#BIN2POKE_OPT+=-o dec
#BIN2POKE_OPT+=-c 16
#BIN2POKE_OPT+=-o bin -c 2

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

%.bin: %.o
	$(OBJCOPY) -O binary $< $@

%.bas: %.bin
	$(PYTHON) $(BIN2POKE) $(BIN2POKE_OPT) $< $@

clean:
	$(RM) *.o *.bin
