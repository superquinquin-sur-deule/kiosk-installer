import subprocess

from ansible.playbook.block import Block
from ansible.plugins.callback import CallbackBase

PLYMOUTH_CMD = "/usr/bin/plymouth"
SUDO_CMD = "/usr/bin/sudo"


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "plymouth_send"

    def __init__(self):
        super().__init__()
        self._plymouth_active = self._ping_plymouth()

    def _ping_plymouth(self):
        try:
            result = subprocess.run(
                [SUDO_CMD, PLYMOUTH_CMD, "--ping"],
                capture_output=True,
                timeout=1,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _send_to_plymouth(self, message):
        if not self._plymouth_active:
            return
        try:
            subprocess.run(
                [SUDO_CMD, PLYMOUTH_CMD, "display-message", "--text", message]
            )
        except Exception:
            pass

    def v2_runner_on_ok(self, result):
        self._send_to_plymouth(f"➜ OK: {result._task.get_name()}")

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._send_to_plymouth(f"➜ FAILED: {result._task.get_name()}")
