"""Backup diário do banco de dados — pensado para rodar via Scheduled Task do PythonAnywhere.

Copia controle_remessa.db para backups/ com timestamp e remove backups com
mais de 30 dias, para não estourar a cota de disco.
"""
from datetime import datetime, timedelta
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "controle_remessa.db"
BACKUP_DIR = BASE_DIR / "backups"
DIAS_RETENCAO = 30

BACKUP_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
destino = BACKUP_DIR / f"controle_remessa_{timestamp}.db"
shutil.copy2(DB_PATH, destino)
print(f"Backup criado: {destino.name}")

limite = datetime.now() - timedelta(days=DIAS_RETENCAO)
removidos = 0
for arquivo in BACKUP_DIR.glob("controle_remessa_*.db"):
    if datetime.fromtimestamp(arquivo.stat().st_mtime) < limite:
        arquivo.unlink()
        removidos += 1
if removidos:
    print(f"{removidos} backup(s) antigo(s) removido(s) (mais de {DIAS_RETENCAO} dias).")
