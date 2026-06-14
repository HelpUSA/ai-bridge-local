import argparse
import json
import time
import uuid
parser = argparse.ArgumentParser(description='Build and validate local bridge message envelopes.')
parser.add_argument('--from-chat', default='local-source')
parser.add_argument('--to-chat', default='local-target')
parser.add_argument('--message', default='hello local bridge')
parser.add_argument('--action', default='send-chat-message')
args = parser.parse_args()
envelope = {'schema': 'ai_bridge_local.local_bridge_envelope', 'schema_version': 1, 'id': str(uuid.uuid4()), 'created_at_epoch': int(time.time()), 'source_chat_id': args.from_chat, 'target_chat_id': args.to_chat, 'action': args.action, 'message': args.message, 'delivery_kind': 'local_bridge_store', 'executes_commands': False}
checks = [{'name': 'source_present', 'passed': bool(envelope['source_chat_id'])}, {'name': 'target_present', 'passed': bool(envelope['target_chat_id'])}, {'name': 'message_root_field', 'passed': 'message' in envelope}, {'name': 'no_payload_message', 'passed': 'payload' not in envelope}]
envelope['checks'] = checks
envelope['valid'] = all(item['passed'] for item in checks)
print(json.dumps(envelope, ensure_ascii=False, indent=2))
