"""
Corrige inventário Candy Color REF: 12792:
  1. Remove linhas antigas no formato "Cor c/ Viés" (duplicatas)
  2. Adiciona 15 linhas de estoque de rolo de viés (lado direito do caderno)

Roda no console bash do PythonAnywhere:
  python corrigir_candy_color.py 12792
"""
import sqlite3, os, sys

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

codigo = sys.argv[1] if len(sys.argv) > 1 else None
if not codigo:
    print("Uso: python corrigir_candy_color.py 12792")
    db.close()
    exit(1)

p = db.execute("SELECT id FROM produtos WHERE codigo=?", (codigo,)).fetchone()
if not p:
    print(f"ERRO: produto {codigo} não encontrado!")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto id={pid}")

# ── 1. Remove linhas antigas no formato "X c/ Y" ──────────────────────────────
removidos = db.execute(
    "DELETE FROM inventario_estoque WHERE produto_id=? AND cor LIKE '% c/ %'",
    (pid,)
).rowcount
db.commit()
print(f"Linhas antigas removidas: {removidos}")

# ── 2. Adiciona linhas de estoque de rolo (lado direito do caderno) ───────────
# cor = nome da cor do viés, est_tecido_pcs = estoque em rolos (vazio por ora)
rolos = [
    "V. Musgo", "Vermelho", "Canela",  "Marrom", "Marinho",
    "Palha",    "Jinho",    "Tabaco",  "Preto",  "Amarelo",
    "V. Malva", "Telha",    "Cinza",   "Rosé",   "Chumbo",
]

inseridos = 0
for cor_rolo in rolos:
    # cor = nome do viés, vies = "ROLO" para distinguir das almofadas prontas
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=? AND vies='ROLO'",
        (pid, cor_rolo)
    ).fetchone()
    if not ex:
        db.execute(
            "INSERT INTO inventario_estoque (produto_id, cor, vies) VALUES (?,?,?)",
            (pid, cor_rolo, "ROLO")
        )
        inseridos += 1
        print(f"  Rolo inserido: {cor_rolo}")
    else:
        print(f"  Rolo já existe: {cor_rolo}")

db.commit()
db.close()
print(f"\nConcluído: {removidos} linhas antigas removidas, {inseridos} rolos inseridos.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
