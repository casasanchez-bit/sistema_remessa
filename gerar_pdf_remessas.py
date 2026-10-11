"""
Gera relatorio de remessas em PDF e salva em static/relatorio_remessas.pdf
Rodar no PythonAnywhere: python gerar_pdf_remessas.py
Depois acessar: /static/relatorio_remessas.pdf
"""
import sqlite3, os
from datetime import date

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import mm
except ImportError:
    print("Instalando reportlab...")
    os.system("pip install reportlab")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import mm

BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, "controle_remessa.db")
OUT  = os.path.join(BASE, "static", "relatorio_remessas.pdf")

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

remessas = db.execute("""
    SELECT r.numero, r.data_envio, t.nome AS terceirizado,
           COUNT(ir.id) AS qtd_itens,
           SUM(ir.qtd_enviada) AS total_pecas
    FROM remessas r
    JOIN terceirizados t ON t.id = r.terceirizado_id
    LEFT JOIN itens_remessa ir ON ir.remessa_id = r.id
    GROUP BY r.id
    ORDER BY r.numero DESC
    LIMIT 50
""").fetchall()

doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=15*mm, bottomMargin=15*mm)

styles = getSampleStyleSheet()
titulo_style = ParagraphStyle('t', parent=styles['Title'],
    fontSize=16, textColor=colors.HexColor('#5C442C'), spaceAfter=4)
sub_style = ParagraphStyle('s', parent=styles['Normal'],
    fontSize=9, textColor=colors.grey, spaceAfter=10)

story = []
story.append(Paragraph("CASA SANCHEZ — Relatório de Remessas", titulo_style))
story.append(Paragraph(
    f"Emitido em {date.today().strftime('%d/%m/%Y')} · Últimas {len(remessas)} remessas (banco de produção)",
    sub_style))

dados = [["Nº", "Data Envio", "Terceirizado", "Itens", "Peças"]]
for r in remessas:
    d = r["data_envio"] or ""
    if len(d) == 10:
        d = f"{d[8:10]}/{d[5:7]}/{d[:4]}"
    dados.append([
        str(r["numero"]),
        d or "—",
        r["terceirizado"],
        str(r["qtd_itens"] or 0),
        str(int(r["total_pecas"] or 0)),
    ])

tabela = Table(dados, colWidths=[15*mm, 28*mm, 95*mm, 18*mm, 18*mm])
tabela.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#AF4005')),
    ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 8),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.HexColor('#FDF3EC')]),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#D9C6B3')),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))

story.append(tabela)
story.append(Spacer(1, 6*mm))
story.append(Paragraph(f"Total: {len(remessas)} remessas listadas.", sub_style))
doc.build(story)
print(f"PDF gerado em: {OUT}")
print(f"Acesse em: https://casasanchez.pythonanywhere.com/static/relatorio_remessas.pdf")
