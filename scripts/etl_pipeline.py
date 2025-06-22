import os
import pandas as pd
import time
from sqlalchemy import create_engine
from unidecode import unidecode


def padronizar_nome(nome):
    """Função para padronizar nomes de instituições."""
    if not isinstance(nome, str):
        return ''
    nome = nome.lower()
    nome = unidecode(nome)
    nome = nome.replace('.', '').replace('-', ' ').replace('  ', ' ')
    return nome.strip()


def run_etl():
    """
    Função principal que executa todo o processo de ETL:
    1. Carrega os dados brutos.
    2. Limpa e transforma os dados.
    3. Salva o resultado no banco de dados PostgreSQL.
    """
    print("Módulo ETL: Iniciando o processo...")

    # --- CARREGAMENTO DOS DADOS ---
    # Lembre-se de corrigir o nome do arquivo aqui se necessário
    path_inep = './data/raw/MICRODADOS_ED_SUP_IES_2023.CSV'
    path_cnpq = './data/raw/Relatorio_de_dados_abertos_CNPq.csv'

    df_inep = pd.read_csv(path_inep, sep=';', encoding='latin-1')

    dtype_cnpq = {0: 'str', 7: 'str', 23: 'str', 24: 'str'}
    df_cnpq = pd.read_csv(path_cnpq, sep=';', encoding='latin-1', skiprows=5, dtype=dtype_cnpq)
    print("Módulo ETL: Dados brutos carregados.")

    # --- SELEÇÃO E TRANSFORMAÇÃO (Lógica da Etapa 2) ---
    colunas_inep = ['CO_IES', 'NO_IES', 'SG_IES', 'NO_MUNICIPIO_IES', 'SG_UF_IES', 'TP_CATEGORIA_ADMINISTRATIVA',
                    'QT_DOC_EX_DOUT', 'QT_DOC_EX_MEST']
    colunas_cnpq = ['Modalidade', 'Instituição Destino', 'Sigla Instituição Destino', 'Grande Área', 'Área']

    df_inep_selecionado = df_inep[colunas_inep].copy()
    df_cnpq_selecionado = df_cnpq[colunas_cnpq].copy()

    df_inep_selecionado['nome_ies_padronizado'] = df_inep_selecionado['NO_IES'].apply(padronizar_nome)
    df_cnpq_selecionado['nome_ies_padronizado'] = df_cnpq_selecionado['Instituição Destino'].apply(padronizar_nome)

    df_cnpq_agregado = df_cnpq_selecionado.groupby('nome_ies_padronizado').agg(
        total_bolsas_cnpq=('Modalidade', 'size')).reset_index()

    df_unificado = pd.merge(df_inep_selecionado, df_cnpq_agregado, on='nome_ies_padronizado', how='left')
    df_unificado['total_bolsas_cnpq'] = df_unificado['total_bolsas_cnpq'].fillna(0).astype(int)
    print("Módulo ETL: Dados transformados e unificados.")

    # --- CARGA NO BANCO DE DADOS POSTGRESQL ---
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_name = os.environ.get('POSTGRES_DB')
    db_host = 'db'
    db_port = 5432
    db_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    print(f"Módulo ETL: Tentando conectar ao banco de dados em {db_host}...")

    retries = 5
    engine = None
    while retries > 0:
        try:
            engine = create_engine(db_string)
            engine.connect()
            print("Módulo ETL: Conexão com o banco de dados estabelecida com sucesso!")
            break
        except Exception as e:
            print(f"Módulo ETL: Erro ao conectar: {e}. Tentando novamente em 5 segundos...")
            retries -= 1
            time.sleep(5)

    if engine is None:
        print("Módulo ETL: Não foi possível conectar ao banco de dados. Abortando.")
        return

    df_unificado.to_sql('censo_cnpq_unificado', engine, if_exists='replace', index=False)
    print("Módulo ETL: Dados salvos com sucesso na tabela 'censo_cnpq_unificado'.")