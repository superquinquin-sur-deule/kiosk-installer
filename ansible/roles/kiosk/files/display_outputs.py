#!/usr/bin/env python3
# Ansible fact: ansible_local['display_outputs']
#
# Discovers connected display outputs using DRM (Direct Rendering Manager).
# Scans /sys/class/drm for connected outputs and returns their names and preferred modes.

import json
import re
from pathlib import Path

DRM_ROOT = Path("/sys/class/drm")
DEFAULT_MODE = "1920x1080"
_MODE_RE = re.compile(r"\d+x\d+")


def _first_line(path):
    try:
        return path.read_text().splitlines()[0]
    except (OSError, IndexError):
        return ""


def _is_supported(path):
    try:
        return DEFAULT_MODE in path.read_text().splitlines()
    except OSError:
        return False


def discover_outputs():
    outputs = []
    for status_path in sorted(DRM_ROOT.glob("card?/card*/status")):
        if _first_line(status_path) != "connected":
            continue

        drm_dir = status_path.parent
        name = re.sub(r"^card\d+-", "", drm_dir.name)

        modes_path = drm_dir / "modes"
        if _is_supported(modes_path):
            mode = DEFAULT_MODE
        else:
            raw = _first_line(modes_path)
            m = _MODE_RE.search(raw)
            mode = m.group() if m else DEFAULT_MODE

        outputs.append({"name": name, "mode": mode})

    return outputs


if __name__ == "__main__":
    print(json.dumps(discover_outputs()))
