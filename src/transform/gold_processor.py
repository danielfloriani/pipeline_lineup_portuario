# src/transform/gold_processor.py (versão final com chave robusta)

import pandas as pd
from src.config import settings
from src.config import mappings

def _consolidate_duplicate_columns(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Função auxiliar para checar e consolidar colunas duplicadas."""
    if isinstance(df.get(col_name), pd.DataFrame):
        print(f"Detectadas colunas '{col_name}' duplicadas. Consolidando...")
        consolidated_col = df[col_name].bfill(axis=1).iloc[:, 0]
        df = df.drop(columns=col_name)
        df[col_name] = consolidated_col
    return df

# Em src/transform/gold_processor.py

def _clean_and_standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pega o DataFrame consolidado, DEDUPLICA com chave robusta, limpa, padroniza e converte tipos.
    """
    print("Iniciando limpeza e padronização final dos dados...")
    
    # 1. Renomeia todas as colunas
    df = df.rename(columns=mappings.RAW_TO_STANDARD_COLUMN_MAP)
    
    if 'data_extracao' in df.columns:
        df['data_extracao'] = pd.to_datetime(df['data_extracao'])

    # 2. Consolida colunas duplicadas
    df = _consolidate_duplicate_columns(df, 'navio')
    df = _consolidate_duplicate_columns(df, 'produto')
    df = _consolidate_duplicate_columns(df, 'sentido')
    df = _consolidate_duplicate_columns(df, 'tonelagem')
    df = _consolidate_duplicate_columns(df, 'imo')
    df = _consolidate_duplicate_columns(df, 'viagem')
    df = _consolidate_duplicate_columns(df, 'data_prevista')

    # 3. Deduplicação
    print(f"Registros antes da deduplicação: {len(df)}")
    df = df.sort_values('data_extracao', ascending=True)
    unique_key = ['imo', 'viagem', 'data_prevista', 'produto']
    key_cols_exist = [col for col in unique_key if col in df.columns]
    df = df.drop_duplicates(subset=key_cols_exist, keep='last')
    print(f"Registros após a deduplicação: {len(df)}")

    # 4. Garante o esquema padrão
    standard_cols = ['navio', 'data_prevista', 'produto', 'sentido', 'tonelagem', 'porto']
    df = df[[col for col in standard_cols if col in df.columns]]

    # --- CORREÇÃO FINAL NA LÓGICA DE LIMPEZA ---
    # Converte 'tonelagem' de forma robusta, limpando o texto antes
    # Remove pontos de milhar, troca vírgula por ponto, e extrai apenas os números
    df['tonelagem'] = df['tonelagem'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.').str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Converte 'data_prevista' de forma flexível, aceitando datas com ou sem horas
    df['data_prevista'] = pd.to_datetime(df['data_prevista'], dayfirst=True, errors='coerce')
    # --- FIM DA CORREÇÃO ---

    # 6. Padronização de valores
    if hasattr(mappings, 'SENTIDO_MAP'):
        df['sentido'] = df['sentido'].astype(str).str.upper().map(mappings.SENTIDO_MAP).fillna(df['sentido'])
    
    # 7. Remove linhas com dados essenciais nulos (AGORA DEVE FUNCIONAR)
    df.dropna(subset=['data_prevista', 'tonelagem', 'produto', 'porto'], inplace=True)
    
    print(f"Limpeza concluída. DataFrame padronizado com {len(df)} registros válidos.")
    return df
    
def process_to_gold():
    """
    Orquestra a criação da Camada Ouro: lê a Prata, limpa, agrega e salva.
    """
    print("--- INICIANDO CAMADA OURO ---")
    silver_file_path = settings.SILVER_PATH / "lineup_consolidado.parquet"
    
    if not silver_file_path.exists():
        print(f"❌ Arquivo da Camada Prata não encontrado. Abortando.")
        return

    df_silver = pd.read_parquet(silver_file_path)
    df_clean = _clean_and_standardize_data(df_silver)

    # Verifica se o df_clean não está vazio antes de agrupar
    if df_clean.empty:
        print("⚠️ Nenhum dado válido restante após a limpeza para processar na Camada Ouro.")
        return

    daily_volumes = df_clean.groupby([
        pd.Grouper(key='data_prevista', freq='D'),
        'porto',
        'produto',
        'sentido'
    ]).agg(
        volume_total_ton=('tonelagem', 'sum')
    ).reset_index()

    daily_volumes = daily_volumes.rename(columns={'data_prevista': 'data'})

    output_path = settings.GOLD_PATH / "volumes_diarios.parquet"
    daily_volumes.to_parquet(output_path, index=False)
    
    print(f"✅ Camada Ouro criada com sucesso! {len(daily_volumes)} registros agregados salvos em {output_path}")
    print("--- FINALIZADA CAMADA OURO ---\n")