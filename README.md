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

References

- https://wiki.debian.org/DebianInstaller/Preseed/EditIso
- https://blog.lof.ovh/fr/posts/tutoriels/automatisation-installation-debian-avec-preseed/

## Test Ansible playbook locally

Start a git daemon in a new terminal

```sh
git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack
```

Start preseeded VM on another terminal

```sh
make test-boot
```

Connect and execute ansible-pull manually

```sh
sudo systemctl stop kiosk-deploy

export ANSIBLE_PYTHON_INTERPRETER="auto_silent" 
ansible-pull --url git://10.0.2.2/ --checkout florent/ansible ansible/local.yml
```
