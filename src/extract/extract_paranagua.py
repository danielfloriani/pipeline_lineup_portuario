# src/extract/extract_paranagua.py
import pandas as pd
from bs4 import BeautifulSoup
from src.config import mappings

def _clean_text_cell(cell_text: str) -> str:
    if isinstance(cell_text, str):
        return cell_text.replace("\n", " ").replace("\r", " ").strip()
    return str(cell_text)

def _converter_tonelagem_paranagua(valor):
    if not isinstance(valor, str): return None
    if 'movs' in valor.lower(): return None
    numero_limpo = valor.lower().replace('tons.', '').replace('.', '').replace(',', '.').strip()
    return pd.to_numeric(numero_limpo, errors='coerce')

def parse_paranagua_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="table table-bordered table-striped table-hover")
    target_table = None
    for table in tables:
        th = table.find("th", colspan=True)
        if th and "ESPERADOS" in th.get_text(strip=True).upper():
            target_table = table
            break
    if target_table is None: return pd.DataFrame()
    header_row = target_table.find_all("thead")[0].find_all("tr")[1]
    headers = [_clean_text_cell(th.get_text()) for th in header_row.find_all("th")]
    tbody = target_table.find("tbody")
    rows = tbody.find_all("tr")
    data = []
    rowspan_map = {}
    for row in rows:
        row_data = []
        cols = row.find_all(["td", "th"])
        col_idx = 0
        while col_idx < len(headers):
            if col_idx in rowspan_map and rowspan_map[col_idx][1] > 0:
                row_data.append(rowspan_map[col_idx][0])
                rowspan_map[col_idx][1] -= 1
                col_idx += 1
                continue
            if not cols:
                row_data.append("")
                col_idx += 1
                continue
            cell = cols.pop(0)
            text = _clean_text_cell(cell.get_text())
            row_data.append(text)
            rowspan_val = cell.get("rowspan")
            if rowspan_val and int(rowspan_val) > 1:
                rowspan_map[col_idx] = [text, int(rowspan_val) - 1]
            col_idx += 1
        data.append(row_data)
    
    df = pd.DataFrame(data, columns=headers)
    
    # Padroniza nomes e tipos antes de entregar
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
    df = df.rename(columns=mappings.RAW_TO_STANDARD_COLUMN_MAP)
    
    if 'tonelagem' in df.columns:
        df['tonelagem'] = df['tonelagem'].apply(_converter_tonelagem_paranagua)
    if 'data_prevista' in df.columns:
        df['data_prevista'] = pd.to_datetime(df['data_prevista'], dayfirst=True, errors='coerce')
    
    df["porto"] = "paranagua"
    
    print(f"📊 {len(df)} registros extraídos e padronizados de Paranaguá.")
    return df