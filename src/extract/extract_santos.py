# src/extract/extract_santos.py
import io
import pandas as pd
from bs4 import BeautifulSoup
from src.config import mappings

def _clean_text_cell(cell):
    if isinstance(cell, str):
        return " | ".join([line.strip() for line in cell.split("<br>") if line.strip()])
    return cell

def parse_santos_tables(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="padrao")
    if not tables: return pd.DataFrame()

    all_data = []
    for table in tables:
        try:
            df = pd.read_html(io.StringIO(str(table)), header=1)[0]
            df = df.astype(str)
            df.columns = (df.columns.str.strip().str.lower()
                .str.replace(r"\s+", "_", regex=True)
                .str.replace(r"[^a-z0-9_]", "", regex=True))
            for col in df.columns:
                df.loc[:, col] = df[col].apply(_clean_text_cell)
            df["tabela_origem"] = "santos"
            all_data.append(df)
        except Exception as e:
            print(f"⚠️ Erro ao processar uma tabela de Santos: {e}")
            continue

    if not all_data: return pd.DataFrame()
        
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Padroniza nomes e tipos antes de entregar
    final_df = final_df.rename(columns=mappings.RAW_TO_STANDARD_COLUMN_MAP)
    if 'tonelagem' in final_df.columns:
        final_df['tonelagem'] = pd.to_numeric(final_df['tonelagem'], errors='coerce')
    if 'data_prevista' in final_df.columns:
        final_df['data_prevista'] = pd.to_datetime(final_df['data_prevista'], dayfirst=True, errors='coerce')

    print(f"📊 {len(final_df)} registros extraídos e padronizados de Santos.")
    return final_df