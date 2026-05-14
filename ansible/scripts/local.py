#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

FALLBACK_HOSTNAME = "kiosk"
FALLBACK_STATIC = Path(__file__).resolve().parent.parent / "inventory/prod"


def get_inventory_dir():
    """Return the configured local inventory."""
    return os.environ.get("ANSIBLE_STATIC", FALLBACK_STATIC)


def get_mac_from_interface(iface_path):
    """Read MAC address from a network interface path."""
    mac_file = iface_path / "address"
    if mac_file.exists():
        return mac_file.read_text().strip().lower()
    return None


def detect_mac():
    """Scan network interfaces and return first MAC address."""
    net_dir = Path("/sys/class/net")
    if not net_dir.exists():
        return None

    for iface_path in sorted(net_dir.iterdir()):
        if iface_path.name == "lo":  # Skip loopback
            continue

        if "virtual" in str(iface_path.resolve()):  # Skip virtual
            continue

        mac = get_mac_from_interface(iface_path)
        if mac:
            return mac

    return None


def load_inventory():
    """Load static inventory."""
    try:
        cmd = ["ansible-inventory", "--list", "--inventory", get_inventory_dir()]
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, env=os.environ
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error loading static inventory: {e.stderr}", file=sys.stderr)
        return {}


def find_host_by_mac(inventory, target_mac):
    """Find hostname and hostvars by MAC address in all groups."""
    if not target_mac:
        return None, None

    hostvars = inventory.get("_meta", {}).get("hostvars", {})
    for hostname, vars in hostvars.items():
        if vars.get("ansible_macaddress", "").lower() == target_mac:
            return hostname, vars

    return None, None


def resolve_membership(inventory, hostname):
    """Returns all groups to which the host belongs."""
    if not hostname:
        return ["ungrouped"]

    groups = {g for g, d in inventory.items() if hostname in d.get("hosts", [])}

    def add_parents(child):
        for parent, d in inventory.items():
            if child in d.get("children", []) and parent not in groups:
                groups.add(parent)
                add_parents(parent)

    for g in list(groups):
        add_parents(g)
    return list(groups) or ["ungrouped"]


def build_final_hostvars(hostvars):
    """Build hostvars with ansible connection defaults."""
    return {
        **(hostvars or {}),
        "ansible_connection": "local",
        "ansible_host": "127.0.0.1",
    }


def generate():
    """Generate Ansible dynamic inventory for local execution."""
    inventory = load_inventory()
    mac = detect_mac()

    # Find host by MAC or use fallback
    hostname, hostvars = find_host_by_mac(inventory, mac)
    if not hostname:
        hostname = FALLBACK_HOSTNAME
        hostvars = {}

    # Find all target related groups
    groups = resolve_membership(inventory, hostname)

    # Build final result
    return {
        "_meta": {"hostvars": {hostname: build_final_hostvars(hostvars)}},
        "all": {"children": groups},
        **{g: {"hosts": [hostname]} for g in groups},
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(json.dumps(generate(), indent=2))
    else:
        print(json.dumps({}))
