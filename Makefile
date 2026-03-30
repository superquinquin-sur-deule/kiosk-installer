ISOBASEFILE=debian-13.3.0-amd64-netinst.iso
ISOPRESEED=preseed-$(ISOBASEFILE)
TESTVMDISK=test-disk.qcow2

$(ISOPRESEED): initrd_final.gz
	rm -f $(ISOPRESEED)
	xorriso \
	    -indev $(ISOBASEFILE) \
	    -outdev $(ISOPRESEED) \
	    -map $< /install.amd/initrd.gz \
	    -map isolinux.cfg /isolinux/isolinux.cfg \
	    -map grub.cfg /boot/grub/grub.cfg \
	    -boot_image any replay -compliance no_emul_toc

.INTERMEDIATE: initrd_original.gz initrd_patch.gz initrd_final.gz

initrd_original.gz:
	osirrox -indev $(ISOBASEFILE) -extract /install.amd/initrd.gz $@

initrd_patch.gz:
	echo "preseed.cfg" | cpio -H newc -o | gzip -9 > $@

initrd_final.gz: initrd_original.gz initrd_patch.gz
	cat $^ > $@

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
