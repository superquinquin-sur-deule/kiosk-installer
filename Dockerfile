FROM alpine:3.19

RUN apk add --no-cache \
    abuild bash git xorriso squashfs-tools \
    mtools grub-efi alpine-conf alpine-keys
RUN abuild-keygen -a -n

RUN git clone --depth=1 --branch 3.19-stable https://gitlab.alpinelinux.org/alpine/aports.git /aports
ENTRYPOINT ["/aports/scripts/mkimage.sh", "--repository", "https://dl-cdn.alpinelinux.org/alpine/v3.19/main"]
