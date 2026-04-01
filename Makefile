ISOBASEFILE  = debian-13.4.0-amd64-netinst.iso
ISOPRESEED   = preseed-$(ISOBASEFILE)
TESTVMDISK   = test-disk.qcow2
INSTALLDIR   = installer
INSTALLFILES = $(shell find $(INSTALLDIR) -type f -not -name preseed.cfg)

$(ISOPRESEED): .xorrisorc
	rm -f $(ISOPRESEED)
	xorriso -no_rc -options_from_file $<

.INTERMEDIATE: initrd_original.gz initrd_patch.gz initrd_final.gz .xorrisorc

initrd_original.gz: $(ISOBASEFILE)
	osirrox -indev $< -extract /install.amd/initrd.gz $@

initrd_patch.gz: $(INSTALLDIR)/preseed.cfg
	cd $(INSTALLDIR) ;\
	echo preseed.cfg | cpio -H newc -o | gzip -9 > ../$@

initrd_final.gz: initrd_original.gz initrd_patch.gz
	cat $^ > $@

.xorrisorc: initrd_final.gz $(INSTALLFILES)
	@echo "-indev $(ISOBASEFILE)" > $@
	@echo "-outdev $(ISOPRESEED)" >> $@
	@echo "-map $< /install.amd/initrd.gz" >> $@
	@$(foreach l, $(filter-out $<, $^), \
	    echo "-map $(l) $(patsubst $(INSTALLDIR)/%,/%,$(l))" >> $@;)
	@echo "-boot_image any replay" >> $@
	@echo "-compliance no_emul_toc" >> $@

$(TESTVMDISK): $(ISOPRESEED)
	qemu-img create -f qcow2 $@ 20G

test-boot: $(TESTVMDISK)
	qemu-system-x86_64 \
	    -enable-kvm -cpu host -smp 4 -m 1G \
	    -net nic,model=virtio \
	    -net user,hostfwd=tcp::2222-:22 \
	    -serial stdio \
	    -cdrom $(ISOPRESEED) \
	    -drive file=$(TESTVMDISK),format=qcow2,if=virtio,cache=unsafe \
	    -virtfs local,path=ansible,mount_tag=ansible,readonly=on,security_model=none

test-ansible: PLAYBOOK = kiosk-installer/ansible/local.yml
test-ansible:
	@ssh -F .ssh_config kiosk-dev \
	    "sudo mount -t 9p -o trans=virtio ansible $(dir $(PLAYBOOK)) 2>/dev/null || true && \
	    ansible-playbook $(PLAYBOOK) -i localhost,"
