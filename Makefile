ISOBASEFILE  = debian-13.4.0-amd64-netinst.iso
ISOPRESEED   = preseed-$(ISOBASEFILE)
ISOLABEL     = KIOSK
TESTVMDISK   = test-disk.qcow2
INSTALLDIR   = installer
INSTALLFILES = $(shell find $(INSTALLDIR)/cdrom -type f)
INITRDFILES  = $(shell find $(INSTALLDIR)/initrd -type f)

$(ISOPRESEED): .xorrisorc
	rm -f $(ISOPRESEED)
	xorriso -no_rc -options_from_file $<

.PHONY: usb
usb:
	@test -n "$(DEVICE)" || (echo "Error: DEVICE is undefined. Usage: make DEVICE=/dev/sdX usb"; exit 1)
	@sudo lsblk $(DEVICE)
	@echo
	@echo -n "Are you sure you want to wipe $(DEVICE)? [y/N] " && read ans && [ $${ans:-N} = y ] || [ $${ans:-N} = Y ]
	@sudo dd if=$(ISOPRESEED) of=$(DEVICE) bs=4M status=progress oflag=sync

.INTERMEDIATE: initrd_original.gz initrd_patch.gz initrd_final.gz .xorrisorc

initrd_original.gz: $(ISOBASEFILE)
	osirrox -indev $< -extract /install.amd/gtk/initrd.gz $@

initrd_patch.gz: $(INITRDFILES)
	cd $(INSTALLDIR)/initrd && \
	    printf '%s\n' $(patsubst $(INSTALLDIR)/initrd/%,%,$^) \
	    | cpio -H newc -o | gzip -9 > $(CURDIR)/$@

initrd_final.gz: initrd_original.gz initrd_patch.gz
	cat $^ > $@

.xorrisorc: initrd_final.gz $(INSTALLFILES)
	@echo "-indev $(ISOBASEFILE)" > $@
	@echo "-outdev $(ISOPRESEED)" >> $@
	@echo "-map $< /install.amd/gtk/initrd.gz" >> $@
	@$(foreach l, $(filter-out $<, $^), \
	    echo "-map $(l) $(patsubst $(INSTALLDIR)/cdrom/%,/%,$(l))" >> $@;)
	@echo "-volid $(ISOLABEL)" >> $@
	@echo "-boot_image any replay" >> $@
	@echo "-compliance no_emul_toc" >> $@

$(TESTVMDISK): $(ISOPRESEED)
	qemu-img create -f qcow2 $@ 20G

.PHONY: test-boot
test-boot: $(TESTVMDISK)
	qemu-system-x86_64 \
	    -enable-kvm -cpu host -smp 4 -m 1G \
	    -net nic,model=virtio \
	    -net user,hostfwd=tcp::2222-:22 \
	    -serial stdio $(if $(OVMF),-bios $(OVMF) )\
	    -cdrom $(ISOPRESEED) \
	    -drive file=$(TESTVMDISK),format=qcow2,if=virtio,cache=unsafe \
	    -virtfs local,path=ansible,mount_tag=ansible,readonly=on,security_model=none

.PHONY: test-ansible
test-ansible: PLAYBOOK = kiosk-installer/ansible/local.yml
test-ansible:
	@ssh -F .ssh_config kiosk-dev \
	    "sudo mount -t 9p -o trans=virtio ansible $(dir $(PLAYBOOK)) 2>/dev/null || true && \
	    ansible-playbook $(PLAYBOOK) -i localhost,"
