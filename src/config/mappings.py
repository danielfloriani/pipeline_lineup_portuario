# src/config/mappings.py

# Mapeamento para padronizar a coluna 'sentido' (operação)
# Em src/config/mappings.py

# Em src/config/mappings.py

SENTIDO_MAP = {
    # Variações de Importação
    "DESCARGA": "Importação",
    "DESC": "Importação",      # <-- ADICIONE ESTA LINHA
    "IMPORTACAO": "Importação",
    "IMP": "Importação",

    # Variações de Exportação
    "CARGA": "Exportação",
    "EMB": "Exportação",        # <-- ADICIONE ESTA LINHA (de Embarque)
    "EXPORTACAO": "Exportação",
    "EXP": "Exportação",
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
    'imo': 'imo',
    'viagem_voyage': 'viagem',

    # Colunas de Paranaguá
    'embarcação': 'navio',
    'chegada': 'data_prevista',    # Verifique se o nome da coluna de data está correto
    'eta': 'data_prevista',        # Adicionando 'eta' também, caso apareça
    'mercadoria': 'produto',
    'operacao': 'sentido',
    'ton': 'tonelagem',
    'previsto': 'tonelagem',       # Mapeando 'previsto' para 'tonelagem'
    'imo': 'imo',
    'viagem': 'viagem',
}

