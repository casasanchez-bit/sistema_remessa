"""
Importa 7 produtos de uma vez — lote novembro/2026
Roda no console bash do PythonAnywhere:
  python inserir_lote_novembro.py

Produtos:
  -318  Glamour 42x42
   625  Capa Almofadão Glamour
   769  Mix Color
 12345  Arabesco
 12678  Cp Almof Napoli 42x42
 13594  Capa Almof Print Cordão
 13818  Sevilha Linho 2N
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# ── Helpers ────────────────────────────────────────────────────────────────────
def vint(v):
    if v is None: return None
    s = str(v).strip()
    if s.lstrip('-').isdigit(): return int(s)
    return None

def vstr(v):
    if v is None: return None
    s = str(v).strip()
    return s if s else None

def vcort(v):
    if v is None: return None
    s = str(v).strip().upper()
    s = ''.join(c for c in s if c == 'X')
    return s if s else None

def buscar_produto(codigos, like_fallback):
    for cod in codigos:
        p = db.execute("SELECT id, descricao FROM produtos WHERE codigo=?", (cod,)).fetchone()
        if p: return p
    if like_fallback:
        p = db.execute(
            "SELECT id, descricao FROM produtos WHERE descricao LIKE ? COLLATE NOCASE",
            (like_fallback,)
        ).fetchone()
        if p: return p
    return None

def inserir(pid, cor, vies, est_atual, costureira_1, costureira_2, cortado,
            est_tecido_pcs, ref_fornecedor, fornecedor):
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=? "
        "AND (vies=? OR (vies IS NULL AND ? IS NULL))",
        (pid, cor, vies, vies)
    ).fetchone()
    if ex:
        db.execute(
            """UPDATE inventario_estoque SET
               vies=?, est_atual=?, costureira_1=?, costureira_2=?,
               cortado=?, est_tecido_pcs=?, ref_fornecedor=?, fornecedor=?
               WHERE id=?""",
            (vies, est_atual, costureira_1, costureira_2,
             cortado, est_tecido_pcs, ref_fornecedor, fornecedor, ex["id"])
        )
        return "atualizado"
    else:
        db.execute(
            """INSERT INTO inventario_estoque
               (produto_id, cor, vies, est_atual, costureira_1, costureira_2,
                cortado, est_tecido_pcs, ref_fornecedor, fornecedor)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (pid, cor, vies, est_atual, costureira_1, costureira_2,
             cortado, est_tecido_pcs, ref_fornecedor, fornecedor)
        )
        return "inserido"

# ══════════════════════════════════════════════════════════════════════════════
# REF -318 / 318 — Glamour 42x42
# Colunas: Ref → ref_fornecedor, Est TC → est_tecido_pcs (texto)
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Glamour 42x42 (REF -318 / 318) ===")
p = buscar_produto(['-318', '318'], '%GLAMOUR%42%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,           ref,  est_atual, costureira_1,  cortado, est_tc)
        ('Palha',         '07', 120, None,          None,   None),
        ('Preto',         '08', 60,  'Jairo 9/11',  'X',    '1/2'),
        ('Laranja',       '28', 120, None,          'XX',   None),
        ('Cinza',         '13', 100, None,          None,   None),
        ('V. Musgo',      '02', 160, None,          'XXX',  '2'),
        ('Marrom',        '22', 120, None,          'XXX',  '1'),
        ('Vermelho',      '19', 180, None,          'XXXX', '4 1/2'),
        ('Marinho',       '04', 90,  None,          None,   '1'),
        ('Bege',          '33', 90,  'Jairo 9/11',  'XX',   '4'),
        ('Vinho',         '10', 150, None,          'XXX',  '1 1/2'),
        ('Marinho esc',   '05', 180, None,          'XXX',  '3'),
        ('Canela',        '34', 210, None,          'X',    '2 1/2'),
        ('Kaqui',         '26', 180, 'Jairo 9/11',  None,   '1'),
        ('Chumbo',        None, 90,  None,          None,   '1 1/2'),
    ]
    for (cor, ref, est_atual, cost1, cort, est_tc) in dados:
        res = inserir(p['id'], cor, None, est_atual, cost1, None,
                      vcort(cort), vstr(est_tc), vstr(ref), None)
        print(f"  {res}: {cor}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# REF 625 — Capa Almofadão Glamour
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Almofadão Glamour (REF 625) ===")
p = buscar_produto(['625'], '%ALMOFAD%GLAMOUR%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,           est_atual, costureira_1,   cortado)
        ('Palha',         30, 'Jairo 29/10', None),
        ('Preto',         45, None,          None),
        ('Laranja',      None, None,          None),
        ('Cinza',         30, 'Jairo 29/10', None),
        ('V. Musgo',      40, 'Jairo 29/10', None),
        ('Marrom',        40, None,          None),
        ('Vermelho',      50, None,          None),
        ('Marinho',      None, None,          None),
        ('Bege',          10, 'Jairo 29/10', None),
        ('Vinho',         30, None,          'X'),
        ('Marinho esc',   35, None,          'X'),
        ('Canela',        60, None,          'X'),
        ('Kaqui',         20, 'Jairo 29/10', None),
    ]
    for (cor, est_atual, cost1, cort) in dados:
        res = inserir(p['id'], cor, None, est_atual, cost1, None,
                      vcort(cort), None, None, None)
        print(f"  {res}: {cor}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# REF 769 — Mix Color
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Mix Color (REF 769) ===")
p = buscar_produto(['769'], '%MIX%COLOR%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,            est_atual, costureira_1,  cortado)
        ('Preto',          80,  None,          None),
        ('Vermelho',      210,  None,          'XX'),
        ('Cinza Cezani',  150,  None,          None),
        ('Cinza claro',   120,  None,          None),
        ('V. Musgo',      120,  'Jairo 5/11',  'XX'),
        ('Kaqui',         180,  None,          'X'),
        ('Cinza Feio',    150,  None,          None),
        ('Palha',        None,  'Jairo 5/11',  None),
        ('Avelã',        None,  'Jairo 5/11',  None),
    ]
    for (cor, est_atual, cost1, cort) in dados:
        res = inserir(p['id'], cor, None, est_atual, cost1, None,
                      vcort(cort), None, None, None)
        print(f"  {res}: {cor}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# REF 12345 — Arabesco
# Colunas: Estampa (número) → cor como "Estampa X"
# col_override: cor → 'Estampa' (já em app.py)
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Arabesco (REF 12345) ===")
p = buscar_produto(['12345'], '%ARABESCO%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (numero, cortado, est_tc)
        (1, None, None),
        (2, 'X',  None),
        (3, None, None),
        (4, 'X',  None),
        (5, None, None),
        (6, None, None),
        (7, None, None),
        (8, None, None),
        (9, 'X',  None),
    ]
    for (num, cort, est_tc) in dados:
        cor = f'Estampa {num}'
        res = inserir(p['id'], cor, None, None, None, None,
                      vcort(cort), vstr(est_tc), None, None)
        print(f"  {res}: {cor}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# REF 12678 — Cp Almof Napoli 42x42
# Coluna extra: Fazer Nervura → costureira_2
# col_override: costureira_2 → 'Fazer Nervura' (já em app.py)
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Napoli 42x42 (REF 12678) ===")
p = buscar_produto(['12678'], '%NAPOLI%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,          est_atual, costureira_1,  cortado,  nervura)
        ('Canela',       270, None,         None,    None),
        ('Palha',        270, None,         None,    None),
        ('Avelã',        150, None,         None,    None),
        ('Rosé',         150, None,         None,    None),
        ('Marinho 768',  180, None,         None,    None),
        ('V. Musgo',     240, 'Julia 9/11', 'XXX',   None),
        ('Vinho',        210, None,         None,    None),
        ('Vermelho',     120, 'Julia 9/11', 'XXXX',  None),
        ('Tabaco',       240, None,         None,    'Bete 19/10'),
        ('Preto',        180, None,         None,    None),
        ('Branco',      None, None,         None,    None),
        ('Mostarda',      30, None,         None,    'Bete 12/10'),
        ('Chumbo',       210, None,         None,    None),
        ('Bege esc',     210, None,         None,    None),
        ('Rato',        None, None,         None,    'Bete 19/10'),
        ('Capuccino',   None, None,         None,    None),
        ('Esmeralda',     70, None,         None,    None),
    ]
    for (cor, est_atual, cost1, cort, nervura) in dados:
        res = inserir(p['id'], cor, None, est_atual, cost1, vstr(nervura),
                      vcort(cort), None, None, None)
        print(f"  {res}: {cor}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# REF 13594 — Capa Almof Print Cordão
# Tem Estampa + Viés (como Candy Color)
# col_override: cor → 'Estampa', vies → 'Viés' (já em app.py)
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Print Cordão (REF 13594) ===")
p = buscar_produto(['13594'], '%PRINT%CORD%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (estampa,         viés,       est_atual, costureira_1)
        ('Mini Cereja',    'Vermelho',   30, None),
        ('Flor Vermelha',  'Vermelho',   90, None),
        ('Cereja',         'Vermelho',   90, None),
        ('Costela Adão',   'Canela',     20, None),
        ('Costela Adão',   'V. Musgo',   40, None),
        ('Costela Adão',   'Avelã',      50, None),
        ('Folha',          'Canela',     30, None),
        ('Folha',          'V. Musgo',   60, None),
        ('Folha',          'Avelã',      50, None),
        ('Ramo',           'Canela',     90, None),
        ('Ramo',           'V. Musgo',   90, None),
        ('Ramo',           'Avelã',      50, None),
    ]
    for (estampa, vies, est_atual, cost1) in dados:
        res = inserir(p['id'], estampa, vies, est_atual, cost1, None,
                      None, None, None, None)
        print(f"  {res}: {estampa} / {vies}")
    db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# REF 13818 — Sevilha Linho 2N
# Coluna extra: Fazer Nervura → costureira_2
# Atenção: est_atual=0 é zero real (produto com estoque zerado)
# col_override: costureira_2 → 'Fazer Nervura' (já em app.py)
# ══════════════════════════════════════════════════════════════════════════════
print("\n=== Sevilha Linho 2N (REF 13818) ===")
p = buscar_produto(['13818'], '%SEVILHA%LINHO%')
if not p:
    print("  PRODUTO NÃO ENCONTRADO — cadastre no sistema primeiro")
else:
    print(f"  → {p['descricao']} (id={p['id']})")
    dados = [
        # (cor,        est_atual, costureira_1, cortado, nervura)
        ('Palha',      130, None, None, None),
        ('Canela',       0, None, 'XX', 'Bete 9/11'),
        ('Azul',        60, None, None, None),
        ('Caramelo',     0, None, 'XX', 'Bete 9/11'),
        ('Cinza esc',    0, None, 'XX', 'Bete 5/11'),
        ('Tabaco',     100, None, None, None),
        ('Cru',          0, None, 'XX', 'Bete 9/11'),
        ('Marinho',      0, None, None, None),
    ]
    for (cor, est_atual, cost1, cort, nervura) in dados:
        res = inserir(p['id'], cor, None, est_atual, cost1, vstr(nervura),
                      vcort(cort), None, None, None)
        print(f"  {res}: {cor}")
    db.commit()

db.close()
print("\n✓ Importação concluída. Faça Reload no PythonAnywhere e recarregue a página.")
