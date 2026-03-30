# kiosk installer

Unattended install of Superquinquin’s Linux kiosk.

## Build

Download a netinst ISO from debian.org

```sh
make ISOBASEFILE=debian-13.3.0-amd64-netinst.iso
```

## Test on QEMU/KVM

Boot on a volatile 20GB-sized qcow file

- write on `/dev/ttyS0` for debugging
- connect with `ssh -p 2222 <user>@localhost`

```sh
make test-boot
```

Force a new installation

```sh
make --always-make test-boot
```

## Control preseed syntax

```sh
docker run --volume $PWD:/src --workdir /src --rm debian:bookworm-slim bash -c \
    "apt-get update && apt-get install -y debconf-utils && debconf-set-selections -c preseed.cfg && echo ok"
```

References

- https://wiki.debian.org/DebianInstaller/Preseed/EditIso
- https://blog.lof.ovh/fr/posts/tutoriels/automatisation-installation-debian-avec-preseed/
