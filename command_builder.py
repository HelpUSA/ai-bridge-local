# -- coding: utf-8 --
import json
import uuid

def new_command_id(prefix):
    return prefix + str(uuid.uuid4())

def build_send_chat_message(source_chat_id, target_chat_id, message):
    return {'schema': 'ai_bridge_local.envelope', 'schema_version': 1, 'command_id': new_command_id('send_chat_'), 'action': 'send-chat-message', 'source_chat_id': source_chat_id, 'target_chat_id': target_chat_id, 'delivery_kind': 'inter_agent_message', 'message': message}

def build_run_command(source_chat_id, cwd, command):
    if isinstance(command, str):
        command = [command]
    return {'schema': 'ai_bridge_local.envelope', 'schema_version': 1, 'command_id': new_command_id('run_'), 'action': 'run-command', 'source_chat_id': source_chat_id, 'target_chat_id': 'gateway-brain-supervisor', 'delivery_kind': 'local_capability', 'payload': {'cwd': cwd, 'timeout_seconds': 120, 'command': command}}

def dumps(envelope):
    return json.dumps(envelope, ensure_ascii=False, indent=2)

def build_script_command(source_chat_id, cwd, script_path, timeout_seconds=120):
 return build_run_command(source_chat_id, cwd, ['python', script_path])
