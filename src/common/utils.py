# src/common/utils.py
from datetime import date
import requests
import certifi
from src.config import settings

def fetch_page(url: str) -> str | None:
    """
    Faz o download do HTML da página informada, com fallback para SSL.
    Retorna o HTML como string ou None em caso de erro.
    """
    try:
        response = requests.get(url, verify=certifi.where(), timeout=20)
        response.raise_for_status()
        print(f"✅ Página carregada com sucesso de: {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        # Tenta novamente ignorando SSL
        print(f"⚠️ Problema de conexão ({e}). Tentando novamente sem verificação SSL...")
        try:
            response = requests.get(url, verify=False, timeout=20)
            response.raise_for_status()
            print(f"✅ Página carregada com sucesso de: {url} (sem verificação SSL)")
            return response.text
        except requests.exceptions.RequestException as final_e:
            print(f"❌ Falha ao carregar a página de {url} após duas tentativas: {final_e}")
            return None

def save_raw_html(html_content: str, port_name: str):
    """
    Salva o conteúdo HTML bruto na camada Bronze.
    Este é o dado mais puro, garantindo rastreabilidade.
    """
    if not html_content:
        print(f"Nenhum conteúdo HTML para salvar para o porto {port_name}.")
        return

    today = date.today().isoformat()
    file_path = settings.BRONZE_PATH / f"lineup_{port_name}_{today}.html"

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"💾 HTML Bruto salvo na Camada Bronze em: {file_path}")
    except IOError as e:
        print(f"❌ Erro ao salvar arquivo para {port_name}: {e}")