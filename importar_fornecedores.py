import sqlite3, os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controle_remessa.db")
db = sqlite3.connect(db_path)

fornecedores = [
    ("F001", "EUROTEXTIL",  None,  "FABIANO",              "18997370120"),
    ("F002", "ROZAC",       None,  "CARLINHO",             "16997683585"),
    ("F003", "EDAN",        None,  "CLEBER",               "19999165796"),
    ("F004", "CKS",         None,  "EDSON BELEZA",         "16997109071"),
    ("F005", "CORTTEX",     None,  "VAGUINHO",             "16981346940"),
    ("F006", "ADAR",        None,  "JULIANA",              None),
]

for f in fornecedores:
    try:
        db.execute(
            "INSERT INTO fornecedores (codigo, nome_razao_social, telefone_empresa, nome_representante, telefone_representante) VALUES (?,?,?,?,?)",
            f
        )
        print(f"OK {f[0]} - {f[1]}")
    except Exception as e:
        print(f"IGNORADO {f[0]}: {e}")

db.commit()
db.close()
print("Concluido!")
