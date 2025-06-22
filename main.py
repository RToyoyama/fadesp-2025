# Importa as funções dos nossos scripts
from scripts.etl_pipeline import run_etl
from scripts.ml_analysis import run_ml_analysis

if __name__ == '__main__':
    print("Orquestrador principal: Iniciando a execução do pipeline completo.")

    # Etapa 1: Executar o processo de ETL para carregar os dados no banco
    run_etl()

    # Etapa 2: Executar a análise de ML e gerar relatórios
    run_ml_analysis()

    print("Orquestrador principal: Processo finalizado com sucesso.")