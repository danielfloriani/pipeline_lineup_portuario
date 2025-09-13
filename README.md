# Desafio Técnico Veeries: Pipeline de Dados de Lineup Portuário

## 📝 Descrição do Projeto
Este projeto implementa um pipeline de dados ETL (Extração, Transformação e Carga) em Python para coletar, processar e agregar diariamente os dados de lineup de navios dos portos de Santos e Paranaguá. O objetivo final é gerar uma base de dados analítica com os volumes diários movimentados por porto, produto e sentido (importação/exportação).

## 🏛️ Arquitetura
A solução foi desenvolvida utilizando a arquitetura Medallion, que separa os dados em três camadas lógicas:
* **🥉 Camada Bronze:** Contém os dados brutos, extraídos diretamente das fontes, sem nenhuma alteração (arquivos HTML). Isso garante a rastreabilidade e a capacidade de reprocessamento.
* **🥈 Camada Silver:** Armazena os dados após um processo de limpeza, padronização de esquema, conversão de tipos e unificação das diferentes fontes em um formato único e consistente (Parquet).
* **🥇 Camada Gold:** Apresenta os dados prontos para o consumo, agregados por dimensões de negócio para responder à pergunta central do desafio: volumes diários.

## 🚀 Como Executar
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/danielfloriani/lineup_ships]
    cd [lineup_ships]
    ```
2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o pipeline completo:**
    ```bash
    python pipeline.py
    ```
    Ao final da execução, os resultados estarão na pasta `data/`, com o arquivo final em `data/gold/volumes_diarios.parquet`.

### 🛠️ Estrutura do Projeto

O repositório está organizado de forma modular para separar as diferentes responsabilidades do pipeline, seguindo as melhores práticas de engenharia de software.

/
├── data/                   # Diretório dos dados (ignorado pelo .gitignore)
│   ├── bronze/             # Camada Bronze: Armazena os dados brutos e inalterados (HTMLs).
│   ├── silver/             # Camada Silver: Armazena os dados limpos e consolidados (Parquet).
│   └── gold/               # Camada Gold: Armazena os dados agregados e prontos para análise (Parquet).
│
├── src/                    # Diretório principal do código-fonte da aplicação.
│   ├── common/             # Módulos com funções utilitárias reutilizáveis (ex: baixar páginas).
│   ├── config/             # Módulos de configuração, sem lógica de negócio (ex: paths, URLs, dicionários).
│   ├── extract/            # Módulos responsáveis pela extração (scraping) dos dados de cada fonte.
│   ├── transform/          # Módulos responsáveis pela transformação e agregação (lógica das camadas Silver e Gold).
│   └── validation/         # Módulos para validação de dados e esquemas (ex: schemas Pandera).
│
├── .gitignore              # Arquivo que define quais arquivos/pastas não devem ser enviados ao Github.
├── pipeline.py             # Script principal (entrypoint) que orquestra a execução de todo o pipeline.
├── requirements.txt        # Lista das dependências do projeto para fácil instalação.
└── README.md               # Documentação do projeto (este arquivo).

## 🤔 Hipóteses e Decisões de Projeto
* **Resiliência a Falhas de SSL:** Foi implementado um fallback para tentativas de conexão sem verificação de certificado, pois foi detectado um problema de SSL em uma das fontes.
* **Manutenção para Schema Drift:** O pipeline foi adaptado para lidar com uma mudança no layout do site do Porto de Santos (remoção de uma coluna). A lógica de extração agora é mais robusta para lidar com colunas vazias.
* **Validação de Dados:** Foi utilizada a biblioteca `Pandera` para criar um script de validação (`validate_silver.py`) que garante a integridade estrutural dos dados consolidados antes do processamento final, atuando como um portão de qualidade.
* **Consolidação de Colunas:** Foi desenvolvida uma função auxiliar para consolidar colunas que, após a renomeação, ficavam duplicadas (ex: `sentido`, `produto`), garantindo um esquema limpo para a camada final.

## 🔮 Próximos Passos e Melhorias
* **Orquestração:** Integrar o pipeline com um orquestrador de workflows como Airflow ou Prefect para agendamento, monitoramento e retentativas automáticas.
* **Containerização:** Empacotar a aplicação com Docker para garantir a portabilidade e facilitar o deploy em diferentes ambientes.
* **Testes:** Expandir a suíte de testes unitários para as funções de transformação e validação, garantindo a qualidade do código.
* **Logging:** Substituir os comandos `print` por um sistema de logging mais robusto (ex: biblioteca `logging` do Python) para melhor controle e monitoramento dos eventos do pipeline.