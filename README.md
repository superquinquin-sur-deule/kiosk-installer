# kiosk installer

## Building

Unattended install of Superquinquin’s Linux kiosk.

```bash
docker build -t alpine-gen .
docker run --privileged --rm \
    --volume "$PWD"/dist:/dist \
    alpine-gen --outdir /dist --profile virt
```

## Testing

```bash
qemu-system-x86_64 \
    -m 512M \
    -nic user \
    -cdrom dist/alpine-virt-*-x86_64.iso
```
