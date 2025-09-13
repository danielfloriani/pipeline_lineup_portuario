# src/extract/extract_santos.py
"""
Módulo de parsing para os dados do Porto de Santos.
Responsabilidade: Transformar o HTML bruto em um DataFrame limpo.
"""
import io
import pandas as pd
from bs4 import BeautifulSoup

def _clean_text_cell(cell):
    """Limpa o conteúdo de uma célula, removendo <br> e espaços extras."""
    if isinstance(cell, str):
        return " | ".join([line.strip() for line in cell.split("<br>") if line.strip()])
    return cell

# Em src/extract/extract_santos.py

def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Limpeza geral do DataFrame de Santos."""
    # --- PONTO DA CORREÇÃO ---
    # Criamos uma cópia explícita para evitar o SettingWithCopyWarning.
    # Isso garante que estamos trabalhando em um novo DataFrame independente.
    df = df.copy() 

    df = df.dropna(axis=1, how='all')
    
    for col in df.columns:
        if str(col).lower().startswith('unnamed'):
            df = df.drop(columns=col)
    
    df.columns = (
        df.columns.str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
            .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    
    # Usar .loc também é uma boa prática para ser mais explícito
    for col in df.columns:
        df.loc[:, col] = df[col].astype(str).apply(_clean_text_cell)
        
    return df

def parse_santos_tables(html: str) -> pd.DataFrame:
    """
    Extrai todas as tabelas de navios esperados do HTML de Santos 
    e retorna um DataFrame unificado e limpo.
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="padrao")
    
    if not tables:
        print("❌ Nenhuma tabela encontrada no HTML de Santos.")
        return pd.DataFrame()

    all_data = []
    for table in tables:
        try:
            tipo_produto = table.find("th").get_text(strip=True)
            df = pd.read_html(io.StringIO(str(table)), header=1)[0]
            
            # --- PONTO DA CORREÇÃO ---
            # Força todas as colunas a serem do tipo 'string' (object)
            # Isso evita o FutureWarning sobre tipos incompatíveis.
            df = df.astype(str)
            
            df = _clean_dataframe(df) # Agora a limpeza é feita em dados de texto
            df["tipo_produto"] = tipo_produto
            df["tabela_origem"] = "santos"
            all_data.append(df)
        except Exception as e:
            print(f"⚠️ Erro ao processar uma tabela de Santos: {e}")
            continue

    if not all_data:
        print("❌ Nenhuma tabela foi processada com sucesso em Santos.")
        return pd.DataFrame()
        
    final_df = pd.concat(all_data, ignore_index=True)
    print(f"📊 {len(final_df)} registros extraídos e limpos de Santos.")
    return final_df