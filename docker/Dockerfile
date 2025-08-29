FROM python:3.11-slim

# Instala ferramentas básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia requirements e instala pacotes
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte
COPY ../src ./src

# Define PYTHONPATH para que imports de src funcionem
ENV PYTHONPATH=/app

# Comando padrão
CMD ["python", "-m", "src.main"]
