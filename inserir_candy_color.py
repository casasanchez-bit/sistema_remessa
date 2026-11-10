"""
Importa dados do inventário — Candy Color REF: 12792
Roda no console bash do PythonAnywhere:
  python inserir_candy_color.py 12792

Cor e Viés ficam em colunas separadas (exige migração de constraint já aplicada).
"""
import sqlite3, os, sys

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

codigo = sys.argv[1] if len(sys.argv) > 1 else None
if codigo:
    p = db.execute("SELECT id FROM produtos WHERE codigo=?", (codigo,)).fetchone()
else:
    p = db.execute(
        "SELECT id FROM produtos WHERE descricao LIKE '%CANDY%COLOR%' COLLATE NOCASE"
    ).fetchone()

if not p:
    print("ERRO: produto Candy Color não encontrado!")
    print("Informe o código: python inserir_candy_color.py <CODIGO>")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto Candy Color → id={pid}")

# Garante que a coluna vies existe (pode não estar no banco antes do Reload)
try:
    db.execute("ALTER TABLE inventario_estoque ADD COLUMN vies TEXT")
    db.commit()
    print("Coluna 'vies' adicionada ao banco.")
except Exception:
    pass  # já existe

# (cor principal, viés, est_atual)
dados = [
    ("Canela",    "Palha",    10),
    ("Marinho",   "Palha",    50),
    ("V. Musgo",  "Palha",    None),
    ("Marrom",    "Palha",    None),
    ("Cinza",     "Palha",    None),
    ("V. Musgo",  "Vermelho", None),
    ("Marinho",   "Vermelho", None),
    ("Vermelho",  "Marinho",  None),
    ("Vermelho",  "V. Musgo", None),
    ("Palha",     "Marrom",   None),
    ("Palha",     "Cinza",    None),
    ("Palha",     "Canela",   40),
    ("Palha",     "V. Musgo", 20),
    ("Palha",     "Marinho",  10),
    ("Tabaco",    "Palha",    20),
]

inseridos = 0
atualizados = 0
for (cor, vies, est_atual) in dados:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=? AND (vies=? OR (vies IS NULL AND ? IS NULL))",
        (pid, cor, vies, vies)
    ).fetchone()
    if ex:
        db.execute(
            "UPDATE inventario_estoque SET est_atual=?, vies=? WHERE id=?",
            (est_atual, vies, ex["id"])
        )
        atualizados += 1
        print(f"  Atualizado: {cor} / {vies}")
    else:
        db.execute(
            "INSERT INTO inventario_estoque (produto_id, cor, vies, est_atual) VALUES (?,?,?,?)",
            (pid, cor, vies, est_atual)
        )
        inseridos += 1
        print(f"  Inserido:  {cor} / {vies}")

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
