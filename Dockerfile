# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto para o diretório de trabalho do contêiner
COPY . .

# Comando que será executado quando o contêiner iniciar
CMD ["python", "main.py"]