"""
Atualiza inventário REF 13027 — Baguete Modern Linho
com os dados do caderno (foto).

Roda no console bash do PythonAnywhere:
  python inserir_baguete_modern.py
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

def vcort(v):
    if v is None: return None
    s = str(v).strip().upper()
    s = ''.join(c for c in s if c == 'X')
    return s if s else None

def inserir(pid, cor, est_atual, cortado):
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            "UPDATE inventario_estoque SET est_atual=?, cortado=? WHERE id=?",
            (est_atual, vcort(cortado), ex["id"])
        )
        return "atualizado"
    else:
        db.execute(
            "INSERT INTO inventario_estoque (produto_id, cor, est_atual, cortado) VALUES (?,?,?,?)",
            (pid, cor, est_atual, vcort(cortado))
        )
        return "inserido"

p = db.execute(
    "SELECT id, descricao FROM produtos WHERE codigo=? OR descricao LIKE ? COLLATE NOCASE",
    ('13027', '%BAGUETE%MODERN%')
).fetchone()

if not p:
    print("ERRO: produto 13027 não encontrado — cadastre no sistema primeiro")
    db.close()
    exit(1)

print(f"→ {p['descricao']} (id={p['id']})")

dados = [
    # (cor,          est_atual, cortado)
    ('Caramelo',     40,  'X'),
    ('Canela',       30,  'X'),
    ('Palha',        50,  'X'),
    ('Azul',         50,  'X'),
    ('Tabaco',       60,  'XX'),
    ('Cinza esc',    60,  'XX'),
    ('Cru',          60,  'XX'),
    ('Marinho',      10,  None),
    ('Cinza claro',  60,  None),
]

for (cor, est, cort) in dados:
    res = inserir(p['id'], cor, est, cort)
    print(f"  {res}: {cor}")

db.commit()
db.close()
print("\n✓ Concluído. Faça Reload no PythonAnywhere e recarregue a página.")
