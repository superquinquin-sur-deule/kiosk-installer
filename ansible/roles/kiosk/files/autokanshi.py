#!/usr/bin/env python3
"""Generate kanshi display configuration from connected outputs."""

import argparse
import sys
from pathlib import Path

from jinja2 import Template

DRM = Path("/sys/class/drm")
PREFERRED = "1920x1080"
PROFILE_TEMPLATE = """{% for config in configs %}profile {{ config.profile }} {
{%- for output in config.outputs %}
    output "{{ output.name }}" mode {{ output.display_mode }} position {{ output.position }}
{%- endfor %}
}
{% endfor %}"""


def get_connected_outputs():
    """Discover connected display outputs from DRM."""
    return [
        d.parent
        for d in DRM.glob("card*-*/status")
        if d.read_text().strip() == "connected"
    ]


def get_available_modes(output):
    """Read available modes for an output."""
    return output.joinpath("modes").read_text().splitlines()


def find_common_mode(outputs):
    """Find best common mode supported by all outputs."""
    if not outputs:
        return None

    first_modes = get_available_modes(outputs[0])
    common = [
        m for m in first_modes if all(m in get_available_modes(o) for o in outputs[1:])
    ]
    return common[0] if common else PREFERRED


def make_output_config(output, mode):
    """Create output configuration dict."""
    return {
        "name": output.name.split("-", 1)[-1],
        "display_mode": mode,
        "position": "0,0",
    }


def build_profile(outputs, mode, indices, name):
    """Build a profile configuration for selected outputs."""
    return {
        "profile": name,
        "outputs": [make_output_config(outputs[i], mode) for i in indices],
    }


def generate_profiles(outputs, mode):
    """Generate profiles: dual-output mirror + single outputs, or default."""
    if len(outputs) != 2:
        return [build_profile(outputs, mode, range(len(outputs)), "mirror")]

    return [
        build_profile(outputs, mode, [0, 1], "mirror"),
        build_profile(outputs, mode, [0], "single_0"),
        build_profile(outputs, mode, [1], "single_1"),
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Generate kanshi display configuration"
    )
    parser.add_argument("--write-to", dest="output", help="Output file path")
    args = parser.parse_args()

    outputs = get_connected_outputs()
    mode = find_common_mode(outputs)

    if not (outputs and mode):
        return

    profiles = generate_profiles(outputs, mode)
    content = Template(PROFILE_TEMPLATE).render(configs=profiles)

    if args.output:
        try:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(content)
        except (PermissionError, OSError) as e:
            sys.exit(f"Error writing to {args.output}: {e}")
    else:
        print(content)


if __name__ == "__main__":
    main()
