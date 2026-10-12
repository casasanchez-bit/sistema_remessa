"""
Setup inicial do módulo Etiquetas:
  1. Cria usuário ETIQUETA / ETIQUETA (se não existir)
  2. Importa 897 produtos da tabela unificada (JSON gerado localmente)
  3. Cria tabela etiquetas_produtos se não existir

Rodar UMA VEZ no PythonAnywhere:
  python setup_etiquetas.py
"""
import sqlite3, json, os, hashlib, base64, hmac, re
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, "controle_remessa.db")

def hash_senha(senha):
    """Mesmo método usado no app.py (werkzeug pbkdf2)."""
    try:
        from werkzeug.security import generate_password_hash
        return generate_password_hash(senha)
    except ImportError:
        # fallback simples caso werkzeug não esteja disponível
        import hashlib, os
        sal = os.urandom(16).hex()
        h = hashlib.sha256((sal + senha).encode()).hexdigest()
        return f"sha256${sal}${h}"

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# ── 1. Garantir tabela etiquetas_produtos ──────────────────────────────────
db.execute("""
CREATE TABLE IF NOT EXISTS etiquetas_produtos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT UNIQUE NOT NULL,
    descricao   TEXT NOT NULL,
    preco_atacado REAL,
    preco_varejo  REAL,
    atualizado_em TEXT
)
""")
db.commit()
print("Tabela etiquetas_produtos OK.")

# ── 2. Criar usuário ETIQUETA ──────────────────────────────────────────────
existente = db.execute("SELECT id FROM usuarios WHERE usuario='ETIQUETA'").fetchone()
if existente:
    uid = existente["id"]
    print(f"Usuário ETIQUETA já existe (id={uid}).")
else:
    h = hash_senha("ETIQUETA")
    cur = db.execute(
        "INSERT INTO usuarios (usuario, senha_hash, criado_em) VALUES (?,?,?)",
        ("ETIQUETA", h, date.today().isoformat())
    )
    uid = cur.lastrowid
    db.commit()
    print(f"Usuário ETIQUETA criado (id={uid}).")

# Garantir permissão etiquetas
perm = db.execute(
    "SELECT id FROM permissoes_usuario WHERE usuario_id=? AND permissao='etiquetas'", (uid,)
).fetchone()
if not perm:
    db.execute(
        "INSERT INTO permissoes_usuario (usuario_id, permissao) VALUES (?,?)",
        (uid, "etiquetas")
    )
    db.commit()
    print("Permissão 'etiquetas' adicionada ao usuário ETIQUETA.")
else:
    print("Permissão 'etiquetas' já existe.")

# ── 3. Importar produtos ───────────────────────────────────────────────────
# O JSON deve estar na mesma pasta do script (copiado do ambiente local)
json_path = os.path.join(BASE, "produtos_etiquetas.json")
if not os.path.exists(json_path):
    print(f"\nARQUIVO NÃO ENCONTRADO: {json_path}")
    print("Copie o arquivo produtos_etiquetas.json para a pasta do projeto e rode novamente.")
else:
    with open(json_path, encoding="utf-8") as f:
        produtos = json.load(f)

    hoje = date.today().isoformat()
    inseridos = atualizados = 0
    for p in produtos:
        codigo    = str(p.get("codigo", "")).strip()
        descricao = str(p.get("descricao", "")).strip()
        pat       = p.get("preco_atacado")
        pv        = p.get("preco_varejo")
        if not codigo or not descricao:
            continue
        existe = db.execute("SELECT id FROM etiquetas_produtos WHERE codigo=?", (codigo,)).fetchone()
        if existe:
            db.execute(
                "UPDATE etiquetas_produtos SET descricao=?, preco_atacado=?, preco_varejo=?, atualizado_em=? WHERE codigo=?",
                (descricao, pat, pv, hoje, codigo)
            )
            atualizados += 1
        else:
            db.execute(
                "INSERT INTO etiquetas_produtos (codigo, descricao, preco_atacado, preco_varejo, atualizado_em) VALUES (?,?,?,?,?)",
                (codigo, descricao, pat, pv, hoje)
            )
            inseridos += 1

    db.commit()
    total = db.execute("SELECT COUNT(*) FROM etiquetas_produtos").fetchone()[0]
    print(f"\nImportação concluída:")
    print(f"  Inseridos:   {inseridos}")
    print(f"  Atualizados: {atualizados}")
    print(f"  Total tabela: {total}")

db.close()
print("\nSetup concluído.")
