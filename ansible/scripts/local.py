#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import yaml

INVENTORY_DIR = Path(__file__).parent.parent / "inventory"
FALLBACK_HOSTNAME = "kiosk"


def get_mac_from_interface(iface_path):
    """Read MAC address from a network interface path."""
    mac_file = iface_path / "address"
    if mac_file.exists():
        return mac_file.read_text().strip()
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


def load_yaml_file(yml_file):
    """Load single YAML file, return dict or empty dict on error."""
    try:
        with open(yml_file) as f:
            return yaml.safe_load(f) or {}
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error loading {yml_file}: {e}", file=sys.stderr)
        return {}


def load_inventory():
    """Load and merge all YAML inventory files."""
    data = {}
    for yml_file in sorted(INVENTORY_DIR.glob("*.yml")):
        data |= load_yaml_file(yml_file)
    return data


def find_matching_host(group, target_mac):
    """Search in a group for hostname matching MAC address.

    Returns (hostname, hostvars) or (None, None) if not found.
    """
    if not isinstance(group, dict):
        return None, None

    hosts = group.get("hosts", {})
    if not isinstance(hosts, dict):
        return None, None

    target_mac_lower = target_mac.lower()
    for hostname, hostvars in hosts.items():
        if isinstance(hostvars, dict):
            mac = hostvars.get("ansible_macaddress", "").lower()
            if mac == target_mac_lower:
                return hostname, hostvars

    return None, None


def find_host_by_mac(inventory, target_mac):
    """Find hostname and hostvars by MAC address in all groups."""
    if not target_mac:
        return None, None

    for group in inventory.values():
        hostname, hostvars = find_matching_host(group, target_mac)
        if hostname:
            return hostname, hostvars

    return None, None


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

    # Build final hostvars with ansible defaults
    final_vars = build_final_hostvars(hostvars)

    return {
        "_meta": {"hostvars": {hostname: final_vars}},
        "all": {"hosts": [hostname], "children": ["ungrouped"]},
        "ungrouped": {"hosts": [hostname]},
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print(json.dumps(generate(), indent=2))
    else:
        print(json.dumps({}))
