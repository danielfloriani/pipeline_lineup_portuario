# src/config/mappings.py
SENTIDO_MAP = {
    "DESCARGA": "Importação", "DESC": "Importação",
    "IMPORTACAO": "Importação", "IMP": "Importação",
    "CARGA": "Exportação", "EMB": "Exportação",
    "EXPORTACAO": "Exportação", "EXP": "Exportação",
    "EMB DESC": "Misto", "IMP/EXP": "Misto",
}

# Mapeamento dos nomes brutos para o nosso esquema padrão
RAW_TO_STANDARD_COLUMN_MAP = {
    # Santos (nomes brutos já em snake_case)
    'navio_ship': 'navio', 'chegarrival_dmy': 'data_prevista',
    'mercadoria_goods': 'produto', 'opera_operat': 'sentido',
    'peso_weight': 'tonelagem', 'viagem_voyage': 'viagem',
    'agncia_office': 'agencia',
    
    # Paranaguá (nomes brutos)
    'embarcação': 'navio', 'eta': 'data_prevista',
    'mercadoria': 'produto', 'operacao': 'sentido',
    'previsto': 'tonelagem', 'agência': 'agencia',

    # Comuns
    'imo': 'imo', 'tabela_origem': 'porto',
}