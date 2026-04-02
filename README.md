# kiosk installer

Unattended install of Superquinquin’s Linux kiosk.

## Create ISO file

Download a netinst ISO from debian.org

```sh
make ISOLABEL=KIOSK-202604 ISOBASEFILE=debian-13.4.0-amd64-netinst.iso
```

## Prepare USB stick

Plug your USB stick and identify its block device

```console
$ make DEVICE=/dev/sdc usb
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sdc      8:32   1  3.7G  0 disk
├─sdc1   8:33   1  753M  0 part
└─sdc2   8:34   1  3.5M  0 part

Are you sure you want to wipe /dev/sdc? [y/N] y
188+1 records in
188+1 records out
789884928 bytes (790 MB, 753 MiB) copied, 74.0032 s, 10.7 MB/s
```

## Tests

### Booting

Legacy Boot on a volatile 20GB-sized qcow file

- Console output redirected to `/dev/ttyS0` for debugging.
- Host-to-guest SSH through `ssh -F ssh_config kiosk-dev`.
- Local `ansible/` directory shared via VirtFS with the `ansible` tag.

```sh
# Start the VM
make test-boot

# Force a fresh install from ISO
make --always-make test-boot
```

UEFI boot requires OVMF library (depend on your workstation)

```sh
# Start with UEFI
make OVMF=/usr/share/edk2/x64/OVMF.4m.fd test-boot
```

### Provisionning

The `ansible/` directory is mounted as a 9p volume inside the VM. This allows live
editing of the playbook on the host and immediate execution on the guest.

```sh
# Run the local-only playbook through SSH
make test-ansible
```

## References

- Modifying an installation ISO image to preseed the installer from its initrd <https://wiki.debian.org/DebianInstaller/Preseed/EditIso>
- Automatiser l’installation de Debian avec un fichier preseed.cfg <https://blog.lof.ovh/fr/posts/tutoriels/automatisation-installation-debian-avec-preseed/>
- QEMU 9p setup <https://wiki.qemu.org/Documentation/9psetup>
