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

# Garante coluna vies e migra constraint para UNIQUE(produto_id, cor, vies)
try:
    db.execute("ALTER TABLE inventario_estoque ADD COLUMN vies TEXT")
    db.commit()
    print("Coluna 'vies' adicionada ao banco.")
except Exception:
    pass  # já existe

try:
    schema_row = db.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='inventario_estoque'"
    ).fetchone()
    schema_sql = schema_row[0] if schema_row else ''
    if 'UNIQUE(produto_id, cor)' in schema_sql and 'UNIQUE(produto_id, cor, vies)' not in schema_sql:
        print("Migrando constraint única para incluir viés...")
        db.execute("""CREATE TABLE inventario_estoque_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL REFERENCES produtos(id) ON DELETE CASCADE,
            cor TEXT NOT NULL,
            vies TEXT,
            est_atual INTEGER,
            est_min INTEGER,
            est_max INTEGER,
            costureira_1 TEXT,
            costureira_2 TEXT,
            cortado TEXT,
            est_tecido_pcs TEXT,
            ref_fornecedor TEXT,
            fornecedor TEXT,
            foto_estampa TEXT,
            UNIQUE(produto_id, cor, vies)
        )""")
        db.execute("""INSERT OR IGNORE INTO inventario_estoque_v2
            SELECT id, produto_id, cor, vies, est_atual, est_min, est_max,
                   costureira_1, costureira_2, cortado, est_tecido_pcs,
                   ref_fornecedor, fornecedor, foto_estampa
            FROM inventario_estoque""")
        db.execute("DROP TABLE inventario_estoque")
        db.execute("ALTER TABLE inventario_estoque_v2 RENAME TO inventario_estoque")
        db.commit()
        print("Constraint migrada com sucesso.")
except Exception as e:
    print(f"AVISO na migração de constraint: {e}")

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
