# src/validation/validate_silver.py (versão final)
import pandas as pd
import pandera.pandas as pa
from pandera.errors import SchemaError
from src.config import settings

# Esquema corrigido para usar 'embarcação' em vez de 'navio'
consolidated_silver_schema = pa.DataFrameSchema(
    columns={
        "navio_ship": pa.Column(str, required=False, nullable=True),
        "embarcação": pa.Column(str, required=False, nullable=True), # <-- CORREÇÃO
        "tabela_origem": pa.Column(str, pa.Check.isin(["santos", "paranagua"])),
    },
    checks=[
        # A verificação agora usa o nome correto da coluna
        pa.Check(
            lambda df: df["embarcação"].notna() | df["navio_ship"].notna(), # <-- CORREÇÃO
            name="pelo_menos_um_navio_nao_nulo"
        )
    ],
    strict=False,
    coerce=True
)

def run_validation():
    print("--- 🔎 INICIANDO VALIDAÇÃO DO ARQUIVO silver/lineup_consolidado.parquet ---")
    
    silver_file = settings.SILVER_PATH / "lineup_consolidado.parquet"

    if not silver_file.exists():
        print(f"❌ ERRO: Arquivo não encontrado.")
        return

    try:
        df_to_validate = pd.read_parquet(silver_file)
        print(f"Arquivo carregado com {len(df_to_validate)} linhas.")
        
        consolidated_silver_schema.validate(df_to_validate)
        
        print("✅ SUCESSO! O arquivo da Camada Prata passou na validação.")

    except SchemaError as e:
        print("❌ FALHA NA VALIDAÇÃO! O arquivo da Camada Prata está inconsistente.")
        print("\n--- DETALHES DO ERRO ---")
        print(e.failure_cases)
    except KeyError as e:
        print(f"❌ ERRO DE CHAVE: Uma coluna esperada no esquema não foi encontrada no DataFrame: {e}")
    except Exception as e:
        print(f"❌ Um erro inesperado ocorreu: {e}")

if __name__ == '__main__':
    run_validation()