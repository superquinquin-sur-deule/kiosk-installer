#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import yaml

INVENTORY_FILE = Path(__file__).parent / "inventory.yml"
FALLBACK_HOSTNAME = "kiosk-dev"


def detect_mac():
    """Scan all network interfaces and return first MAC address."""
    net_dir = Path("/sys/class/net")
    if not net_dir.exists():
        return None

    for iface_path in sorted(net_dir.iterdir()):
        iface = iface_path.name
        if iface == "lo":  # Skip loopback
            continue

        mac_file = iface_path / "address"
        if mac_file.exists():
            return mac_file.read_text().strip()

    return None


def load_inventory_file():
    """Load inventory.yml, return dict or empty dict on error."""
    try:
        with open(INVENTORY_FILE) as f:
            return yaml.safe_load(f) or {}
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error loading {INVENTORY_FILE}: {e}", file=sys.stderr)
        return {}


def resolve_hostname(mac, hosts_map):
    """Return hostname for MAC, fallback to default."""
    return hosts_map.get(mac, FALLBACK_HOSTNAME)


def find_host_groups(hostname, groups_map):
    """Return set of groups containing this hostname. 'all' is always implicit."""
    groups = {g for g, members in groups_map.items() if hostname in members}
    groups.add("all")
    return groups


def build_hostvars(hostname):
    """Build hostvars entry for hostname."""
    return {
        hostname: {
            "ansible_connection": "local",
            "ansible_host": "127.0.0.1",
        }
    }


def build_groups(host_groups, hostname):
    """Build group entries with membership."""
    return {group: {"hosts": [hostname]} for group in host_groups}


def generate():
    """Generate Ansible dynamic inventory."""
    data = load_inventory_file()
    hosts_map = data.get("hosts", {})
    groups_map = data.get("groups", {})

    mac = detect_mac()
    hostname = resolve_hostname(mac, hosts_map)
    host_groups = find_host_groups(hostname, groups_map)

    inventory = {
        "_meta": {"hostvars": build_hostvars(hostname)},
        **build_groups(host_groups, hostname),
    }

    return inventory


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(json.dumps(generate(), indent=2))
    else:
        print(json.dumps({}))
