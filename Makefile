ISOBASEFILE=debian-13.3.0-amd64-netinst.iso
ISOPRESEED=preseed-$(ISOBASEFILE)
TESTVMDISK=test-disk.qcow2
INSTALLDIR=installer

$(ISOPRESEED): .xorrisorc
	rm -f $(ISOPRESEED)
	xorriso -no_rc -options_from_file $<

.INTERMEDIATE: initrd_original.gz initrd_patch.gz initrd_final.gz .xorrisorc

initrd_original.gz:
	osirrox -indev $(ISOBASEFILE) -extract /install.amd/initrd.gz $@

initrd_patch.gz:
	cd $(INSTALLDIR) ;\
	echo preseed.cfg | cpio -H newc -o | gzip -9 > ../$@

initrd_final.gz: initrd_original.gz initrd_patch.gz
	cat $^ > $@

.xorrisorc: initrd_final.gz
	@echo "-indev $(ISOBASEFILE)" > $@
	@echo "-outdev $(ISOPRESEED)" >> $@
	@echo "-map $< /install.amd/initrd.gz" >> $@
	@find $(INSTALLDIR) -type f -not -name preseed.cfg -printf "-map %p /%P\n" >> $@
	@echo "-boot_image any replay" >> $@
	@echo "-compliance no_emul_toc" >> $@

$(TESTVMDISK):
	qemu-img create -f qcow2 $@ 20G

test-boot: $(TESTVMDISK)
	qemu-system-x86_64 \
	    -enable-kvm -cpu host -smp 4 -m 1G \
	    -net nic,model=virtio \
	    -net user,hostfwd=tcp::2222-:22 \
	    -serial stdio \
	    -cdrom $(ISOPRESEED) \
	    -drive file=$(TESTVMDISK),format=qcow2,if=virtio,cache=unsafe
