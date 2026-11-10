"""
Cria o usuário NEIA no sistema.
Roda no console bash do PythonAnywhere — informe a senha como argumento:
  python criar_usuario_neia.py SENHA_AQUI
"""
import sqlite3, os, sys
from werkzeug.security import generate_password_hash
from datetime import date

if len(sys.argv) < 2:
    print("Uso: python criar_usuario_neia.py SENHA_AQUI")
    exit(1)

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

USUARIO = "NEIA"
SENHA   = sys.argv[1]

existing = db.execute("SELECT id FROM usuarios WHERE usuario=?", (USUARIO,)).fetchone()
if existing:
    print(f"Usuário {USUARIO} já existe (id={existing['id']}). Nenhuma alteração feita.")
else:
    db.execute(
        "INSERT INTO usuarios (usuario, senha_hash, criado_em) VALUES (?,?,?)",
        (USUARIO, generate_password_hash(SENHA), date.today().isoformat())
    )
    db.commit()
    print(f"Usuário {USUARIO} criado com sucesso!")

db.close()
