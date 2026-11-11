"""
Corrige duplicatas no inventário REF 13027 — Baguete Modern Linho.
  1. Copia ref_fornecedor/fornecedor das linhas antigas (MAIÚSCULAS) para as novas
  2. Deleta todas as linhas antigas em MAIÚSCULAS

Roda no console bash do PythonAnywhere:
  python corrigir_baguete_modern.py
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

p = db.execute(
    "SELECT id FROM produtos WHERE codigo='13027' OR descricao LIKE '%BAGUETE%MODERN%' COLLATE NOCASE"
).fetchone()
if not p:
    print("ERRO: produto 13027 não encontrado")
    db.close()
    exit(1)
pid = p["id"]

# Mapeamento: linha antiga (cor MAIÚSCULA) → linha nova (cor correta)
pares = [
    ('AZUL',          'Azul'),
    ('CANELA',        'Canela'),
    ('CARAMELO',      'Caramelo'),
    ('CINZA CLARO',   'Cinza claro'),
    ('CINZA ESCURO',  'Cinza esc'),
    ('CRÚ',           'Cru'),
    ('MARINHO',       'Marinho'),
    ('PALHA',         'Palha'),
    ('TABACO',        'Tabaco'),
]

for (cor_old, cor_new) in pares:
    old = db.execute(
        "SELECT id, ref_fornecedor, fornecedor FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor_old)
    ).fetchone()
    if not old:
        continue

    # Copia ref/fornecedor para a linha nova (se a nova existir e estiver vazia)
    novo = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor_new)
    ).fetchone()
    if novo and old["ref_fornecedor"]:
        db.execute(
            "UPDATE inventario_estoque SET ref_fornecedor=?, fornecedor=? WHERE id=?",
            (old["ref_fornecedor"], old["fornecedor"], novo["id"])
        )
        print(f"  Copiado ref_fornecedor '{old['ref_fornecedor']}' de '{cor_old}' → '{cor_new}'")

    # Deleta linha antiga
    db.execute("DELETE FROM inventario_estoque WHERE id=?", (old["id"],))
    print(f"  Deletado: {cor_old}")

# Deleta também linhas sem correspondência (ex: PALHA ESCURO)
sem_par = db.execute(
    "SELECT id, cor FROM inventario_estoque WHERE produto_id=? AND cor=UPPER(cor) AND cor GLOB '*[A-Z]*'",
    (pid,)
).fetchall()
for row in sem_par:
    db.execute("DELETE FROM inventario_estoque WHERE id=?", (row["id"],))
    print(f"  Deletado sem par: {row['cor']}")

db.commit()
db.close()
print("\n✓ Concluído. Faça Reload no PythonAnywhere e recarregue a página.")
