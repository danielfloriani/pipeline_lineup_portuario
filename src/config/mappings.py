# src/config/mappings.py

# Mapeamento para padronizar a coluna 'sentido' (operação)
SENTIDO_MAP = {
    "DESCARGA": "Importação",
    "CARGA": "Exportação",
    "IMPORTACAO": "Importação",
    "EXPORTACAO": "Exportação",
    "IMP": "Importação",
    "EXP": "Exportação",
    # Adicione outras variações que encontrar nos dados
}


# Mapeamento para padronizar os nomes das colunas das fontes brutas para o nosso esquema padrão
RAW_TO_STANDARD_COLUMN_MAP = {
    # Colunas de Santos
    'navio_ship': 'navio',
    'chegarrival_dmy': 'data_prevista',
    'mercadoria_goods': 'produto',
    'opera_operat': 'sentido',
    'peso_weight': 'tonelagem',
    'tabela_origem': 'porto',
    # Colunas de Paranaguá
    'embarcação': 'navio',
    'chegada': 'data_prevista',
    'mercadoria': 'produto',
    'operacao': 'sentido',
    'ton': 'tonelagem',
}