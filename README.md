# kiosk installer

Unattended install of Superquinquin’s Linux kiosk.

## Build

```console
$ make ISOBASEFILE=debian-13.3.0-amd64-netinst.iso
```

## Control preseed syntax

```sh
docker run --volume $PWD:/src --workdir /src --rm debian:bookworm-slim bash -c \
    "apt-get update && apt-get install -y debconf-utils && debconf-set-selections -c preseed.cfg && echo ok"
```

References

- https://wiki.debian.org/DebianInstaller/Preseed/EditIso
- https://blog.lof.ovh/fr/posts/tutoriels/automatisation-installation-debian-avec-preseed/
