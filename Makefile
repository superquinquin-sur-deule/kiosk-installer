ISO=dist/alpine-virt-3.23.3-x86_64.iso
TAR=dist/localhost.apkovl.tar.gz
OUT=dist/sqqs-kiosk.iso
SRC=$(find overlay -type f)

build: $(OUT)

clean:
	rm -f $(OUT) $(TAR)

run: build
	qemu-system-x86_64 \
        -m 512M -nic user \
        -cdrom $(OUT)

$(TAR): $(SRC)
	tar --owner=0 --group=0 -czf $(TAR) -C overlay .

$(OUT): $(TAR)
	rm -f $@
	xorriso \
      -indev $(ISO) -outdev $@ \
      -map $(TAR) /localhost.apkovl.tar.gz \
      -boot_image any replay
