"""
Roda no console bash do PythonAnywhere:
  python inserir_donatella.py
"""
import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# 1. Adiciona coluna foto_estampa (ignora se já existe)
try:
    db.execute("ALTER TABLE inventario_estoque ADD COLUMN foto_estampa TEXT")
    db.commit()
    print("Coluna foto_estampa adicionada.")
except Exception as e:
    print(f"Coluna foto_estampa já existe ou erro: {e}")

# 2. Encontra produto 13040
p = db.execute("SELECT id FROM produtos WHERE codigo='13040'").fetchone()
if not p:
    print("ERRO: produto 13040 não encontrado!")
    db.close()
    exit(1)
pid = p["id"]
print(f"Produto 13040 → id={pid}")

# 3. Insere / atualiza os 35 registros
estampas = [
    ("Estampa 4",  "estampa_04.jpg"),
    ("Estampa 5",  "estampa_05.jpg"),
    ("Estampa 6",  "estampa_06.jpg"),
    ("Estampa 8",  "estampa_08.jpg"),
    ("Estampa 9",  "estampa_09.jpg"),
    ("Estampa 10", "estampa_10.jpg"),
    ("Estampa 11", "estampa_11.jpg"),
    ("Estampa 17", "estampa_17.jpg"),
    ("Estampa 18", "estampa_18.jpg"),
    ("Estampa 21", "estampa_21.jpg"),
    ("Estampa 22", "estampa_22.jpg"),
    ("Estampa 23", "estampa_23.jpg"),
    ("Estampa 25", "estampa_25.jpg"),
    ("Estampa 26", "estampa_26.jpg"),
    ("Estampa 27", "estampa_27.jpg"),
    ("Estampa 28", "estampa_28.jpg"),
    ("Estampa 29", "estampa_29.jpg"),
    ("Estampa 30", "estampa_30.jpg"),
    ("Estampa 31", "estampa_31.jpg"),
    ("Estampa 32", "estampa_32.jpg"),
    ("Estampa 35", "estampa_35.jpg"),
    ("Estampa 36", "estampa_36.jpg"),
    ("Estampa 37", "estampa_37.jpg"),
    ("Estampa 38", "estampa_38.jpg"),
    ("Estampa 39", "estampa_39.jpg"),
    ("Estampa 40", "estampa_40.jpg"),
    ("Estampa 41", "estampa_41.jpg"),
    ("Estampa 42", "estampa_42.jpg"),
    ("Estampa 43", "estampa_43.jpg"),
    ("Estampa 44", "estampa_44.jpg"),
    ("Estampa 45", "estampa_45.jpg"),
    ("Estampa 46", "estampa_46.jpg"),
    ("Estampa 47", "estampa_47.jpg"),
    ("Estampa 48", "estampa_48.jpg"),
    ("Estampa 49", "estampa_49.jpg"),
]

inseridos = 0
atualizados = 0
for cor, foto in estampas:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute("UPDATE inventario_estoque SET foto_estampa=? WHERE id=?", (foto, ex["id"]))
        atualizados += 1
    else:
        db.execute(
            "INSERT INTO inventario_estoque (produto_id, cor, foto_estampa) VALUES (?,?,?)",
            (pid, cor, foto)
        )
        inseridos += 1

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
