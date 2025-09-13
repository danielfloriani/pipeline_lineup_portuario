# src/extract/extract_paranagua.py
"""
Módulo de parsing para os dados do Porto de Paranaguá.
Responsabilidade: Transformar o HTML bruto em um DataFrame limpo,
tratando corretamente as células mescladas (rowspan).
"""
import pandas as pd
from bs4 import BeautifulSoup

def _clean_text_cell(cell_text: str) -> str:
    """Remove quebras de linha, espaços extras e normaliza o texto da célula."""
    if isinstance(cell_text, str):
        text = cell_text.replace("\n", " ").replace("\r", " ").strip()
        return text
    return str(cell_text)

def parse_paranagua_table(html: str) -> pd.DataFrame:
    """
    Extrai a tabela 'Esperados' do HTML de Paranaguá, tratando rowspan,
    e retorna um DataFrame unificado e limpo.
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table", class_="table table-bordered table-striped table-hover")

    target_table = None
    for table in tables:
        th = table.find("th", colspan=True)
        if th and "ESPERADOS" in th.get_text(strip=True).upper():
            target_table = table
            break

    if target_table is None:
        print("❌ Tabela 'Esperados' não encontrada no HTML de Paranaguá.")
        return pd.DataFrame()

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
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
    df["tabela_origem"] = "paranagua"
    
    print(f"📊 {len(df)} registros extraídos e limpos de Paranaguá.")
    return df


if __name__ == '__main__':
    print("🧪 INICIANDO TESTE INDIVIDUAL DO SCRIPT DE PARANAGUÁ...")
    
    from src.common import utils
    from src.config import settings

    html_content = utils.fetch_page(settings.URL_PARANAGUA)

    if html_content:
        print("\nHTML baixado. Testando a função de parsing...")
        df_resultado = parse_paranagua_table(html_content)

        if not df_resultado.empty:
            print("\n✅ Parsing concluído com sucesso!")
            print("Informações do DataFrame extraído:")
            df_resultado.info()
            print("\nPrimeiras 5 linhas do resultado:")
            print(df_resultado.head())
        else:
            print("\n❌ A função de parsing não retornou dados.")
    else:
        print("\n❌ Falha ao baixar o HTML. Não foi possível testar o parsing.")
        
    print("\n🏁 TESTE INDIVIDUAL FINALIZADO.")