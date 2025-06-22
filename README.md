# Desafio de Engenharia e Análise de Dados - FADESP 2025

## 1. Introdução

Este projeto foi desenvolvido como resposta ao Desafio de Engenharia e Análise de Dados da FADESP. O objetivo principal é realizar uma análise completa da relação entre a qualidade institucional das Instituições de Ensino Superior (IES) e a produção científica no Brasil, além de mapear as conexões que formam o ecossistema de pesquisa nacional. Para isso, foram utilizadas duas bases de dados públicas.

## 2. Fontes e Obtenção dos Dados

Os dados utilizados neste projeto são públicos e, devido ao seu tamanho, não foram incluídos diretamente no repositório. Para facilitar a avaliação, os arquivos exatos utilizados na análise estão disponíveis para download nos links diretos do Google Drive abaixo.

Para executar os notebooks, você precisa baixar os dois arquivos e colocá-los na pasta `data/raw/`.

1.  **Censo da Educação Superior (INEP):**
    * **Link para Download:** `https://drive.google.com/file/d/1Mi7edD7kQV89FXKR0deXmndfyT-OWAGS/view?usp=sharing`
    * **Arquivo Esperado:** `MICRODADOS_ED_SUP_IES_2023.CSV`

2.  **Bolsas de Pesquisa do CNPq:**
    * **Link para Download:** `https://drive.google.com/file/d/1w15Nki88dqH0uGCGLJGcZIvxFfBcYYC1/view?usp=sharing`
    * **Arquivo Esperado:** `Relatorio_de_dados_abertos_CNPq.csv`

## 3. Metodologia e Etapas do Projeto

O projeto foi estruturado em uma sequência lógica de etapas para garantir a qualidade e a reprodutibilidade da análise:

1.  **Exploração e Carregamento:** Análise inicial dos datasets para entender sua estrutura, identificar desafios de limpeza e planejar a unificação.
2.  **Engenharia de Dados (ETL):** Implementação de rotinas para limpar, padronizar, agregar e unificar os dados do INEP e do CNPq, gerando um dataset coeso e pronto para análise.
3.  **Análise Exploratória de Dados (EDA):** Geração de estatísticas descritivas e visualizações para responder perguntas de negócio e extrair os primeiros insights.
4.  **Análise Avançada (Machine Learning):** Aplicação de técnicas de clusterização (K-Means) e redução de dimensionalidade (PCA) para identificar perfis de instituições com base em suas características.
5.  **Análise de Redes:** Modelagem do fluxo de pesquisadores entre instituições utilizando a biblioteca `NetworkX` para identificar hubs de conhecimento e as principais rotas do fluxo de talentos no país.
6.  **Containerização (Docker):** Desenvolvimento de uma configuração Docker Compose para empacotar o pipeline de ETL e a análise de ML, garantindo um ambiente de execução isolado e reproduzível.

## 4. Principais Descobertas e Insights

A análise dos dados revelou padrões importantes sobre o cenário da educação superior e pesquisa no Brasil:

* **Forte Correlação Qualidade-Pesquisa:** Existe uma correlação positiva e forte (coeficiente de 0.69) entre o **número de docentes com doutorado** em uma IES e o **total de bolsas de pesquisa** recebidas do CNPq.
* **Concentração de Fomento:** As bolsas de pesquisa são majoritariamente concentradas em um grupo seleto de universidades, com **USP, UNICAMP e UFRJ** liderando com folga.
* **Hegemonia das Instituições Públicas:** As **universidades públicas (Federais e Estaduais)** são responsáveis pela esmagadora maioria das bolsas de pesquisa, confirmando seu papel central na produção científica do país.
* **Mapeamento do Fluxo de Talentos:** A análise de redes revelou as instituições que atuam como principais **'hubs'** na atração de pesquisadores (como USP e UNICAMP) e aquelas que são grandes **'formadoras'**, exportando talentos para o ecossistema científico nacional.
* **Perfis de Instituições (Clustering):** O modelo de Machine Learning conseguiu segmentar as instituições em **3 clusters distintos**: "Polos de Pesquisa", "IES em Desenvolvimento" e "Foco no Ensino".

## 5. Estrutura do Projeto

```
desafio-fadesp-2025/
├── data/
│   ├── raw/      <-- Coloque os arquivos .csv baixados aqui
│   └── processed/
├── notebooks/
│   ├── 1_exploracao_inicial.ipynb
│   ├── 2_limpeza_e_unificacao.ipynb
│   ├── 3_analise_e_visualizacao.ipynb
│   ├── 4_analise_avancada_ml.ipynb
│   └── 5_analise_de_redes.ipynb
├── reports/
│   ├── cluster_profiles_report.txt
│   └── cluster_visualization.png
├── scripts/
│   ├── etl_pipeline.py
│   └── ml_analysis.py
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## 6. Como Executar o Projeto

Existem duas maneiras de executar e explorar este projeto. A primeira é a recomendada para uma análise detalhada do processo.

### Método 1: Execução Local dos Notebooks (Recomendado)

Este método permite acompanhar passo a passo toda a construção da análise.

**Pré-requisitos:**
* Python 3.9 ou superior
* Git

**Passos:**

1.  **Clone o repositório.**
2.  **Baixe os dados** conforme as instruções na Seção 2 e coloque-os na pasta `data/raw/`.
3.  **Crie e ative um ambiente virtual** e instale as dependências com `pip install -r requirements.txt`.
4.  **Inicie o Jupyter Lab** com `jupyter lab`.
5.  No ambiente Jupyter, abra a pasta `notebooks/` e execute os arquivos na ordem numérica (de 1 a 5).

### Método 2: Execução com Docker (Experimental)

Este método executa o pipeline de ETL e ML de forma automática.

**Pré-requisitos:**
* Docker Desktop instalado e em execução.
* Dados baixados na pasta `data/raw/`.

**Passos:**

1.  Na pasta raiz do projeto, execute o comando: `docker-compose up --build`.
2.  Ao final, a pasta `reports/` será criada com o relatório e a imagem dos clusters.

> **Nota Importante:** A execução bem-sucedida deste método depende de uma configuração local do Docker e do WSL funcionando corretamente. A **execução via notebooks (Método 1) é a forma garantida de revisar este projeto.**

## 7. Tecnologias Utilizadas

* **Linguagem:** Python 3.9
* **Bibliotecas Principais:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, NetworkX, Unidecode
* **Ferramentas de Engenharia:** Docker, Docker Compose, PostgreSQL
* **Ambiente de Desenvolvimento:** Jupyter Lab, PyCharm

## 8. Metodologia de Trabalho e Ferramentas

Para acelerar o desenvolvimento e explorar diferentes abordagens técnicas de forma eficiente, este projeto contou com o auxílio de uma Inteligência Artificial generativa (Google Gemini) como uma ferramenta de programação em par (pair programming).

A IA foi utilizada como uma assistente para:
* Gerar blocos de código repetitivos (boilerplate).
* Sugerir soluções para depuração de erros complexos, como os de configuração de ambiente do Git e Docker/WSL.
* Refatorar o código para seguir as melhores práticas, como na separação dos scripts e na otimização de funções.

Toda a **arquitetura do projeto, as decisões analíticas, a interpretação dos resultados, a depuração final e a validação da lógica** foram conduzidas pelo autor deste projeto. O uso da IA foi um meio para otimizar o tempo e permitir um foco maior na estratégia e na qualidade da análise.
