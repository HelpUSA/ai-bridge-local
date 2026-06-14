import json
ROLES = [
 {'role': 'supervisor', 'responsibility': 'define objective, scope, gates, and final acceptance', 'may_execute': False},
 {'role': 'executor', 'responsibility': 'inspect repo, propose patch, run approved commands, and report evidence', 'may_execute': True},
 {'role': 'fiscal', 'responsibility': 'review plan, validate evidence, block unsafe scope, and request corrections', 'may_execute': False},
 {'role': 'documentador', 'responsibility': 'update guide, roadmap, release notes, and handoff context', 'may_execute': False},
]
print(json.dumps({'schema': 'ai_bridge_local.responsibility_matrix', 'schema_version': 1, 'roles': ROLES}, ensure_ascii=False, indent=2))
