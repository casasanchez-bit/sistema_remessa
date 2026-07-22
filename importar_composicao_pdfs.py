"""
Importa composição de matérias-primas a partir dos PDFs da pasta 'Restantes'.
Cada PDF tem o código do produto como nome do arquivo (ex: 36.pdf).
"""
import re
import os
import sqlite3
import pdfplumber

PASTA_PDFS = os.path.join(os.path.dirname(__file__),
                          "Composição dos Produtos", "Restantes")
DB_PATH    = os.path.join(os.path.dirname(__file__), "controle_remessa.db")

# Regex: inicio da linha = código numérico, depois descrição, depois "| -" ou "|-", depois 3 números
RE_ITEM = re.compile(
    r'^(\d+)\s+(.+?)\s*\|[\s\-]+\s*([\d,]+)\s+[\d,]+\s+[\d,]+\s*$'
)

def extrair_composicao(pdf_path):
    """Retorna lista de (mp_codigo, mp_descricao, quantidade) do PDF."""
    itens = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text() or ""
            for linha in texto.splitlines():
                m = RE_ITEM.match(linha.strip())
                if m:
                    mp_codigo   = m.group(1).strip()
                    mp_descricao = m.group(2).strip()
                    qtd_str     = m.group(3).replace(",", ".")
                    try:
                        quantidade = float(qtd_str)
                    except ValueError:
                        continue
                    itens.append((mp_codigo, mp_descricao, quantidade))
    return itens


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    pdfs = sorted(f for f in os.listdir(PASTA_PDFS) if f.lower().endswith(".pdf"))
    print(f"PDFs encontrados: {len(pdfs)}\n")

    ok_total = skip_total = err_total = 0
    nao_encontrados = []

    for arquivo in pdfs:
        produto_codigo = os.path.splitext(arquivo)[0]
        pdf_path = os.path.join(PASTA_PDFS, arquivo)

        prod = db.execute(
            "SELECT id FROM produtos WHERE codigo = ?", (produto_codigo,)
        ).fetchone()
        if not prod:
            nao_encontrados.append(produto_codigo)
            err_total += 1
            continue

        produto_id = prod["id"]
        itens = extrair_composicao(pdf_path)

        if not itens:
            print(f"  [AVISO] {arquivo}: nenhum item extraído")
            continue

        ok = skip = 0
        for mp_codigo, mp_descricao, quantidade in itens:
            db.execute(
                "INSERT OR IGNORE INTO materias_primas (codigo, descricao) VALUES (?, ?)",
                (mp_codigo, mp_descricao)
            )
            mp = db.execute(
                "SELECT id FROM materias_primas WHERE codigo = ?", (mp_codigo,)
            ).fetchone()
            try:
                db.execute(
                    "INSERT INTO produto_composicao (produto_id, materia_prima_id, quantidade) "
                    "VALUES (?, ?, ?)",
                    (produto_id, mp["id"], quantidade)
                )
                ok += 1
            except sqlite3.IntegrityError:
                db.execute(
                    "UPDATE produto_composicao SET quantidade = ? "
                    "WHERE produto_id = ? AND materia_prima_id = ?",
                    (quantidade, produto_id, mp["id"])
                )
                skip += 1

        print(f"  {arquivo}: {ok} inserido(s), {skip} atualizado(s)")
        ok_total   += ok
        skip_total += skip

    conn.commit()
    conn.close()

    print(f"\n{'='*50}")
    print(f"RESULTADO FINAL")
    print(f"  Matérias-primas inseridas : {ok_total}")
    print(f"  Já existiam (atualizadas) : {skip_total}")
    print(f"  Produtos não encontrados  : {err_total}")
    if nao_encontrados:
        print(f"  Códigos não encontrados   : {', '.join(nao_encontrados)}")
    print("Importação concluída.")


if __name__ == "__main__":
    main()
