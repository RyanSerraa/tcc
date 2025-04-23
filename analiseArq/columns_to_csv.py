import pandas as pd

# Realiza toda a leitura dos dados do CSV
df = pd.read_csv("/home/ryan/tcc/tcc/analiseArq/crime_data/NYPD_Arrests_Data__Historic_.csv")

# Obtém valores únicos da coluna "Crm Cd Desc"
df_group_age_NY = df['AGE_GROUP'].drop_duplicates()

# Salva os dados filtrados em um novo arquivo CSV
df_group_age_NY.to_csv("GroupAge.csv", index=True, header=True)

df = pd.read_csv("/home/ryan/tcc/tcc/analiseArq/crime_data/Dallas Police Arrests.csv")

# Obtém valores únicos da coluna "Crm Cd Desc"
df_age_dallas = df['Age'].drop_duplicates()

# Salva os dados filtrados em um novo arquivo CSV
df_age_dallas.to_csv("Age.csv", index=True, header=True)
