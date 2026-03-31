#!/bin/sh
set -xe

cp -r /cdrom/assets/. /target/
in-target chmod 440 /etc/sudoers.d/ansible

in-target chown -R ansible:ansible /home/ansible
in-target chmod 700 /home/ansible
in-target chmod 700 /home/ansible/.ssh
in-target chmod 600 /home/ansible/.ssh/authorized_keys

in-target systemctl enable dbus
in-target systemctl enable kiosk-deploy.service
