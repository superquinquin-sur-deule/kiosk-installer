ISOBASEFILE=debian-13.3.0-amd64-netinst.iso
ISOPRESEED=preseed-$(ISOBASEFILE)

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

test:
	qemu-img create -f qcow2 test-disk.qcow2 2G
	qemu-system-x86_64 \
	    -m 1G -net nic,model=virtio -net user \
	    -cdrom preseed-debian-13.3.0-amd64-netinst.iso \
	    -drive file=test-disk.qcow2,format=qcow2
