"""
Importa dados do inventário — Dijon com Pingente (REF 13442)
Roda no console bash do PythonAnywhere:
  python inserir_dijon.py

Mapeamento de colunas específico deste produto:
  Planilha "Estampa"      → cor
  Planilha "Cor Pingente" → fornecedor   (campo reaproveitado)
  Planilha "Tamanho"      → ref_fornecedor (campo reaproveitado)
  Linha 5 toda com "~"    → ignorada (riscada no caderno)
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

p = db.execute("SELECT id FROM produtos WHERE codigo='13442'").fetchone()
if not p:
    print("ERRO: produto 13442 não encontrado!")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto 13442 → id={pid}")

# Linha 5 ignorada (toda com ~ = riscada no caderno)
dados = [
    # (estampa→cor, est_atual, cortado, tamanho→ref_fornecedor, cor_pingente→fornecedor)
    ("Borboleta",     20,   "X",    "42x42", "Marrom"),
    ("Zebra",         None, None,   "42x42", "Preto"),
    ("Coqueiro azul", None, "X",    "42x42", "Marinho"),
    ("Tigre",         20,   None,   "48x48", "Preto"),
]

inseridos = 0
atualizados = 0
for (cor, est_atual, cortado, ref_forn, forn) in dados:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            """UPDATE inventario_estoque
               SET est_atual=?, cortado=?, ref_fornecedor=?, fornecedor=?
               WHERE id=?""",
            (est_atual, cortado, ref_forn, forn, ex["id"])
        )
        atualizados += 1
        print(f"  Atualizado: {cor}")
    else:
        db.execute(
            """INSERT INTO inventario_estoque
               (produto_id, cor, est_atual, cortado, ref_fornecedor, fornecedor)
               VALUES (?,?,?,?,?,?)""",
            (pid, cor, est_atual, cortado, ref_forn, forn)
        )
        inseridos += 1
        print(f"  Inserido:  {cor}")

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
