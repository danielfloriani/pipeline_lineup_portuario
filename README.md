# Desafio Técnico: Pipeline de Dados de Lineup Portuário

## 📝 Descrição do Projeto
Este projeto implementa um pipeline de dados ETL em Python para coletar, processar e agregar diariamente as informações de lineup de navios dos portos de Santos e Paranaguá. A solução foi projetada para ser resiliente às inconsistências dos dados de origem, utilizando a arquitetura Medallion para garantir a qualidade e a rastreabilidade em cada etapa. O resultado final é uma base de dados analítica (Camada Ouro) com os volumes diários movimentados por porto, produto e sentido (importação/exportação).

## 🏛️ Arquitetura
A solução foi desenvolvida utilizando a arquitetura Medallion, que separa o fluxo de dados em três camadas lógicas:

* **🥉 Camada Bronze:** Contém os dados brutos e imutáveis, extraídos diretamente das fontes (arquivos HTML com data de extração). Funciona como uma fonte da verdade, permitindo o reprocessamento e a auditoria completa do pipeline.
* **🥈 Camada Silver:** Armazena os dados após a consolidação das fontes. Nesta camada, os dados ainda refletem as heterogeneidades estruturais de cada porto.
* **🥇 Camada Gold:** Apresenta o produto de dados final. Nesta etapa, a lógica de transformação é aplicada para limpar, padronizar, deduplicar e agregar os dados em um esquema único e confiável, pronto para o consumo analítico.

## 🚀 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/danielfloriani/pipeline_lineup_portuario](https://github.com/danielfloriani/pipeline_lineup_portuario.git)
    cd pipeline_lineup_portuario
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o pipeline completo:**
    ```bash
    python pipeline.py
    ```
    Ao final da execução, a tabela analítica estará em `data/gold/volumes_diarios.parquet`.

## 🤔 Decisões de Projeto e Desafios Superados

O desenvolvimento seguiu uma abordagem iterativa, onde a auditoria contínua dos resultados guiou as decisões de engenharia para aumentar a robustez da solução.

* **Estratégia de Processamento:** A decisão inicial de processar todo o histórico da camada Bronze revelou um desafio crítico: a duplicação de volumes devido a reagendamentos de navios. A arquitetura foi então refinada para processar apenas a "fotografia" mais recente de cada porto, garantindo que a camada Ouro reflita o estado mais atualizado do lineup.

* **Centralização da Lógica de Limpeza:** Tentativas iniciais de distribuir a lógica de limpeza entre os módulos de extração criaram inconsistências difíceis de depurar. A solução final e mais robusta foi centralizar **toda** a lógica de padronização, conversão de tipos e tratamento de casos específicos (como os formatos numéricos de Paranaguá) em um único módulo (`gold_processor.py`), garantindo que as regras sejam aplicadas de forma uniforme sobre o conjunto de dados consolidado.

* **Robustez na Conversão de Tipos:** A conversão de dados textuais para numéricos e datas foi um desafio chave. A utilização de `errors='coerce'` em `pd.to_numeric` e `pd.to_datetime`, combinada com funções de limpeza específicas, garantiu que o pipeline não falhasse com dados mal formatados, descartando-os de forma controlada e registrando apenas informações de alta qualidade.

* **Deduplicação Inteligente:** Mesmo processando apenas o arquivo mais recente, foi identificado que poderiam existir duplicatas. Foi implementada uma lógica de deduplicação baseada em uma chave de negócio (`imo`, `viagem`, `data_prevista`, `produto`) para assegurar que cada evento de embarque seja representado apenas uma vez no resultado final.

## 🔮 Próximos Passos e Melhorias

* **Orquestração:** Integrar o pipeline com um orquestrador de workflows como Airflow ou Prefect para agendamento, monitoramento e retentativas automáticas.
* **Testes Unitários:** Implementar testes formais com `pytest` para as funções de transformação, validando a lógica de limpeza e agregação de forma isolada.
* **Containerização:** Empacotar a aplicação com Docker para garantir a portabilidade e facilitar o deploy em diferentes ambientes.
* **Logging:** Substituir os comandos `print` por um sistema de `logging` mais estruturado para melhor controle e monitoramento dos eventos do pipeline em produção.