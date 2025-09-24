# src/transform/gold_processor.py
import pandas as pd
from src.config import settings
from src.config import mappings

def process_to_gold() -> None:
    """Orquestra a criação da Camada Ouro a partir dos dados já pré-limpos da Prata."""
    print("--- INICIANDO CAMADA OURO ---")
    silver_file_path = settings.SILVER_PATH / "lineup_consolidado.parquet"
    
    if not silver_file_path.exists():
        print(f"❌ Arquivo da Camada Prata não encontrado.")
        return

    df = pd.read_parquet(silver_file_path)

    # 1. DEDUPLICAÇÃO
    print(f"Registros antes da deduplicação: {len(df)}")
    df['data_extracao'] = pd.to_datetime(df['data_extracao'])
    df = df.sort_values('data_extracao', ascending=True)
    
    unique_key = ['imo', 'viagem', 'data_prevista', 'produto']
    key_cols_exist = [col for col in unique_key if col in df.columns]
    for col in key_cols_exist:
        df[col] = df[col].astype(str)
        
    df = df.drop_duplicates(subset=key_cols_exist, keep='last')
    print(f"Registros após a deduplicação: {len(df)}")

    # --- PONTO DA CORREÇÃO ---
    # RECONVERTE A COLUNA 'data_prevista' PARA DATETIME APÓS A DEDUPLICAÇÃO
    df['data_prevista'] = pd.to_datetime(df['data_prevista'], errors='coerce')
    # --- FIM DA CORREÇÃO ---

    # 2. PADRONIZAÇÃO DE VALORES
    if hasattr(mappings, 'SENTIDO_MAP'):
        df['sentido'] = df['sentido'].astype(str).str.upper().map(mappings.SENTIDO_MAP).fillna(df['sentido'])

    # 3. FILTRO FINAL DE QUALIDADE
    df.dropna(subset=['data_prevista', 'tonelagem', 'produto', 'porto'], inplace=True)
    print(f"Limpeza final concluída com {len(df)} registros válidos.")

    if df.empty:
        print("⚠️ Nenhum dado válido restante para processar na Camada Ouro.")
        return

    # 4. AGREGAÇÃO
    daily_volumes = df.groupby([
        df['data_prevista'].dt.floor('D'),
        'porto', 'produto', 'sentido'
    ]).agg(volume_total_ton=('tonelagem', 'sum')).reset_index()

    daily_volumes = daily_volumes.rename(columns={'data_prevista': 'data'})

    output_path = settings.GOLD_PATH / "volumes_diarios.parquet"
    daily_volumes.to_parquet(output_path, index=False)
    
    print(f"✅ Camada Ouro criada com sucesso! {len(daily_volumes)} registros agregados salvos.")
    print("--- FINALIZADA CAMADA OURO ---\n")