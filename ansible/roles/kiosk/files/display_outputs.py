#!/usr/bin/env python3
# Ansible fact: ansible_local['display_outputs']
#
# Discovers connected display outputs using DRM (Direct Rendering Manager).
# Scans /sys/class/drm for connected outputs and returns their names.

import json
import re
from pathlib import Path

DRM_ROOT = Path("/sys/class/drm")


def _first_line(path):
    try:
        return path.read_text().splitlines()[0]
    except (OSError, IndexError):
        return ""


def discover_outputs():
    outputs = []
    for status_path in sorted(DRM_ROOT.glob("card?/card*/status")):
        if _first_line(status_path) != "connected":
            continue

        drm_dir = status_path.parent
        name = re.sub(r"^card\d+-", "", drm_dir.name)

        outputs.append(name)

    return outputs


if __name__ == "__main__":
    print(json.dumps(discover_outputs()))
