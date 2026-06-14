import argparse
import json
import sqlite3
from pathlib import Path

SCHEMA = 'ai_bridge_local.inspect_delivery_failure'


def short(value, limit=800):
    if value is None:
        return None
    text = str(value)
    if len(text) <= limit:
        return text
    return text[:limit] + '...[truncated]'


def row_to_dict(row):
    return {key: short(row[key]) for key in row.keys()}


def category(text):
    t = (text or '').lower()
    if 'submit_button_not_found_or_disabled' in t:
        return 'submit_button_not_found_or_disabled'
    if 'submit_not_confirmed' in t or 'composer_still_has_text' in t:
        return 'submit_not_confirmed'
    if 'envelope_parse_error' in t or 'json' in t or 'parse' in t:
        return 'envelope_parse_error'
    if 'timeout' in t:
        return 'timeout'
    if 'indentationerror' in t or 'syntaxerror' in t:
        return 'python_compile'
    if 'delivering' in t:
        return 'delivering_stuck'
    if 'failed' in t:
        return 'failed_command'
    return 'unknown'


def suggestion(cat):
    tips = {
        'submit_button_not_found_or_disabled': 'Verificar aba destino, composer, permissao da extensao, seletor do botao e estado disabled.',
        'submit_not_confirmed': 'Confirmar se o composer limpou apos clique; se ainda houver texto, retry menor e diagnostico visual.',
        'envelope_parse_error': 'Reenviar envelope menor com JSON estrito ASCII; evitar aspas curvas e comandos inline grandes.',
        'timeout': 'Isolar comando e aumentar timeout somente para validacao pesada.',
        'python_compile': 'Corrigir arquivo apontado e rodar py_compile antes de release_check.',
        'delivering_stuck': 'Inspecionar target_chat_id e eventos; reenfileirar apenas com politica explicita.',
        'failed_command': 'Ler stderr/stdout, reproduzir em read-only e aplicar patch minimo.',
    }
    return tips.get(cat, 'Coletar commands, events, dead_letters e invalid_messages para classificar a falha.')


def query_all(con, sql, params=()):
    try:
        return [row_to_dict(row) for row in con.execute(sql, params).fetchall()]
    except sqlite3.Error as exc:
        return [{'query_error': short(exc)}]


def inspect(con, command_id, limit):
    if command_id:
        commands = query_all(con, 'select * from commands where command_id = ? order by id desc', (command_id,))
        dead = query_all(con, 'select * from dead_letters where command_id = ? order by id desc', (command_id,))
        events = query_all(con, 'select * from events where command_id = ? order by id desc', (command_id,))
        invalid = query_all(con, 'select * from invalid_messages where raw_text like ? order by id desc limit ?', ('%' + command_id + '%', limit))
    else:
        commands = query_all(con, 'select * from commands where status in (\'failed\',\'delivering\') order by id desc limit ?', (limit,))
        dead = query_all(con, 'select * from dead_letters order by id desc limit ?', (limit,))
        events = []
        invalid = query_all(con, 'select * from invalid_messages order by id desc limit ?', (limit,))

    texts = []
    for collection in (commands, dead, events, invalid):
        for item in collection:
            texts.extend(str(item.get(key, '')) for key in ('last_error', 'stderr', 'stdout', 'message', 'error', 'status'))

    cat = category(chr(10).join(texts))
    status = 'found' if commands or dead or events or invalid else 'not_found'
    return {
        'schema': SCHEMA,
        'schema_version': 1,
        'command_id': command_id,
        'status': status,
        'summary': {
            'commands': len(commands),
            'dead_letters': len(dead),
            'events': len(events),
            'invalid_messages': len(invalid),
        },
        'diagnosis': {
            'category': cat,
            'recommended_action': suggestion(cat),
        },
        'records': {
            'commands': commands,
            'dead_letters': dead,
            'events': events,
            'invalid_messages': invalid,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='queue_local.db')
    parser.add_argument('--command-id', default='')
    parser.add_argument('--limit', type=int, default=5)
    args = parser.parse_args()

    db = Path(args.db)
    if not db.exists():
        raise SystemExit('queue db not found: ' + str(db))
    if args.limit < 1 or args.limit > 50:
        raise SystemExit('limit outside policy')

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    print(json.dumps(inspect(con, args.command_id, args.limit), indent=2, sort_keys=True))
    return 0



if __name__ == '__main__':
    raise SystemExit(main())
