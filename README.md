# kiosk installer

Unattended install of Superquinquin’s Linux kiosk.

## Build

Download a netinst ISO from debian.org

```sh
make ISOBASEFILE=debian-13.3.0-amd64-netinst.iso
```

## Tests

### Booting

Boot on a volatile 20GB-sized qcow file

- Console output redirected to `/dev/ttyS0` for debugging.
- Host-to-guest SSH through `ssh -F ssh_config kiosk-dev`.
- Local `ansible/` directory shared via VirtFS with the `ansible` tag.

```sh
# Start the VM
make test-boot

# Force a fresh install from ISO
make --always-make test-boot
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
