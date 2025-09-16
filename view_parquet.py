# view_parquet.py
import pandas as pd
from src.config import settings

# --- Configurações do Pandas ---
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', None)

def main():
    """
    Função principal que orquestra a visualização do arquivo Parquet.
    """
    # --- SELEÇÃO INTERATIVA DA CAMADA ---
    camada_escolhida = ""
    while camada_escolhida not in ['gold', 'silver']:
        camada_escolhida = input("Qual camada você deseja visualizar? (gold ou silver): ").lower().strip()
        if camada_escolhida not in ['gold', 'silver']:
            print("Opção inválida. Por favor, digite 'gold' ou 'silver'.")

    # Define o nome do arquivo com base na camada escolhida
    if camada_escolhida == 'gold':
        nome_do_arquivo = "volumes_diarios.parquet"
    else: # silver
        nome_do_arquivo = "lineup_consolidado.parquet"

    caminho_arquivo = settings.DATA_PATH / camada_escolhida / nome_do_arquivo

    try:
        df = pd.read_parquet(caminho_arquivo)
        print(f"\n--- Visualizando o arquivo: {caminho_arquivo} ---")
        print(f"O arquivo tem {len(df)} linhas e {len(df.columns)} colunas no total.\n")

        df_trabalho = df.copy()
        coluna_porto = 'porto' if 'porto' in df.columns else 'tabela_origem'

        # Filtro de Porto
        filtro_porto_input = input("Você gostaria de filtrar por um porto? (s/n): ").lower().strip()
        if 's' in filtro_porto_input:
            porto_alvo = input("Digite o nome do porto (santos ou paranagua): ").lower().strip()
            if porto_alvo in ['santos', 'paranagua']:
                df_trabalho = df_trabalho[df_trabalho[coluna_porto] == porto_alvo]
                print(f"Filtrando por '{porto_alvo}'. {len(df_trabalho)} registros encontrados.")

        # Filtro de Produto
        filtro_produto_input = input("\nVocê gostaria de filtrar por um produto? (s/n): ").lower().strip()
        if 's' in filtro_produto_input:
            produto_alvo = input("Digite o nome do produto: ").strip()
            
            coluna_busca = 'produto'
            if camada_escolhida == 'silver' and 'mercadoria_goods' in df_trabalho.columns:
                df_trabalho['produto_busca'] = df_trabalho['mercadoria_goods'].fillna(df_trabalho.get('mercadoria', ''))
                coluna_busca = 'produto_busca'
            
            df_trabalho = df_trabalho[df_trabalho[coluna_busca].str.contains(produto_alvo, case=False, na=False)]
            print(f"\n--- Exibindo {len(df_trabalho)} registros para o produto '{produto_alvo}' ---")
        
        # Exibe o resultado final
        if 's' in filtro_porto_input or 's' in filtro_produto_input:
             print(df_trabalho)
        else: 
            if camada_escolhida == 'silver':
                print("\n--- Visualização Estratégica da Camada Silver ---")
                colunas_estrategicas = [
                    'tabela_origem', 'navio_ship', 'embarcação', 'mercadoria_goods', 'mercadoria',
                    'imo', 'viagem_voyage', 'viagem', 'chegarrival_dmy', 'eta',
                    'peso_weight', 'previsto', 'opera_operat', 'operacao', 'sentido',
                    'data_extracao'
                ]
                colunas_para_mostrar = [col for col in colunas_estrategicas if col in df.columns]
                df_visualizacao = df[colunas_para_mostrar]
                df_visualizacao.info(verbose=False)
                print("\n--- Conteúdo (Colunas Estratégicas) ---")
                print(df_visualizacao)
            else: # gold
                df.info()
                print("\n--- Conteúdo Completo do Arquivo ---")
                print(df)

    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo não encontrado em '{caminho_arquivo}'.")
    except Exception as e:
        print(f"❌ Um erro inesperado ocorreu: {e}")

if __name__ == '__main__':
    main()