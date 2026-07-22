"""
Gera um PDF por produto (com plano de corte cadastrado) usando Playwright.
Salva em: controle-remessa-terceirizacao/Planos de Corte PDF/
"""
import os, re, sqlite3
from playwright.sync_api import sync_playwright

DB      = os.path.join(os.path.dirname(__file__), "controle_remessa.db")
PASTA   = os.path.join(os.path.dirname(__file__), "Planos de Corte PDF")
BASE_URL = "http://localhost:5000"
USUARIO  = "admin"
SENHA    = "1234"

def sanitizar(nome):
    nome = re.sub(r'[\\/:*?"<>|]', '-', nome)
    return nome.strip()[:100]

def buscar_produtos():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT p.id, p.codigo, p.descricao
        FROM produtos p
        JOIN planos_corte pc ON pc.produto_id = p.id
        ORDER BY p.codigo
    """).fetchall()
    con.close()
    return rows

def main():
    os.makedirs(PASTA, exist_ok=True)
    produtos = buscar_produtos()
    print(f"Produtos com plano de corte: {len(produtos)}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()

        # Login
        page.goto(f"{BASE_URL}/login")
        page.fill("input[name='usuario']", USUARIO)
        page.fill("input[name='senha']", SENHA)
        page.click("button[type='submit']")
        page.wait_for_url(f"{BASE_URL}/")
        print("Login OK\n")

        for i, prod in enumerate(produtos, 1):
            url = f"{BASE_URL}/produtos/{prod['id']}/plano-corte"
            page.goto(url)
            page.wait_for_load_state("networkidle")

            # Impede window.print() de abrir diálogo e aciona o desenho do canvas
            page.evaluate("""
                window.print = function(){};
                if (typeof imprimirCompleto === 'function') {
                    imprimirCompleto();
                }
            """)

            # Aguarda o canvas ser desenhado
            page.wait_for_timeout(400)

            nome_arquivo = sanitizar(f"{prod['codigo']} - {prod['descricao']}") + ".pdf"
            caminho = os.path.join(PASTA, nome_arquivo)

            page.pdf(
                path=caminho,
                format="A4",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            )

            print(f"  [{i:>3}/{len(produtos)}] {prod['codigo']} — {prod['descricao']}")

        browser.close()

    print(f"\nConcluido! {len(produtos)} PDFs salvos em:\n{PASTA}")

if __name__ == "__main__":
    main()
