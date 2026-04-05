import subprocess

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

    # ------------------------------------------------------------------
    # Plymouth communication
    # ------------------------------------------------------------------

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

    def _send_label(self, label):
        if not self._plymouth_active:
            return
        try:
            subprocess.run(
                [SUDO_CMD, PLYMOUTH_CMD, "display-message", "--text", label],
                check=False,
                capture_output=True,
                timeout=2,
            )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Ansible callback hooks
    # ------------------------------------------------------------------

    def v2_playbook_on_task_start(self, task, is_conditional):
        name = task.get_name().strip()

        if name.startswith("Gathering Facts"):
            return

        self._send_label(name)
