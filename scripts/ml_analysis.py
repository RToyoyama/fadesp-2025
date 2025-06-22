import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


def run_ml_analysis():
    """
    Executa a análise de ML nos dados processados do banco de dados.
    1. Lê os dados da tabela PostgreSQL.
    2. Executa o modelo de clusterização K-Means.
    3. Gera um relatório de perfil dos clusters.
    4. Gera e salva uma visualização dos clusters com PCA.
    """
    print("\nMódulo ML: Iniciando análise avançada...")

    # --- CONEXÃO COM O BANCO DE DADOS PARA LER OS DADOS ---
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_name = os.environ.get('POSTGRES_DB')
    db_host = 'db'
    db_string = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

    try:
        engine = create_engine(db_string)
        # Lê os dados da tabela que o ETL criou
        df = pd.read_sql_table('censo_cnpq_unificado', engine)
        print("Módulo ML: Dados lidos com sucesso do PostgreSQL.")
    except Exception as e:
        print(f"Módulo ML: Erro ao ler dados do banco de dados: {e}")
        return

    # --- PREPARAÇÃO DOS DADOS PARA O MODELO (Lógica da Etapa 4) ---
    features = ['QT_DOC_EX_DOUT', 'QT_DOC_EX_MEST', 'total_bolsas_cnpq']
    df_ml = df.dropna(subset=features).copy()
    df_ml_filtered = df_ml[(df_ml[features].T != 0).any()]

    if df_ml_filtered.empty:
        print("Módulo ML: Não há dados suficientes para a clusterização.")
        return

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_ml_filtered[features])

    # --- MODELAGEM K-MEANS ---
    K_IDEAL = 3
    kmeans = KMeans(n_clusters=K_IDEAL, random_state=42, n_init=10)
    df_ml_filtered['cluster'] = kmeans.fit_predict(df_scaled)
    print("Módulo ML: Clusterização K-Means executada.")

    # --- GERAÇÃO DO RELATÓRIO ---
    print("Módulo ML: Gerando relatório de perfil dos clusters...")
    cluster_profile = df_ml_filtered.groupby('cluster')[features].mean().sort_values(by='total_bolsas_cnpq',
                                                                                     ascending=False)

    # Cria a pasta 'reports' se ela não existir
    os.makedirs('reports', exist_ok=True)
    report_path = 'reports/cluster_profiles_report.txt'
    with open(report_path, 'w') as f:
        f.write("--- Perfil Médio dos Clusters de Instituições ---\n\n")
        f.write(cluster_profile.to_string())
        f.write("\n\n--- Interpretação ---\n")
        f.write("Cluster 0: Polos de Pesquisa (alto volume de doutores e bolsas).\n")
        f.write("Cluster 1: IES em Desenvolvimento (volume intermediário).\n")
        f.write("Cluster 2: Foco no Ensino (baixo volume de doutores e bolsas).\n")
    print(f"Módulo ML: Relatório salvo em '{report_path}'.")

    # --- GERAÇÃO DA VISUALIZAÇÃO PCA ---
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)
    df_pca = pd.DataFrame(data=df_pca, columns=['Componente 1', 'Componente 2'])
    df_pca['cluster'] = df_ml_filtered['cluster']

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='Componente 1', y='Componente 2', hue='cluster', data=df_pca, palette='deep', alpha=0.8)
    plt.title('Visualização dos Clusters de IES (PCA)')

    viz_path = 'reports/cluster_visualization.png'
    plt.savefig(viz_path)
    print(f"Módulo ML: Visualização salva em '{viz_path}'.")
    print("Módulo ML: Análise avançada concluída.")