# pipeline.py
"""
Orquestrador principal do pipeline de dados de lineup de navios.
Executa as três camadas da arquitetura Medallion: Bronze, Prata e Ouro.
"""
import pandas as pd
import re
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
    Camada Prata: Encontra o arquivo mais recente de cada porto na Camada Bronze,
    processa-os, adiciona a data de extração e salva os dados consolidados.
    """
    print("--- INICIANDO CAMADA PRATA ---")
    
    # Encontra todos os arquivos da camada bronze
    all_bronze_files = list(settings.BRONZE_PATH.glob("*.html"))
    
    # Separa os arquivos por porto
    santos_files = [f for f in all_bronze_files if "santos" in f.name]
    paranagua_files = [f for f in all_bronze_files if "paranagua" in f.name]

    # Encontra o arquivo MAIS RECENTE de cada porto
    latest_files_to_process = []
    if santos_files:
        latest_files_to_process.append(max(santos_files, key=lambda f: f.stat().st_ctime))
    if paranagua_files:
        latest_files_to_process.append(max(paranagua_files, key=lambda f: f.stat().st_ctime))

    if not latest_files_to_process:
        print("❌ Nenhum arquivo encontrado na camada Bronze para processar.")
        return

    print("Processando os seguintes arquivos (os mais recentes de cada porto):")
    for f in latest_files_to_process:
        print(f" - {f.name}")

    processed_dfs = []
    for file_path in latest_files_to_process:
        # ... (o resto da lógica de ler o arquivo e o parser continua a mesma) ...
        # A lógica de adicionar a 'data_extracao' ainda é útil para rastreabilidade
        match = re.search(r'(\d{4}-\d{2}-\d{2})', str(file_path.name))
        if not match: continue
        data_extracao = match.group(1)

        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        if "santos" in file_path.name:
            df = extract_santos.parse_santos_tables(html_content)
        elif "paranagua" in file_path.name:
            df = extract_paranagua.parse_paranagua_table(html_content)
        
        if not df.empty:
            df['data_extracao'] = pd.to_datetime(data_extracao)
            processed_dfs.append(df)
    
    if not processed_dfs:
        print("❌ Nenhum dado para processar na camada Prata. Encerrando.")
        return

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