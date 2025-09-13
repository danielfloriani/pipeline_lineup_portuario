# pipeline.py
"""
Orquestrador principal do pipeline de dados de lineup de navios.
Executa as três camadas da arquitetura Medallion: Bronze, Prata e Ouro.
"""
import pandas as pd
from src.config import settings
from src.common import utils
from src.extract import extract_santos, extract_paranagua
from src.transform import gold_processor # <--- Importe o processador Ouro
def run_bronze():
    """
    Camada Bronze: Coleta os dados brutos (HTML) das fontes e salva localmente.
    """
    print("--- INICIANDO CAMADA BRONZE ---")
    # Busca e salva Santos
    santos_html = utils.fetch_page(settings.URL_SANTOS)
    if santos_html:
        utils.save_raw_html(santos_html, "santos")

    # Busca e salva Paranaguá
    paranagua_html = utils.fetch_page(settings.URL_PARANAGUA)
    if paranagua_html:
        utils.save_raw_html(paranagua_html, "paranagua")
    print("--- FINALIZADA CAMADA BRONZE ---\n")

def run_silver():
    """
    Camada Prata: Lê os dados brutos, aplica parsing, limpeza, padronização
    e salva os dados consolidados em formato Parquet.
    """
    print("--- INICIANDO CAMADA PRATA ---")
    processed_dfs = []
    
    bronze_files = list(settings.BRONZE_PATH.glob("*.html"))
    for file_path in bronze_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        if "santos" in file_path.name:
            df = extract_santos.parse_santos_tables(html_content)
        elif "paranagua" in file_path.name:
            df = extract_paranagua.parse_paranagua_table(html_content)
        else:
            continue
        
        if not df.empty:
            processed_dfs.append(df)
    
    if not processed_dfs:
        print("❌ Nenhum dado para processar na camada Prata. Encerrando.")
        return

    # Unifica os DataFrames
    silver_df = pd.concat(processed_dfs, ignore_index=True)
    
    output_path = settings.SILVER_PATH / "lineup_consolidado.parquet"
    silver_df.to_parquet(output_path, index=False)
    
    print(f"💾 Camada Prata salva com {len(silver_df)} registros em: {output_path}")
    print("--- FINALIZADA CAMADA PRATA ---\n")

def run_gold():
    # Agora a função chama a lógica real
    gold_processor.process_to_gold()


if __name__ == "__main__":
    run_bronze()
    run_silver()
    run_gold()
    print(">>> PIPELINE CONCLUÍDO <<<")