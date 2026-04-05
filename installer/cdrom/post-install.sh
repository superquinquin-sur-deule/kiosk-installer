#!/bin/sh
set -xe
exec > /dev/ttyS0 2>&1

ANSIBLE_HOME=/var/lib/ansible
in-target usermod --home ${ANSIBLE_HOME} --move-home ansible

cp -r /cdrom/assets/. /target/
in-target chown -R ansible:ansible ${ANSIBLE_HOME}
in-target chmod 700 ${ANSIBLE_HOME}
in-target chmod 700 ${ANSIBLE_HOME}/.ssh
in-target chmod 600 ${ANSIBLE_HOME}/.ssh/authorized_keys
in-target chmod 440 /etc/sudoers.d/ansible

in-target systemctl enable dbus
in-target systemctl enable systemd-resolved systemd-networkd
in-target systemctl enable kiosk-installer.service
in-target apt-get purge -y ifupdown

in-target plymouth-set-default-theme superquinquin
in-target systemctl mask getty@tty1.service

in-target update-grub
in-target update-initramfs -u
