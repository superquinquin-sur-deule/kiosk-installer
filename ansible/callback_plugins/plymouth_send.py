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
        self._task_index = 0
        self._task_total = 0
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

    def _send_progress(self, ratio):
        if not self._plymouth_active:
            return
        try:
            subprocess.run(
                [
                    SUDO_CMD,
                    PLYMOUTH_CMD,
                    "system-update",
                    f"--progress={int(ratio * 100)}",
                ],
                check=False,
                capture_output=True,
                timeout=2,
            )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Task counting
    # ------------------------------------------------------------------

    def _count_explicit_tasks(self, playbook):
        total = 0
        for play in playbook.get_plays():
            for block in play.compile():
                if isinstance(block, Block):
                    for task in block.get_tasks():
                        if not getattr(task, "implicit", False):
                            total += 1
        return total

    # ------------------------------------------------------------------
    # Message formatting
    # ------------------------------------------------------------------

    def _strip_role_prefix(self, task_name):
        """'system : Install X'  ->  'Install X'"""
        return task_name.split(" : ", 1)[-1]

    # ------------------------------------------------------------------
    # Ansible callback hooks
    # ------------------------------------------------------------------

    def v2_playbook_on_start(self, playbook):
        self._task_total = self._count_explicit_tasks(playbook)
        self._send_progress(0.0)

    def v2_playbook_on_task_start(self, task, is_conditional):
        name = task.get_name().strip()

        if name.startswith("Gathering Facts"):
            return

        self._task_index += 1
        self._send_label(self._strip_role_prefix(name))
        self._send_progress(
            self._task_index / self._task_total if self._task_total else 0.0
        )
