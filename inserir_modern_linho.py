"""
Importa dados do inventário — Almof Modern Linho (REF 12566)
Roda no console bash do PythonAnywhere:
  python inserir_modern_linho.py

Notas:
  Linha "Ulian" aparece duplicada → apenas a com est_atual=204 foi importada
  Linhas vazias e nota de data ignoradas
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

p = db.execute("SELECT id FROM produtos WHERE codigo='12566'").fetchone()
if not p:
    print("ERRO: produto 12566 não encontrado!")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto 12566 → id={pid}")

dados = [
    # (cor, est_atual, cortado, est_tecido_pcs, ref_fornecedor)
    ("Caramelo",    300, "XX",   "5",       "214"),
    ("Palha",       210, "XXXX", "2",       "204"),
    ("Canela",      200, "XX",   "5",       "828"),
    ("Azul",        120, "XX",   "3",       "730"),
    ("Tabaco",       90, "XXXX", "2",       "840"),
    ("Cinza esc",   210, "XXX",  "4 1/4",   "903"),
    ("Cru",         130, "XX",   "11 1/2",  "200"),
    ("Cinza claro",  90, None,   "1/2",     "GELO Edan"),
    ("Marinho",      80, "X",    None,      None),
    ("Palha esc",    90, "X",    None,      None),
    ("Ulian",       204, None,   None,      None),
]

inseridos = 0
atualizados = 0
for (cor, est_atual, cortado, est_tc, ref_forn) in dados:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            """UPDATE inventario_estoque
               SET est_atual=?, cortado=?, est_tecido_pcs=?, ref_fornecedor=?
               WHERE id=?""",
            (est_atual, cortado, est_tc, ref_forn, ex["id"])
        )
        atualizados += 1
        print(f"  Atualizado: {cor}")
    else:
        db.execute(
            """INSERT INTO inventario_estoque
               (produto_id, cor, est_atual, cortado, est_tecido_pcs, ref_fornecedor)
               VALUES (?,?,?,?,?,?)""",
            (pid, cor, est_atual, cortado, est_tc, ref_forn)
        )
        inseridos += 1
        print(f"  Inserido:  {cor}")

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
