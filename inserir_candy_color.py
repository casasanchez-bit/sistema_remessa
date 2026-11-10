"""
Importa dados do inventário — Candy Color (REF: verificar com usuário)
Roda no console bash do PythonAnywhere:
  python inserir_candy_color.py

Mapeamento: cor armazena a combinação "Cor Principal c/ Viés"
porque a mesma cor aparece com viés diferentes (ex: V. Musgo c/ Palha
e V. Musgo c/ Vermelho são variantes distintas).
"""
import sqlite3, os, sys

DB = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

# ── Busca o produto pelo código informado na linha de comando
# Uso: python inserir_candy_color.py 12345
# Se não informar, tenta localizar pelo nome
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

# Combinações cor principal c/ viés — cada par é uma variante única
# est_atual: apenas as linhas que tinham número no caderno
dados = [
    # (cor,                          est_atual)
    ("Canela c/ Palha",              10),
    ("Marinho c/ Palha",             50),
    ("V. Musgo c/ Palha",            None),
    ("Marrom c/ Palha",              None),
    ("Cinza c/ Palha",               None),
    ("V. Musgo c/ Vermelho",         None),
    ("Marinho c/ Vermelho",          None),
    ("Vermelho c/ Marinho",          None),
    ("Vermelho c/ V. Musgo",         None),
    ("Palha c/ Marrom",              None),
    ("Palha c/ Cinza",               None),
    ("Palha c/ Canela",              40),
    ("Palha c/ V. Musgo",            20),
    ("Palha c/ Marinho",             10),
    ("Tabaco c/ Palha",              20),
]

inseridos = 0
atualizados = 0
for (cor, est_atual) in dados:
    ex = db.execute(
        "SELECT id FROM inventario_estoque WHERE produto_id=? AND cor=?",
        (pid, cor)
    ).fetchone()
    if ex:
        db.execute(
            "UPDATE inventario_estoque SET est_atual=? WHERE id=?",
            (est_atual, ex["id"])
        )
        atualizados += 1
        print(f"  Atualizado: {cor}")
    else:
        db.execute(
            "INSERT INTO inventario_estoque (produto_id, cor, est_atual) VALUES (?,?,?)",
            (pid, cor, est_atual)
        )
        inseridos += 1
        print(f"  Inserido:  {cor}")

db.commit()
db.close()
print(f"\nConcluído: {inseridos} inseridos, {atualizados} atualizados.")
print("Faça Reload no PythonAnywhere e recarregue a página.")
