"""
Importa dois produtos da linha Realce:
  - Baguete Realce
  - Almofada Realce

Roda no console bash do PythonAnywhere:
  python inserir_realce.py
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

def buscar(codigos, like):
    for cod in codigos:
        p = db.execute("SELECT id, descricao FROM produtos WHERE codigo=?", (cod,)).fetchone()
        if p: return p
    return db.execute(
        "SELECT id, descricao FROM produtos WHERE descricao LIKE ? COLLATE NOCASE", (like,)
    ).fetchone()

def inserir(pid, cor, est_atual, costureira_1, costureira_2, cortado, ref_fornecedor):
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=? COLLATE NOCASE",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            """UPDATE inventario_estoque SET
               est_atual=?, costureira_1=?, costureira_2=?,
               cortado=?, ref_fornecedor=?
               WHERE id=?""",
            (est_atual, costureira_1, costureira_2,
             vcort(cortado), ref_fornecedor, ex["id"])
        )
        return "atualizado"
    else:
        db.execute(
            """INSERT INTO inventario_estoque
               (produto_id, cor, est_atual, costureira_1, costureira_2, cortado, ref_fornecedor)
               VALUES (?,?,?,?,?,?,?)""",
            (pid, cor, est_atual, costureira_1, costureira_2,
             vcort(cortado), ref_fornecedor)
        )
        return "inserido"

# ══════════════════════════════════════════════════════════════════════════════
# Baguete Realce
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Baguete Realce ===")
p = buscar(['C9144', '09144'], '%BAGUETE%REALCE%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,          est,  cost1, cost2, cortado, ref)
        ('Palha',         2,   None,  None,  'X',     None),
        ('Canela',        50,  None,  None,  'X',     None),
        ('Avelã',         10,  None,  None,  None,    '207'),
        ('Cinza',          2,  None,  None,  None,    None),
        ('V. Musgo',      30,  None,  None,  None,    None),
        ('Vermelho',      60,  None,  None,  None,    None),
        ('Rubi',          20,  None,  None,  None,    None),
        ('Branco',        20,  None,  None,  'XX',    None),
        ('Rosé',           0,  None,  None,  'X',     None),
        ('Bege esc',      40,  None,  None,  'X',     None),
        ('Mostarda',      30,  None,  None,  None,    None),
        ('Tabaco Jano',    2,  None,  None,  'X',     None),
        ('Vinho',          2,  None,  None,  'X',     None),
        ('Marccap',        0,  None,  None,  'X',     None),
        ('Marinho',        8,  None,  None,  'X',     '199'),
        ('Kaqui',          8,  None,  None,  'X',     '272'),
        ('Chumbo',        60,  None,  None,  None,    None),
        ('Marfim',        20,  None,  None,  None,    None),
    ]
    for (cor, est, cost1, cost2, cort, ref) in dados:
        res = inserir(p['id'], cor, est, cost1, cost2, cort, ref)
        print(f"  {res}: {cor}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# Almofada Realce
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Almofada Realce ===")
p = buscar(['11882'], '%ALMOF%REALCE%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,           est,   cost1,           cost2, cortado, ref)
        ('Palha',          60,   None,             None,  'X',     None),
        ('Canela',         20,   'Jairo 16/11',    None,  None,    None),
        ('Avelã',          80,   None,             None,  None,    '207'),
        ('Cinza',         None,  None,             None,  None,    None),
        ('V. Musgo',       70,   None,             None,  None,    None),
        ('Vermelho',       20,   'Jairo 16/11',    None,  None,    None),
        ('Rubi',           60,   None,             None,  None,    None),
        ('Branco',        None,  None,             None,  None,    None),
        ('Rosé',           45,   None,             None,  None,    None),
        ('Bege esc',       50,   None,             None,  'X',     None),
        ('Mostarda',       35,   None,             None,  None,    None),
        ('Tabaco Jano',    30,   None,             None,  None,    None),
        ('Vinho',          20,   'Jairo 29/10',    None,  None,    None),
        ('Marccap',        40,   None,             None,  'X',     None),
        ('Marinho',        10,   None,             None,  None,    '199'),
        ('Kaqui',          10,   None,             None,  None,    '272'),
        ('Chumbo',         15,   'Jairo 29/10',    None,  None,    None),
        ('Marfim',         40,   None,             None,  None,    None),
        ('Tabaco Borrn',   10,   None,             None,  'X',     None),
    ]
    for (cor, est, cost1, cost2, cort, ref) in dados:
        res = inserir(p['id'], cor, est, cost1, cost2, cort, ref)
        print(f"  {res}: {cor}")
    db.commit()

db.close()
print("\n✓ Concluído. Faça Reload no PythonAnywhere e recarregue a página.")
