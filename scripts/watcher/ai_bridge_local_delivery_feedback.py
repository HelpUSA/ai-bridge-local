# -*- coding: utf-8 -*-
import argparse
import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = 'queue_local.db'
FEEDBACK_PREFIX = 'delivery_feedback_for_'

def parse_dt(value):
    if not value:
        return None
    s = str(value).strip()
    if not s:
        return None
    if s.endswith(chr(90)):
        s = s[:-1] + chr(43) + chr(48) + chr(48) + chr(58) + chr(48) + chr(48)
    if chr(84) in s or chr(43) in s[10:]:
        try:
            return datetime.fromisoformat(s).astimezone(timezone.utc)
        except Exception:
            pass
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    except Exception:
        return None

def age_seconds(row):
    dt = parse_dt(row['delivered_at']) or parse_dt(row['created_at'])
    if not dt:
        return 0
    now = datetime.now(timezone.utc)
    return int((now - dt).total_seconds())

def feedback_exists(con, original_id):
    feedback_id = FEEDBACK_PREFIX + str(original_id)
    row = con.execute('select 1 from commands where command_id=?', (feedback_id,)).fetchone()
    return row is not None

def build_feedback_text(row, age):
    return (
        '[AI_LOCAL_ERRO]\n'
        'acao=verifique_e_reenvie\n'
        'executado=nao\n'
        'tipo=delivery_not_acked\n'
        'id_original=' + str(row['command_id']) + '\n'
        'destino_original=' + str(row['target_chat_id']) + '\n'
        'status_original=' + str(row['status']) + '\n'
        'idade_segundos=' + str(age) + '\n'
        'motivo=O envio inter-chat foi marcado como delivering, mas nao recebeu ack do chat destino dentro do limite.\n'
        'correcao=Confirme se o chat destino esta aberto e ativo. Reenvie com command_id novo ou mande uma mensagem mais simples.\n'
        'observacao=Nada novo foi executado por este feedback; isto e apenas retorno automatico ao chat de origem.'
    )

def feedback_target(row):
    if str(row['source_chat_id']) == 'gateway-brain-supervisor':
        return row['target_chat_id']
    return row['source_chat_id']

def insert_feedback(con, row, age, dry_run=False):
    original_id = str(row['command_id'])
    feedback_id = FEEDBACK_PREFIX + original_id
    if dry_run:
        print('DRY_RUN_FEEDBACK|' + feedback_id + '|to=' + str(feedback_target(row)) + '|original_to=' + str(row['target_chat_id']) + '|age=' + str(age))
        return 0
    con.execute(
        'insert into commands (command_id, source_chat_id, target_chat_id, action, delivery_kind, conversation_id, from_agent, message, payload_json, status, created_at) values (?,?,?,?,?,?,?,?,?,?,?)',
        (
            feedback_id,
            'gateway-brain-supervisor',
            feedback_target(row),
            'send-chat-message',
            'local_inter_agent_message',
            'delivery_feedback_' + str(row['conversation_id'] or 'local'),
            'AI Bridge Local Delivery Feedback 0.4.30',
            build_feedback_text(row, age),
            json.dumps({}, ensure_ascii=False),
            'queued',
            datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        ),
    )
    print('INSERTED_FEEDBACK|' + feedback_id + '|to=' + str(feedback_target(row)) + '|original=' + original_id)
    return 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default=DB_PATH)
    parser.add_argument('--stale-seconds', type=int, default=60)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--include-prefix', default='')
    args = parser.parse_args()

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        '''
        select id, command_id, source_chat_id, target_chat_id, action, delivery_kind,
               conversation_id, from_agent, status, created_at, delivered_at, acked_at, last_error
        from commands
        where action='send-chat-message'
          and delivery_kind='local_inter_agent_message'
          and status in ('queued','delivering')
          and acked_at is null
          and command_id not like ?
        order by id asc
        ''',
        (FEEDBACK_PREFIX + '%',),
    ).fetchall()

    print('CANDIDATES|' + str(len(rows)))
    inserted = 0
    for row in rows:
        command_id = str(row['command_id'])
        if args.include_prefix and not command_id.startswith(args.include_prefix):
            continue
        age = age_seconds(row)
        print('CANDIDATE|' + str(row['id']) + '|' + command_id + '|age=' + str(age) + '|from=' + str(row['source_chat_id']) + '|to=' + str(row['target_chat_id']))
        if age < args.stale_seconds:
            print('SKIP_NOT_STALE|' + command_id)
            continue
        if feedback_exists(con, command_id):
            print('SKIP_ALREADY_FEEDBACK|' + command_id)
            continue
        inserted += insert_feedback(con, row, age, dry_run=args.dry_run)

    if inserted and not args.dry_run:
        con.commit()
    con.close()
    print('INSERTED|' + str(inserted))

if __name__ == '__main__':
    main()
