#!/usr/bin/python
import json
import os

from ansible.module_utils.basic import AnsibleModule


def deep_merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            deep_merge(value, node)
        else:
            destination[key] = value
    return destination


def run_module():
    module_args = dict(
        path=dict(type="str", required=True),
        policies=dict(type="dict", required=False, default={}),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    path = module.params["path"]
    new_policies = module.params["policies"]

    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = {"policies": {}}

    original_data = json.dumps(data, sort_keys=True)

    if module.params["state"] == "present":
        data["policies"] = deep_merge(new_policies, data.get("policies", {}))

    changed = original_data != json.dumps(data, sort_keys=True)

    if changed and not module.check_mode:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    module.exit_json(changed=changed, contents=data)


if __name__ == "__main__":
    run_module()
