import subprocess

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "plymouth_send"

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.plymouth_cmd = "/usr/bin/plymouth"
        try:
            result = subprocess.run(
                [
                    "/usr/bin/sudo",
                    self.plymouth_cmd,
                    "--ping",
                ],
                capture_output=True,
                timeout=1,
            )
            self.enabled = result.returncode == 0
        except Exception:
            self.enabled = False

    def _display_to_plymouth(self, message):
        if self.enabled:
            try:
                subprocess.run(
                    [
                        "/usr/bin/sudo",
                        self.plymouth_cmd,
                        "display-message",
                        "--text",
                        message,
                    ],
                    check=False,
                    capture_output=True,
                    timeout=2,
                )
            except Exception:
                pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        name = task.get_name().strip()
        if name and not name.startswith("Gathering Facts"):
            self._display_to_plymouth(name)
