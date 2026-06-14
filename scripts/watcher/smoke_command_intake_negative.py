import subprocess
import sys
def expect_fail(*args):
 cp = subprocess.run([sys.executable, 'scripts/watcher/command_intake.py', *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 assert cp.returncode != 0, cp.stdout
expect_fail('--intent', 'unknown_intent')
expect_fail('--intent', 'inspect_repo', '--cwd', 'Z:/definitely_missing_path')
expect_fail('--intent', 'inspect_repo', '--timeout', '9999')
expect_fail('--intent', 'inspect_repo', '--inline-command', 'AI_BRIDGE_LOCAL_START')
expect_fail('--intent', 'inspect_repo', '--inline-command', 'remove-item temp.txt')
expect_fail('--intent', 'push_release', '--allow-network-push')
print('OK command_intake_negative_smoke')
