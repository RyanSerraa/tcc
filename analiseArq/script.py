
import pandas as pd

# Nome do arquivo CSV de entrada
csv_file = 'fperson.csv'
# Nome do arquivo JSON de saída
# json_file = 'dump.json'

# Carregar o arquivo CSV
df = pd.read_csv(csv_file)
# Amostrar 1% dos dados (ajuste a proporção conforme necessário)
print(len(df))

# csv_file= "prepareted.csv"
# # Abrindo o arquivo CSV e lendo os dados
# with open(csv_file, mode='r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)
#     # Convertendo as linhas do CSV em uma lista de dicionários
#     data = [row for row in csv_reader]

# # Salvando os dados em JSON
# with open(json_file, mode='w', encoding='utf-8') as file:
#     json.dump(data, file, indent=4, ensure_ascii=False)

# print(f"Arquivo JSON criado: {json_file}")


# # Nome do arquivo original e do arquivo atualizado
# arquivo_original = "dump.json"
# arquivo_atualizado = "dump_atualizado.json"

# # Carregar os dados do arquivo JSON original
# with open(arquivo_original, "r", encoding="utf-8") as file:
#     data = json.load(file)

# # Remover os pontos nas chaves de cada item
# data_atualizada = [
#     {key.replace(".", ""): value for key, value in item.items()} for item in data
# ]

# # Salvar os dados atualizados em um novo arquivo JSON
# with open(arquivo_atualizado, "w", encoding="utf-8") as file:
#     json.dump(data_atualizada, file, ensure_ascii=False, indent=4)

# print(f"Dados atualizados salvos em '{arquivo_atualizado}'.")