# Desafio Técnico Veeries: Pipeline de Dados de Lineup Portuário

## 📝 Descrição do Projeto
Este projeto implementa um pipeline de dados ETL em Python para coletar, processar e agregar diariamente os dados de lineup de navios dos portos de Santos e Paranaguá. A solução é robusta, resiliente a inconsistências nos dados de origem e utiliza a arquitetura Medallion para garantir a qualidade e rastreabilidade dos dados. O resultado final é uma base de dados analítica (Camada Ouro) com os volumes diários movimentados por porto, produto e sentido.

## 🏛️ Arquitetura
A solução foi desenvolvida utilizando a arquitetura Medallion, que separa os dados em três camadas lógicas:
* **🥉 Camada Bronze:** Contém os dados brutos e imutáveis, extraídos diretamente das fontes (arquivos HTML com data de extração). Funciona como uma fonte da verdade, permitindo o reprocessamento completo do pipeline.
* **🥈 Camada Silver:** Armazena os dados após a consolidação das fontes, limpeza, padronização de esquema e, crucialmente, a **deduplicação** para garantir que cada evento de embarque seja representado apenas por sua previsão mais recente.
* **🥇 Camada Gold:** Apresenta os dados prontos para o consumo, agregados por dimensões de negócio para responder à pergunta central do desafio: os volumes diários de operação.

## 🚀 Como Executar
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/danielfloriani/desafio-veeries.git](https://github.com/danielfloriani/desafio-veeries.git)
    cd desafio-veeries
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o pipeline completo:**
    ```bash
    python pipeline.py
    ```
    Ao final da execução, a tabela final estará em `data/gold/volumes_diarios.parquet`.

## 🤔 Decisões de Projeto e Desafios Superados
O desenvolvimento seguiu uma abordagem iterativa, focada em robustez e na qualidade do dado final. As principais decisões foram:
* **Processamento da "Verdade Atual":** O pipeline foi projetado para processar apenas a extração mais recente de cada porto, garantindo que a base de dados reflita o estado mais atualizado do lineup, evitando a complexidade de lidar com previsões históricas conflitantes.
* **Deduplicação Inteligente:** Através da auditoria dos dados, percebeu-se que mesmo o arquivo mais recente poderia conter duplicatas. Foi implementada uma lógica de deduplicação baseada em uma chave de negócio robusta (`imo`, `viagem`, `data_prevista`, `produto`) e na data de extração, garantindo que cada evento de embarque seja contado apenas uma vez.
* **Robustez na Limpeza:** As funções de transformação foram construídas para serem resilientes a dados "sujos". O uso de `errors='coerce'` em conversões numéricas e de data, por exemplo, previne que o pipeline quebre e garante que apenas dados válidos prossigam para a camada final.
* **Validação Contínua:** O ceticismo sobre os resultados levou à criação de scripts de auditoria, que foram cruciais para descobrir e validar o comportamento do pipeline frente a problemas do mundo real, como formatos de data inconsistentes e reagendamentos de navios.
* **Modularidade e Configuração:** O código foi separado por responsabilidades (`extract`, `transform`, `config`), e configurações como mapeamentos de colunas foram externalizadas para o diretório `config`, facilitando a manutenção futura.

## 🔮 Próximos Passos e Melhorias
* **Orquestração:** Integrar o pipeline com um orquestrador como Airflow ou Prefect para agendamento e monitoramento automáticos.
* **Testes Unitários:** Implementar testes formais com `pytest` para as funções de transformação, garantindo que futuras alterações não quebrem a lógica de negócio.
* **Containerização:** Empacotar a aplicação com Docker para garantir a portabilidade e facilitar o deploy.
* **Logging:** Substituir os comandos `print` por um sistema de `logging` mais estruturado para melhor monitoramento em produção.