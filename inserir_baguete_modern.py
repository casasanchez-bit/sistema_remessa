"""
Importa dados do inventário — Baguete Modern (REF 13027)
Roda no console bash do PythonAnywhere:
  python inserir_baguete_modern.py

Notas:
  Planilha não tem colunas Est TC nem Ref Fornecedor
  Linhas vazias e nota de data ignoradas
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

p = db.execute("SELECT id FROM produtos WHERE codigo='13027'").fetchone()
if not p:
    print("ERRO: produto 13027 não encontrado!")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto 13027 → id={pid}")

dados = [
    # (cor, est_atual, cortado)
    ("Caramelo",    40, "X"),
    ("Canela",      30, "X"),
    ("Palha",       50, "X"),
    ("Azul",        50, "X"),
    ("Tabaco",      60, "XX"),
    ("Cinza esc",   60, "XX"),
    ("Cru",         60, "XX"),
    ("Marinho",     10, None),
    ("Cinza claro", 60, None),
]

inseridos = 0
atualizados = 0
for (cor, est_atual, cortado) in dados:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            """UPDATE inventario_estoque
               SET est_atual=?, cortado=?
               WHERE id=?""",
            (est_atual, cortado, ex["id"])
        )
        atualizados += 1
        print(f"  Atualizado: {cor}")
    else:
        db.execute(
            """INSERT INTO inventario_estoque
               (produto_id, cor, est_atual, cortado)
               VALUES (?,?,?,?)""",
            (pid, cor, est_atual, cortado)
        )
        inseridos += 1
        print(f"  Inserido:  {cor}")

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
