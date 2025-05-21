import pandas as pd
import numpy as np

df_chicago= pd.read_csv("crime_data/Chicago Crimes_-_2001_to_Present.csv")

#Tipo do crime 
primary_type= df_chicago["Primary Type"].drop_duplicates()
primary_type.to_csv("primary_type.csv", index= False)

#Descrição do crime
description = df_chicago["Description"].drop_duplicates()
description.to_csv("description.csv", index=False)

#Location Description
location_description = df_chicago["Location Description"].drop_duplicates()
location_description.to_csv("location_description.csv", index=False)


df_dallas = pd.read_csv("crime_data/Dallas Police Arrests.csv")

#Tipo de armas
ar_weapon = df_dallas["ArWeapon"].drop_duplicates()
ar_weapon.to_csv("arWeapon.csv", index=False)

# Raças disponiveis 
race = df_dallas["Race"].drop_duplicates()
race.to_csv("race.csv", index=False)
# Tipo das drogas
drug_type = df_dallas["DrugType"].drop_duplicates()
drug_type.to_csv("drugType.csv", index=False)

df_la = pd.read_csv("crime_data/LA Crime_Data_from_2010_to_2019.csv")

# Tipo do crime cometido
type_crime = df_la["Crm Cd Desc"].drop_duplicates()
type_crime.to_csv("type_crime.csv", index=False)

# Idade da vitima
vict_age = df_la["Vict Age"].drop_duplicates()
vict_age.to_csv("vict_age.csv", index=False)

# Sexo da vitima 
vict_sex = df_la["Vict Sex"].drop_duplicates()
vict_sex.to_csv("vict_sex.csv", index=False)

# Descendencia da vitima
vict_descent = df_la["Vict Descent"].drop_duplicates()
vict_descent.to_csv("vict_descent.csv", index=False)

# Tipo da arma
weapon_desc = df_la["Weapon Desc"].drop_duplicates()
weapon_desc.to_csv("weapon_desc.csv", index=False)

df_NYPD = pd.read_csv("crime_data/NYPD_Arrests_Data__Historic_.csv")

type_crime_group = df_NYPD[["PD_CD", "PD_DESC"]].drop_duplicates(subset="PD_CD")
type_crime_group.to_csv("type_crime_group.csv", index=False)

age_group = df_NYPD["AGE_GROUP"].drop_duplicates()
age_group.to_csv("age_group.csv", index = False)

perp_race = df_NYPD["PERP_RACE"].drop_duplicates()
perp_race.to_csv("perp_race.csv", index=False)


df_fatal_encounters = pd.read_csv("crime_data/fatal_encounters_dot_org.csv")

age_fatal_encounters = df_fatal_encounters["Subject's age"].drop_duplicates()
age_fatal_encounters.to_csv("age_fatal_encounters.csv", index=False)

race_fatal_encounters = df_fatal_encounters["Subject's race"].drop_duplicates()
race_fatal_encounters.to_csv("race_fatal_encounters.csv", index=False)

gender_fatal_encounters = df_fatal_encounters["Subject's gender"].drop_duplicates()
gender_fatal_encounters.to_csv("gender_fatal_encounters.csv", index=False)

location_fatal_encounters = df_fatal_encounters[["Location of death (city)"]].drop_duplicates()
location_fatal_encounters.to_csv("location_fatal_encounters.csv")

df_police_deaths = pd.read_csv("crime_data/police_deaths_538.csv")

dept = df_police_deaths["dept"].drop_duplicates()
dept.to_csv("dept.csv", index=False)

df_police_killings = pd.read_csv("crime_data/police_killings_MPV.csv")

vict_age_police__killigs = df_police_killings["Victim's age"].drop_duplicates()
vict_age_police__killigs.to_csv("vict_age_police_killigs.csv", index=False)

vict_gender_police__killigs = df_police_killings["Victim's gender"].drop_duplicates()
vict_gender_police__killigs.to_csv("vict_gender_police_killigs.csv", index=False)

vict_race_police__killigs = df_police_killings["Victim's race"].drop_duplicates()
vict_race_police__killigs.to_csv("vict_race_police_killigs.csv", index=False)

city = df_police_killings["City"].drop_duplicates()
city.to_csv("city.csv", index= False)

cause_of_death = df_police_killings["Cause of death"].drop_duplicates()
cause_of_death.to_csv("cause_of_death.csv", index=False)

Armed_group= df_police_killings[["Unarmed/Did Not Have an Actual Weapon", "Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)" ]].drop_duplicates()
Armed_group.to_csv("Armed.csv")

threat_level = df_police_killings["Alleged Threat Level (Source: WaPo)"].drop_duplicates()
threat_level.to_csv("threat.csv", index=False)

df_shootings = pd.read_csv("crime_data/shootings_wash_post.csv")

race_shootings = df_shootings["race"].drop_duplicates()
race_shootings.to_csv("race_shootings.csv", index=False)

city_shootings = df_shootings["city"].drop_duplicates()
city_shootings.to_csv("city_shootings.csv", index=False)

threat_level_shootings = df_shootings["threat_level"].drop_duplicates()
threat_level_shootings.to_csv("threat_level_shootings.csv", index=False)


## Tipo de crime 
# Primary Type, type_crime,type_crime_group

## Tipo de arma
#ar_weapon,weapon_desc

## Raças
# race, perp_race