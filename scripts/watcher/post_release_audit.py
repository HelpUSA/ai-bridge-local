import json
import subprocess
from pathlib import Path
ROOT = Path.cwd()
run = lambda cmd: subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
status = run(['git', 'status', '-sb'])
head = run(['git', 'log', '--oneline', '--decorate', '-1'])
version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
latest_tags = run(['git', 'tag', '--sort=-creatordate']).splitlines()[:5]
expected_prefix = 'v' + version
head_has_version_tag = expected_prefix in head
payload = {'schema': 'ai_bridge_local.post_release_audit', 'executes_commands': False, 'status': status, 'head': head, 'version': version, 'latest_tags': latest_tags, 'head_has_version_tag': head_has_version_tag}
print(json.dumps(payload, ensure_ascii=False, indent=2))
