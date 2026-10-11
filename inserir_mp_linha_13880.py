import sqlite3, os

db_path = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row

# Produto 13880 -> id
produto = db.execute("SELECT id FROM produtos WHERE codigo = '13880'").fetchone()
if not produto:
    print("ERRO: produto codigo 13880 nao encontrado.")
    exit(1)
produto_id = produto["id"]

# Materia-prima LINHA DE ALGODAO -> id
mp = db.execute("SELECT id, descricao FROM materias_primas WHERE codigo = '10314'").fetchone()
if not mp:
    print("ERRO: materia-prima codigo 10314 (LINHA DE ALGODAO) nao encontrada.")
    exit(1)
mp_id = mp["id"]

# Verificar se ja existe
existe = db.execute(
    "SELECT id FROM produto_composicao WHERE produto_id=? AND materia_prima_id=?",
    (produto_id, mp_id)
).fetchone()

if existe:
    print(f"Vinculo ja existe (id={existe['id']}). Nenhuma alteracao feita.")
else:
    db.execute(
        "INSERT INTO produto_composicao (produto_id, materia_prima_id, quantidade) VALUES (?, ?, NULL)",
        (produto_id, mp_id)
    )
    db.commit()
    print(f"OK: LINHA DE ALGODAO ({mp['descricao']}) vinculada ao produto 13880 (produto_id={produto_id}).")
