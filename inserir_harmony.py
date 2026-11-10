"""
Importa dados do inventário — Coleção Harmony 42x42 (REF 12026)
Roda no console bash do PythonAnywhere:
  python inserir_harmony.py
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# Encontra produto 12026
p = db.execute("SELECT id FROM produtos WHERE codigo='12026'").fetchone()
if not p:
    print("ERRO: produto 12026 não encontrado!")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto 12026 → id={pid}")

# Dados extraídos da planilha "24 - Harmony 42x42.xlsx"
# est_atual: Lavanda tem 'OK' no caderno → NULL (sem contagem numérica)
# cortado / est_tecido_pcs: valores texto do caderno ('XXX', '3 1/2', etc.)
dados = [
    # (cor,          est_atual, cortado,  est_tecido_pcs)
    ("Canela",       250,       "XXX",    "4"),
    ("Palha",        270,       "XXXX",   "20 ??"),
    ("Marinho",      160,       "XXXX",   "2"),
    ("V. Musgo",     240,       "XX",     "1"),
    ("Rosé",         250,       "XXXX",   "3 1/2"),
    ("Kaqui",        180,       "XXX",    "1 1/2"),
    ("Cinza",        220,       "XXX",    "5"),
    ("Telha",        150,       "XXX",    "1 1/2"),
    ("Mostarda",     210,       "XX",     "2"),
    ("Vermelho",     100,       "XXX",    "2 1/2"),
    ("Coral",        40,        "XX",     "1/4"),
    ("Piscina",      20,        "X",      "1/2"),
    ("Tabaco",       130,       "XXX",    "3 1/2"),
    ("Lavanda",      None,      "X",      "2 OPQ"),   # OK no caderno = sem número
    ("Cereja",       150,       "X",      "3"),
]

inseridos = 0
atualizados = 0
for (cor, est_atual, cortado, est_tc) in dados:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            """UPDATE inventario_estoque
               SET est_atual=?, cortado=?, est_tecido_pcs=?
               WHERE id=?""",
            (est_atual, cortado, est_tc, ex["id"])
        )
        atualizados += 1
        print(f"  Atualizado: {cor}")
    else:
        db.execute(
            """INSERT INTO inventario_estoque
               (produto_id, cor, est_atual, cortado, est_tecido_pcs)
               VALUES (?,?,?,?,?)""",
            (pid, cor, est_atual, cortado, est_tc)
        )
        inseridos += 1
        print(f"  Inserido:  {cor}")

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
