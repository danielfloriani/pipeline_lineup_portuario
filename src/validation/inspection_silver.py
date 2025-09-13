# inspecao_silver.py
import pandas as pd
from src.config import settings

# --- Configurações do Pandas para melhor visualização no terminal ---
pd.set_option('display.max_rows', 100)      # Mostrar até 100 linhas
pd.set_option('display.max_columns', 50)     # Mostrar até 50 colunas
pd.set_option('display.width', 250)        # Usar mais largura do terminal
pd.set_option('display.max_colwidth', 50)  # Mostrar mais texto dentro de cada célula

# Carrega o resultado da sua camada Prata
try:
    df_silver = pd.read_parquet(settings.SILVER_PATH / "lineup_consolidado.parquet")
    print("✅ Arquivo 'lineup_consolidado.parquet' carregado com sucesso!")
    print(f"Total de registros: {len(df_silver)}\n")
except FileNotFoundError:
    print("❌ Arquivo 'lineup_consolidado.parquet' não encontrado. Rode o pipeline.py primeiro.")
    exit()

# --- INÍCIO DA NOSSA INVESTIGAÇÃO ---

# 1. Visão Geral: Vamos ver as colunas e as primeiras linhas de cada fonte
print("--- Visão Geral do DataFrame Consolidado ---")
print("Colunas disponíveis:", df_silver.columns.to_list())
print("\nPrimeiras 5 linhas (geralmente de Paranaguá):")
print(df_silver.head())
print("\nÚltimas 5 linhas (geralmente de Santos):")
print(df_silver.tail())
print("-" * 50)


# 2. Verificando a união das fontes
print("\n--- Verificação da Consolidação ---")
print("Contagem de registros por porto de origem:")
print(df_silver['tabela_origem'].value_counts())
print("-" * 50)


# 3. Investigação Específica (Spot Check)
#    Abra os sites e substitua os nomes abaixo pelos navios que você está vendo AGORA.
#    Isto é apenas um exemplo.
print("\n--- Investigação Específica (Spot Check) ---")

# Exemplo para um navio de Paranaguá
# (Pegue um navio do site com várias mercadorias para testar o 'rowspan')
navio_paranagua_exemplo = 'STAR KINN' # <--- SUBSTITUA PELO NOME DE UM NAVIO REAL DO SITE
print(f"\nBuscando dados para o navio de Paranaguá: '{navio_paranagua_exemplo}'")
print(df_silver[df_silver['embarcação'] == navio_paranagua_exemplo])

# Exemplo para um navio de Santos
navio_santos_exemplo = 'MSC ADELAIDE' # <--- SUBSTITUA PELO NOME DE UM NAVIO REAL DO SITE
print(f"\nBuscando dados para o navio de Santos: '{navio_santos_exemplo}'")
print(df_silver[df_silver['navio_ship'] == navio_santos_exemplo])
print("-" * 50)