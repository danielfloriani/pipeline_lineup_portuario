# src/config/settings.py
from pathlib import Path

# --- Caminhos do Projeto ---
# O resolve() garante que teremos o caminho absoluto (completo)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = PROJECT_ROOT / "data"
BRONZE_PATH = DATA_PATH / "bronze"
SILVER_PATH = DATA_PATH / "silver"
GOLD_PATH = DATA_PATH / "gold"

# --- URLs das Fontes ---
URL_SANTOS = "https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/"
URL_PARANAGUA = "https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo"

# --- Criação dos diretórios (garante que eles existam) ---
BRONZE_PATH.mkdir(parents=True, exist_ok=True)
SILVER_PATH.mkdir(parents=True, exist_ok=True)
GOLD_PATH.mkdir(parents=True, exist_ok=True)
