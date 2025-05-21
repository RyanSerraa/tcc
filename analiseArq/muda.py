from pyspark.sql.functions import split, trim, concat_ws, col,when, lit, date_format, to_timestamp, upper, regexp_replace, collect_list, substring, first, length, ltrim, rtrim, to_date, create_map, regexp_extract, year,dayofmonth, month, lower
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

# Normalização do Dallas
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests.select("ArArrestDate","ArLCity","ArWeapon","ArresteeName","Age","Race","Sex", "DrugType")
split_col = split(col("ArresteeName"), ",")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("ArresteeName",
    concat_ws(" ",
        trim(split_col.getItem(1)),
        trim(split_col.getItem(2)),
        trim(split_col.getItem(0))
    )
)
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn(
    "Race",
    when(col("Race") == "Hispanic or Latino", "Hispanic")
    .when(col("Race").isin("Black", "White", "Asian", "Hispanic"), col("Race"))
    .otherwise("Others")
)
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("Sex", when(col("Sex").isin("Female", "Male"), col("Sex")).otherwise("Unknown"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn(
    "Age",
    when(col("Age") == "LOS ANGELES, CA", None)
    .when(col("Age") == "DALLAS, TX", None)
    .otherwise(col("Age"))
)
valores_invalidos = ["None", "Drugs", "THREATS", "Hands/Feet", "33", "Gas/Carbon Monoxide","Other"]
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn(
    "ArWeapon",
    when(col("ArWeapon").isNull(), "Unknown")
    .when(col("ArWeapon").isin(valores_invalidos), "Unknown")
    .otherwise(col("ArWeapon"))
)
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("ArArrestDate", to_timestamp("ArArrestDate", "MM/dd/yyyy hh:mm:ss a"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("ArArrestDate", to_date(col("ArArrestDate"), "MM/dd/yyyy"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("YEAR", year(col("ArArrestDate"))) \
                      .withColumn("MONTH", month(col("ArArrestDate")))\
                      .withColumn("DAY", dayofmonth(col("ArArrestDate")))

df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("DrugType", when(col("DrugType").isNull() | col("DrugType").isin("No", "Uknown", "Yes"), "UNKNOWN").otherwise(col("DrugType")))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("DrugType", upper(col("DrugType")))

df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("CRIME", lit("UNKNOWN"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("STATE", lit("TEXAS"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("LATITUDE", lit("32.776667"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("LONGITUDE", lit("-96.796990"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("ArLCity", when(col("ArLCity").isNotNull(), "DALLAS").otherwise("DALLAS"))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("ArWeapon", upper(col("ArWeapon")))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("Race", upper(col("Race")))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("Sex", upper(col("Sex")))
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumn("Age", col("Age").cast("int"))

df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("ArLCity", "CITY")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("ArArrestDate", "DATE")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("ArWeapon", "WEAPON")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("ArresteeName", "NAME")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("Age", "AGE")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("Race", "RACE")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("Sex", "SEX")
df_spark_Dallas_Arrests_data = df_spark_Dallas_Arrests_data.withColumnRenamed("DrugType", "DRUG")

df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests.select("ARREST_DATE","PD_DESC", "AGE_GROUP", "PERP_SEX", "PERP_RACE", "Latitude", "Longitude")

df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("PD_DESC",
                                   when(col("PD_DESC").contains("ABORTION"), "ABORTION")
                                   .when(col("PD_DESC").contains("ADM.CODE"), "ADMINISTRATIVE CODE VIOLATION")
                                   .when(col("PD_DESC").contains("HARASSMENT"), "HARASSMENT")
                                   .when(col("PD_DESC") == "AGGRAVATED SEXUAL ASBUSE", "SEXUAL ABUSE")
                                   .when(col("PD_DESC") == "FAC. SEXUAL OFFENSE W/CONTROLLED SUBSTANCE", "SEXUAL OFFENSE WITH CONTROLLED SUBSTANCE")
                                   .when(col("PD_DESC").contains("SEXUAL ABUSE"), "SEXUAL ABUSE")
                                   .when(col("PD_DESC").contains("SEXUAL MISCONDUCT"), "SEXUAL MISCONDUCT")
                                   .when(col("PD_DESC").contains("USE OF A CHILD IN A SEXUAL"), "USE OF A CHILD IN A SEXUAL PERFORMANCE")
                                   .when(col("PD_DESC").contains("COURSE OF SEXUAL CONDUCT AGAIN"), "COURSE OF SEXUAL CONDUCT AGAINST A CHILD")
                                   .when(col("PD_DESC").contains("AGRICULTURE & MARKETS LAW"), "AGRICULTURE & MARKETS LAW")
                                   .when(col("PD_DESC").contains("ALCOHOLIC BEVERAGE"), "ALCOHOLIC BEVERAGES - PUBLIC CONTROL LAW")
                                   .when(col("PD_DESC").contains("ARSON"), "ARSON")
                                   .when(col("PD_DESC").contains("RIOT"), "RIOT")
                                   .when(col("PD_DESC").contains("ROBBERY"), "ROBBERY")
                                   .when((col("PD_DESC").contains("ASSAULT 2")) | (col("PD_DESC").contains("ASSAULT 3")), "ASSAULT")
                                   .when(col("PD_DESC").contains("VEHICULAR ASSAULT"), "VEHICULAR ASSAULT")
                                   .when(col("PD_DESC").contains("BAIL JUMPING"), "BAIL JUMPING")
                                   .when(col("PD_DESC").contains("IMPAIRED DRIVING"), "IMPAIRED DRIVING")
                                   .when(col("PD_DESC").contains("BICYCLE"), "BICYCLE TRAFFIC INFRACTION")
                                   .when(col("PD_DESC").contains("BRIBERY"), "BRIBERY")
                                   .when(col("PD_DESC").contains("SODOMY"), "SODOMY")
                                   .when(col("PD_DESC").contains("UNLAWFUL POSS. WEAPON UPON SCH"), "UNLAWFUL POSS. WEAPON UPON SCHOOL GROUNDS")
                                   .when(col("PD_DESC").contains("SOLICITATION"), "SOLICITATION CRIMINAL")
                                   .when(col("PD_DESC").contains("SALE SCHOOL GROUNDS"), "SALE SCHOOL GROUNDS")
                                   .when(col("PD_DESC").contains("RAPE"), "RAPE")
                                   .when(col("PD_DESC").contains("TRESPASS"), "TRESPASS CRIMINAL")
                                   .when(col("PD_DESC").contains("TRAFFIC"), "OFFENSES RELATED TO TRAFFIC")
                                   .when(col("PD_DESC").contains("STOLEN PROPERTY"), "STOLEN PROPERTY")
                                   .when(col("PD_DESC").contains("SALE OF UNAUTHORIZED RECORDING"), "SALE OF UNAUTHORIZED RECORDING")
                                   .when(col("PD_DESC").contains("RECKLESS"), "RECKLESS")
                                   .when(col("PD_DESC").contains("BURGLARY"), "BURGLARY")
                                   .when(col("PD_DESC").contains("UNAUTHORIZED USE VEHICLE"), "UNAUTHORIZED USE VEHICLE")
                                   .when(col("PD_DESC").contains("PUBLIC ADMINIS"), "PUBLIC ADMINISTRATION")
                                   .when(col("PD_DESC").contains("CHILD,OFFENSES AGAINST"), "OFFENSES AGAINST CHILD")
                                   .when(col("PD_DESC").contains("COERCION"), "COERCION")
                                   .when(col("PD_DESC").contains("TAMPERING"), "TAMPERING")
                                   .when(col("PD_DESC").contains("RIGHT OF WAY"), "RIGHT OF WAY")
                                   .when(col("PD_DESC").contains("PUBLIC SAFETY"), "PUBLIC SAFETY")
                                   .when(col("PD_DESC").contains("PUBLIC HEALTH LAW"), "PUBLIC HEALTH LAW")
                                   .when(col("PD_DESC").contains("MONEY LAUNDERING"), "MONEY LAUNDERING")
                                   .when(col("PD_DESC").contains("COMPUTER"), "OFFENSES RELATED TO COMPUTER")
                                   .when(col("PD_DESC").contains("CONSPIRACY"), "CONSPIRACY")
                                   .when(col("PD_DESC").contains("RADIO DEVICES"), "RADIO DEVICES")
                                   .when(col("PD_DESC").contains("KIDNAPPING"), "KIDNAPPING")
                                   .when(col("PD_DESC").contains("PERJURY"), "PERJURY")
                                   .when(col("PD_DESC").contains("PEDESTRIAN"), "PEDESTRIAN")
                                   .when(col("PD_DESC").contains("POSSESSION HYPODERMIC INSTRUME"), "POSSESSION HYPODERMIC INSTRUMENT")
                                   .when(col("PD_DESC").contains("PARK"), "PARKING")
                                   .when(col("PD_DESC").contains("MISCHIEF"), "MISCHIEF")
                                   .when(col("PD_DESC").contains("MENACING"), "MENACING")
                                   .when(col("PD_DESC").contains("NUISANCE"), "NUISANCE")
                                   .when(col("PD_DESC").contains("PROSTITUTION"), "PROSTITUTION")
                                   .when(col("PD_DESC").contains("LARCENY"), "LARCENY")
                                   .when(col("PD_DESC").contains("INCEST"), "INCEST")
                                   .when(col("PD_DESC").contains("MANUFA"), "OFFENSES RELATED TO MANUFACTURE")
                                   .when(col("PD_DESC").contains("IMPRISONMENT"), "IMPRISONMENT")
                                   .when(col("PD_DESC").contains("IMPERSONATION"), "IMPERSONATION")
                                   .when(col("PD_DESC").contains("CRIMINAL DISPOSAL FIREARM 1"), "CRIMINAL DISPOSAL FIREARM")
                                   .when(col("PD_DESC").contains("CRIMINAL MIS"), "CRIMINAL MISCHIEF")
                                   .when(col("PD_DESC").contains("CUSTODIAL INTERFERENCE"), "CUSTODIAL INTERFERENCE")
                                   .when(col("PD_DESC").contains("VULNERABLE ELDERLY"), "VULNERABLE ELDERLY")
                                   .when(col("PD_DESC").contains("FACILITATION"), "FACILITATION CRIMINAL")
                                   .when(col("PD_DESC").contains("FALSE REPORT"), "FALSE REPORT")
                                   .when(col("PD_DESC").contains("FIREWORKS"), "FIREWORKS")
                                   .when(col("PD_DESC").contains("FOLLOWING"), "FOLLOWING CLOSELY")
                                   .when(col("PD_DESC").contains("FORGERY"), "FORGERY")
                                   .when(col("PD_DESC").contains("FRAUD"), "FRAUD")
                                   .when(col("PD_DESC").contains("WEAPONS,PROHIBITED"), "WEAPONS, PROHIBITED")
                                   .when(col("PD_DESC").contains("WAY STREET"), "ONE WAY STREET")
                                   .when(col("PD_DESC").contains("OBSCEN"), "OBSCENITY")
                                   .when(col("PD_DESC").contains("FUGITIVE"), "FUGITIVE")
                                   .when(col("PD_DESC").contains("MANSLAUGHTER"), "MANSLAUGHTER")
                                   .when(col("PD_DESC").contains("GENERAL BUSINESS LAW"), "GENERAL BUSINESS LAW")
                                   .when(col("PD_DESC").contains("GAMBLING"), "GAMBLING")
                                   .when(col("PD_DESC").contains("LOITERING"), "LOITERING")
                                   .when(col("PD_DESC").contains("MATERIAL              OFFENSIV"), "MATERIAL OFFENSIVE")
                                   .when(col("PD_DESC").contains("HOMICIDE"), "HOMICIDE")
                                   .when(col("PD_DESC").contains("TERRORIS"), "OFFENSES RELATED TO TERRORISM")
                                   .when(col("PD_DESC").contains("MARIJUANA, POSSESSION"), "MARIJUANA, POSSESSION")
                                   .when(col("PD_DESC").contains("MARIJUANA, SALE"), "MARIJUANA, SALE")
                                   .when(col("PD_DESC").contains("IDENTITY THFT"), "IDENTITY THEFT")
                                   .when((col("PD_DESC").contains("F.C.A.")) | (col("PD_DESC").contains("F.O.A.")), "FAMILY COURT ACT")
                                   .when((col("PD_DESC").contains("WEAPONS POSSESSION")) | (col("PD_DESC").contains("WEAPONS, POSSESSION")), "WEAPONS POSSESSION")
                                   .when((col("PD_DESC").contains("WEAPONS DISPOSITION")) | (col("PD_DESC").contains("WEAPONS,DISPOSITION")), "WEAPONS DISPOSITION")
                                   .when((col("PD_DESC").contains("CONTROLLED SUBSTANCE, POSSESSI")) | (col("PD_DESC").contains("CONTROLLED SUBSTANCE,POSSESS.")), "CONTROLLED SUBSTANCE, POSSESSION")
                                   .when((col("PD_DESC").contains("THEFT OF")) | (col("PD_DESC").contains("THEFT,")), "THEFT")
                                   .when((col("PD_DESC").contains("CONTROLLED SUBSTANCE, INTENT T")) | (col("PD_DESC").contains("CONTROLLED SUBSTANCE,INTENT TO")), "CONTROLLED SUBSTANCE, INTENT TO SELL")
                                   .when((col("PD_DESC").contains("CONTROLLED SUBSTANCE, SALE")) | (col("PD_DESC").contains("CONTROLLED SUBSTANCE,SALE")), "CONTROLLED SUBSTANCE, SALE")
                                   .when((col("PD_DESC").contains("DISORDERLY CONDUCT")) | (col("PD_DESC").contains("DIS. CON.")), "DISORDERLY CONDUCT")
                                   .when((col("PD_DESC").contains("LEAVING SCENE-ACCIDENT")) | (col("PD_DESC").contains("LEAVING THE SCENE")), "LEAVING SCENE-ACCIDENT")
                                   .when((col("PD_DESC").contains("NY STATE")) | (col("PD_DESC").contains("NY CITY")) | (col("PD_DESC").contains("NYS")) | (col("PD_DESC").contains("NYC")), "NY STATE LAWS")
                                   .when((col("PD_DESC").contains("DRUG PARAPHERNALIA,   POSSESSE")), "DRUG PARAPHERNALIA, POSSESSION OR SALE")
                                   .when((col("PD_DESC").contains("ESCAPE")), "ESCAPE")
                                   .when(col("PD_DESC").isNull(), "UNKNOWN")
                                   .otherwise(col("PD_DESC")))

df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("DRUG",
                                 when(col("PD_DESC").contains("CONTROLLED SUBSTANCE"), "CONTROLLED SUBSTANCE")
                                 .when(col("PD_DESC").contains("DRUG PARAPHERNALIA"), "PARAPHERNALIA")
                                 .when(col("PD_DESC").contains("MARIJUANA"), "MARIJUANA")
                                 .when(col("PD_DESC").contains("DRUG"), "UNIDENTIFED DRUG")
                                   .otherwise(None))

df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn(
    "AGE_GROUP",
    when(col("AGE_GROUP").isin("<18", "18-24", "25-44", "45-64", "65+"), col("AGE_GROUP"))
    .otherwise(None)
)
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("ARREST_DATE", to_date(col("ARREST_DATE"), "MM/dd/yyyy"))
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("YEAR", year(col("ARREST_DATE"))) \
                      .withColumn("MONTH", month(col("ARREST_DATE")))\
                      .withColumn("DAY", dayofmonth(col("ARREST_DATE")))
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn(
    "PERP_RACE",
    when(col("PERP_RACE") == "AMERICAN INDIAN/ALASKAN NATIVE", "OTHERS")
    .when(col("PERP_RACE") == "BLACK HISPANIC", "HISPANIC")
    .when(col("PERP_RACE") == "WHITE HISPANIC", "HISPANIC")
    .when(col("PERP_RACE") == "OTHER", "OTHERS")
    .when(col("PERP_RACE") == "ASIAN / PACIFIC ISLANDER", "ASIAN")
    .otherwise(col("PERP_RACE"))
)
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn(
    "PERP_SEX",
    when(col("PERP_SEX") == "M", "MALE")
    .when(col("PERP_SEX") == "F", "FEMALE")
    .otherwise(col("PERP_SEX"))
)
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("PD_DESC", "CRIME")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("ARREST_DATE", "DATE")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("AGE_GROUP", "AGE")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("PERP_SEX", "GENDER")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("Latitude", "LATITUDE")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("Longitude", "LONGITUDE")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumnRenamed("PERP_RACE", "RACE")
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("NAME", lit("UNKNOWN"))
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("CITY", lit("NEW YORK"))
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("STATE", lit("NEW YORK"))
df_spark_NYPD_Arrests_data = df_spark_NYPD_Arrests_data.withColumn("WEAPON", lit("UNKNOWN"))

# Normalização do Chicago Crimes
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes.select("Date", "Primary Type", "Latitude", "Longitude")

df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("Primary Type",
                                 when(col("Primary Type").contains("SEX"), "SEX CRIMES")
                                 .when(col("Primary Type").contains("NARCOTIC"), "NARCOTICS & RELATED OFFENSES")
                                 .when(col("Primary Type").contains("NON-CRIMINAL"), "NON - CRIMINAL")
                                 .when(col("Primary Type") == "KIDNAPPING", "KIDNAPPING & RELATED OFFENSES")
                                 .when(col("Primary Type") == "OFFENSE INVOLVING CHILDREN", "OFFENSES RELATED TO CHILDREN")
                                 .when(col("Primary Type") == "OTHER OFFENSE", "OTHERS")
                                 .when(col("Primary Type") == "HOMICIDE", "HOMICIDE & RELATED OFFENSES")
                                 .when(col("Primary Type") == "ASSAULT", "ASSAULT & RELATED OFFENSES")
                                 .when(col("Primary Type").isin("MOTOR VEHICLE THEFT", "ROBBERY", "THEFT", "BURGLARY"), "THEFT & RELATED OFFENSES")
                                 .otherwise(col("Primary Type")))

df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("Date", to_timestamp("Date", "MM/dd/yyyy hh:mm:ss a"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("Date", date_format("Date", "MM/dd/yyyy"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("Date", to_date(col("Date"), "MM/dd/yyyy"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("YEAR", year(col("Date"))) \
                      .withColumn("MONTH", month(col("Date")))\
                      .withColumn("DAY", dayofmonth(col("Date")))

df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("Latitude", when(col("Latitude").isNull(), "41.8781").otherwise(col("Latitude")))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("Longitude", when(col("Longitude").isNull(), "-87.6298").otherwise(col("Longitude")))

df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumnRenamed("Primary Type", "CRIME")
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumnRenamed("Date", "DATE")
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumnRenamed("Latitude", "LATITUDE")
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumnRenamed("Longitude", "LONGITUDE")
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("CITY", lit("CHICAGO"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("STATE", lit("ILLINOIS"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("WEAPON", lit("UNKNOWN"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("NAME", lit("UNKNOWN"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("GENDER", lit("UNKNOWN"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("RACE", lit("UNKNOWN"))
df_spark_Chicago_Crimes_data = df_spark_Chicago_Crimes_data.withColumn("AGE", lit(None))

#Normalização do Los Angeles Crimes 
df_spark_LA_Crimes_data = df_spark_LA_Crimes.select("DATE OCC","Crm Cd Desc","Vict Age", "Vict Sex", "Vict Descent","Weapon Desc", "LAT", "LON")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("Crm Cd Desc",
                                 when(col("Crm Cd Desc") == "ABORTION/ILLEGAL", "ABORTION")
                                 .when(col("Crm Cd Desc") == "CRIMINAL HOMICIDE", "HOMICIDE")
                                 .when(col("Crm Cd Desc") == "OTHER MISCELLANEOUS CRIME", "MISCELLANEOUS PENAL LAW")
                                 .when(col("Crm Cd Desc").contains("THREAT"), "OFFENSES RELATED TO THREATS")
                                 .when((col("Crm Cd Desc").contains("STOLEN")) | (col("Crm Cd Desc").contains("THEFT")), "THEFT & RELATED OFFENSES")
                                 .when(col("Crm Cd Desc").contains("ANIM"), "OFFENSES RELATED TO NATURE")
                                 .when(col("Crm Cd Desc").contains("BATTERY"), "BATTERY")
                                 .when(col("Crm Cd Desc").contains("CHLD"), "RELATED OFFENSES TO CHILDREN")
                                 .when(col("Crm Cd Desc").contains("BURGLARY"), "BURGLARY")
                                 .when(col("Crm Cd Desc").contains("SHOPLIFTING"), "SHOPLIFTING")
                                 .when(col("Crm Cd Desc").contains("CHILD ABUSE"), "CHILD ABUSE")
                                 .when(col("Crm Cd Desc").contains("CHILD ANNOYING"), "CHILD ANNOYING")
                                 .when(col("Crm Cd Desc").contains("CHILD NEGLECT"), "CHILD NEGLECT")
                                 .when(col("Crm Cd Desc").contains("PURSE SNATCHING"), "PURSE SNATCHING")
                                 .when(col("Crm Cd Desc").contains("INTIMATE PARTNER"), "INTIMATE PARTNER ASSAULT")
                                 .when(col("Crm Cd Desc").contains("ASSAULT WITH DEADLY WEAPON"), "ASSAULT WITH DEADLY WEAPON")
                                 .when(col("Crm Cd Desc").contains("BUNCO"), "BUNCO & RELATED OFFENSES")
                                 .when(col("Crm Cd Desc").contains("FRAUD"), "FRAUD & RELATED OFFENSES")
                                 .when(col("Crm Cd Desc").contains("DOCUMENT"), "OFFENSES RELATED TO DOCUMENTS")
                                 .when(col("Crm Cd Desc").contains("DRUNK"), "OFFENSES RELATED TO DRUNK")
                                 .when(col("Crm Cd Desc").contains("HUMAN TRAFFICKING"), "HUMAN TRAFFICKING")
                                 .when(col("Crm Cd Desc").contains("KIDNAPPING"), "KIDNAPPING & RELATED OFFENSES")
                                 .when(col("Crm Cd Desc").contains("LYNCHING"), "OFFENSES RELATED TO LYNCHING")
                                 .when(col("Crm Cd Desc").contains("PICKPOCKET"), "OFFENSES RELATED TO PICKPOCKET")
                                 .when(col("Crm Cd Desc").contains("RAPE"), "RAPE")
                                 .when(col("Crm Cd Desc").contains("SEX"), "SEX CRIMES")
                                 .when(col("Crm Cd Desc").contains("SHOTS"), "SHOTS FIRED")
                                 .when(col("Crm Cd Desc").contains("TILL TAP"), "TILL TAP")
                                 .when(col("Crm Cd Desc").contains("TRESPASSING"), "CRIMINAL TRESPASS")
                                 .when(col("Crm Cd Desc").contains("VANDALISM"), "VANDALISM & RELATED OFFENSES")
                                 .when(col("Crm Cd Desc").contains("VIOLATION"), "VIOLATION & RELATED OFFENSES")
                                 .when((col("Crm Cd Desc") == "FIREARMS RESTRAINING ORDER (FIREARMS RO)") |(col("Crm Cd Desc") == "FIREARMS TEMPORARY RESTRAINING ORDER (TEMP FIREARMS RO)"), "FIREARMS RESTRAINING ORDER & RELATED OFFENSES")
                                 .otherwise(col("Crm Cd Desc")))

df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("DATE OCC", to_timestamp("DATE OCC", "MM/dd/yyyy hh:mm:ss a"))
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("DATE OCC", date_format("DATE OCC", "MM/dd/yyyy"))
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("DATE OCC", to_date(col("DATE OCC"), "MM/dd/yyyy"))
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("YEAR", year(col("DATE OCC"))) \
                      .withColumn("MONTH", month(col("DATE OCC")))\
                      .withColumn("DAY", dayofmonth(col("DATE OCC")))

df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("Vict Age", when(col("Vict Age") < 1, None).otherwise(col("Vict Age")))

df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("Vict Sex",
                                 when(col("Vict Sex") == "M", "MALE")
                                 .when(col("Vict Sex") == "F", "FEMALE")
                                 .otherwise("UNKNOWN"))

df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("Vict Descent",
                                 when(col("Vict Descent") == "A", "ASIAN")
                                 .when(col("Vict Descent") == "B", "BLACK")
                                 .when(col("Vict Descent") == "H", "HISPANIC")
                                 .when(col("Vict Descent") == "W", "WHITE")
                                 .when(col("Vict Descent").isin("-", None), "UNKNOWN")
                                 .otherwise("OTHERS"))

df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("Weapon Desc",
                                 when(col("Weapon Desc").contains("FIREARM"), "FIREARM")
                                 .when(col("Weapon Desc").isin("VERBAL THREAT", "BOMB THREAT"), "OTHERS")
                                 .when(col("Weapon Desc").isNull(), "UNKNOWN")
                                 .when(col("Weapon Desc") == "UNK TYPE SEMIAUTOMATIC ASSAULT RIFLE", "UNKNOWN TYPE SEMIAUTOMATIC ASSAULT RIFLE")
                                 .when(col("Weapon Desc") == "OTHER KNIFE", "OTHER CUTTING INSTRUMENT")
                                 .otherwise(col("Weapon Desc")))

df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("Crm Cd Desc", "CRIME")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("DATE OCC", "DATE")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("Vict Age", "AGE")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("Vict Sex", "GENDER")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("Vict Descent", "RACE")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("Weapon Desc", "WEAPON")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("LAT", "LATITUDE")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumnRenamed("LON", "LONGITUDE")
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("CITY", lit("LOS ANGELES"))
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("STATE", lit("CALIFORNIA"))
df_spark_LA_Crimes_data = df_spark_LA_Crimes_data.withColumn("NAME", lit("UNKNOWN"))


# Normalização do Fatal_Encounters
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.select(
    col("Subject's age"),
    col("Subject's race"),
    col("Subject's gender"),
    col("Location of death (city)"),
    col("Location of death (state)"),
    col("Cause of death"),
    col("Agency responsible for death"),
    col("Date (Year)")
)

# Corrigindo idade: converte para int se for número, senão 0
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("Subject's age",
    when(col("Subject's age").rlike("^\d+$"), col("Subject's age").cast("int"))
    .otherwise(0)
)
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("Agency responsible for death", upper(col("Agency responsible for death")))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("prefixo", col("Agency responsible for death").substr(1, 23))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("prefixo",ltrim(col("prefixo")))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("prefixo",rtrim(col("prefixo")))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("prefixo",regexp_replace(col("prefixo"), "[-,]+$", ""))
janela = Window.partitionBy("prefixo")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("DEPT", first("Agency responsible for death").over(janela))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("DEPT", split("DEPT", ",").getItem(0))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("DEPT",
                                       when(col("DEPT").isNull(), "UNKNOWN")
                                       .otherwise(col("DEPT")))
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("DEPT",ltrim(col("DEPT")))

# Padroniza raça e converte para upper
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("Subject's race",
    when(col("Subject's race").contains("White"), "WHITE")
    .when(col("Subject's race").contains("Black"), "BLACK")
    .when(col("Subject's race").contains("Asian"), "ASIAN")
    .when(col("Subject's race").contains("Hispanic"), "HISPANIC")
    .when(col("Subject's race").isin("Native American/Alaskan", "Middle Eastern", "Race unspecified"), "OTHERS")
    .otherwise("UNKNOWN")
)

# Padroniza gênero e converte para upper
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("Subject's gender",
    when(col("Subject's gender").contains("Male"), "MALE")
    .when(col("Subject's gender").contains("Female"), "FEMALE")
    .otherwise("OTHERS")
)

# Padroniza cidade e converte para upper
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("Location of death (city)",
    when(
        col("Location of death (city)").isNull() |
        col("Location of death (city)").rlike("^\d+$") |
        col("Location of death (city)").rlike("^\d{1,2}/\d{1,2}/\d{2,4}[:]"),
        "UNKNOWN"
    ).otherwise(upper(col("Location of death (city)")))
)

# Dicionário de siglas e seus respectivos estados
state_mapping = {
    "AK": "ALASKA", "AL": "ALABAMA", "AR": "ARKANSAS", "AZ": "ARIZONA", "CA": "CALIFORNIA",
    "CO": "COLORADO", "CT": "CONNECTICUT", "DC": "DISTRICT OF COLUMBIA", "DE": "DELAWARE", "FL": "FLORIDA",
    "GA": "GEORGIA", "HI": "HAWAII", "IA": "IOWA", "ID": "IDAHO", "IL": "ILLINOIS", "IN": "INDIANA",
    "KS": "KANSAS", "KY": "KENTUCKY", "LA": "LOUISIANA", "MA": "MASSACHUSETTS", "MD": "MARYLAND",
    "ME": "MAINE", "MI": "MICHIGAN", "MN": "MINNESOTA", "MO": "MISSOURI", "MS": "MISSISSIPPI",
    "MT": "MONTANA", "NC": "NORTH CAROLINA", "ND": "NORTH DAKOTA", "NE": "NEBRASKA", "NH": "NEW HAMPSHIRE",
    "NJ": "NEW JERSEY", "NM": "NEW MEXICO", "NV": "NEVADA", "NY": "NEW YORK", "OH": "OHIO",
    "OK": "OKLAHOMA", "OR": "OREGON", "PA": "PENNSYLVANIA", "RI": "RHODE ISLAND", "SC": "SOUTH CAROLINA",
    "SD": "SOUTH DAKOTA", "TN": "TENNESSEE", "TX": "TEXAS", "UNKNOWN": "UNKNOWN", "UT": "UTAH",
    "VA": "VIRGINIA", "VT": "VERMONT", "WA": "WASHINGTON", "WI": "WISCONSIN", "WV": "WEST VIRGINIA",
    "WY": "WYOMING"
}

# Criando o mapa com create_map
state_map = create_map(
    *[lit(x) for pair in state_mapping.items() for x in pair]
)

# Aplicando a substituição de siglas para nomes
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn(
    "Location of death (state)",
    when(
        col("Location of death (state)").isNull() |
        col("Location of death (state)").rlike("^\d+$") |
        col("Location of death (state)").rlike("^\d{1,2}/\d{1,2}/\d{2,4}[:]") |
        col("Location of death (state)").isin("Harris"),
        "UNKNOWN"
    ).otherwise(state_map.getItem(upper(col("Location of death (state)"))))
)

# Padroniza causa da morte e converte para upper
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn(
    "Cause of death",
    when(
        col("Cause of death").isNull() |
        col("Cause of death").isin("Pending investigation", "Undetermined", "Other") |
        col("Cause of death").contains("Officers"),
        "UNKNOWN"
    ).otherwise(upper(col("Cause of death")))
)

# Padroniza agência responsável e converte para upper
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn(
    "Agency responsible for death",
    when(col("Agency responsible for death").isNull(), "UNKNOWN")
    .otherwise(upper(col("Agency responsible for death")))
)

# Limpa e formata a data
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumn("Date (Year)",
    regexp_replace(col("Date (Year)"), r'^"|"$', '')
).filter(
    col("Date (Year)").rlike(r"^\d{1,2}/\d{1,2}/\d{4}:")
).withColumn("Date (Year)",
    to_date(
        regexp_extract(col("Date (Year)"), r"^(\d{1,2}/\d{1,2}/\d{4})", 1),
        "M/d/yyyy"
    )
)

df_spark_Fatal_Encounters = df_spark_Fatal_Encounters \
    .withColumn("YEAR", year(col("Date (Year)"))) \
    .withColumn("MONTH", month(col("Date (Year)"))) \
    .withColumn("DAY", dayofmonth(col("Date (Year)")))


df_spark_Police_Killings = df_spark_Police_Killings.select(
    col("Victim's age"),
    col("Victim's race"),
    col("Victim's gender"),
    col("City"),
    col("State"),
    col("Date of Incident (month/day/year)"),
    col("Cause of death"),
    col("Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)"),
    col("Alleged Threat Level (Source: WaPo)"),
    col("Fleeing (Source: WaPo)")
)

# Corrige idade
df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "Victim's age",
    when(col("Victim's age").rlike("^\d+$"), col("Victim's age").cast("int")).otherwise(0)
)

# Corrige raça
df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "Victim's race",
    when(col("Victim's race").isin("Native American", "Pacific Islander"), "OTHERS")
    .when(col("Victim's race").isin("Asian", "Black", "Hispanic", "White"), upper(col("Victim's race")))
    .otherwise("UNKNOWN")
)

# Corrige gênero
df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "Victim's gender",
    when(col("Victim's gender").contains("Male"), "MALE")
    .when(col("Victim's gender").contains("Female"), "FEMALE")
    .otherwise("OTHERS")
)

# Mapeia estados
state_mapping = {
    "AK": "ALASKA",
    "AL": "ALABAMA",
    "AR": "ARKANSAS",
    "AZ": "ARIZONA",
    "CA": "CALIFORNIA",
    "CO": "COLORADO",
    "CT": "CONNECTICUT",
    "DC": "DISTRICT OF COLUMBIA",
    "DE": "DELAWARE",
    "FL": "FLORIDA",
    "GA": "GEORGIA",
    "HI": "HAWAII",
    "IA": "IOWA",
    "ID": "IDAHO",
    "IL": "ILLINOIS",
    "IN": "INDIANA",
    "KS": "KANSAS",
    "KY": "KENTUCKY",
    "LA": "LOUISIANA",
    "MA": "MASSACHUSETTS",
    "MD": "MARYLAND",
    "ME": "MAINE",
    "MI": "MICHIGAN",
    "MN": "MINNESOTA",
    "MO": "MISSOURI",
    "MS": "MISSISSIPPI",
    "MT": "MONTANA",
    "NC": "NORTH CAROLINA",
    "ND": "NORTH DAKOTA",
    "NE": "NEBRASKA",
    "NH": "NEW HAMPSHIRE",
    "NJ": "NEW JERSEY",
    "NM": "NEW MEXICO",
    "NV": "NEVADA",
    "NY": "NEW YORK",
    "OH": "OHIO",
    "OK": "OKLAHOMA",
    "OR": "OREGON",
    "PA": "PENNSYLVANIA",
    "RI": "RHODE ISLAND",
    "SC": "SOUTH CAROLINA",
    "SD": "SOUTH DAKOTA",
    "TN": "TENNESSEE",
    "TX": "TEXAS",
    "UNKNOWN": "UNKNOWN",
    "UT": "UTAH",
    "VA": "VIRGINIA",
    "VT": "VERMONT",
    "WA": "WASHINGTON",
    "WI": "WISCONSIN",
    "WV": "WEST VIRGINIA",
    "WY": "WYOMING"
}

state_map = create_map(*[lit(x) for pair in state_mapping.items() for x in pair])

df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "State",
    when(
        col("State").isNull() |
        ~col("State").isin(*state_mapping.keys()),
        "UNKNOWN"
    ).otherwise(state_map[col("State")])
)

# Corrige causa da morte
df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "Cause of death",
    when(col("Cause of death").isNull(), "UNKNOWN")
    .when(lower(col("Cause of death")).like("%gunshot%"), "GUNSHOT")
    .when(lower(col("Cause of death")).like("%taser%"), "TASER")
    .when(lower(col("Cause of death")).like("%pepper%") | lower(col("Cause of death")).like("%chemical%"), "CHEMICAL")
    .when(lower(col("Cause of death")).like("%beaten%") | lower(col("Cause of death")).like("%bludgeoned%"), "BEATEN")
    .when(lower(col("Cause of death")).like("%restraint%"), "PHYSICAL RESTRAINT")
    .when(lower(col("Cause of death")).like("%vehicle%"), "VEHICLE")
    .when(lower(col("Cause of death")).like("%asphyxiated%"), "ASPHYXIA")
    .when(lower(col("Cause of death")).like("%bomb%"), "EXPLOSION")
    .when(lower(col("Cause of death")).like("%other%") | lower(col("Cause of death")).like("%undetermined%"), "UNKNOWN")
    .otherwise("UNKNOWN")
)


def normalize_city(df_teste_police_killings: DataFrame, col_name: str) -> DataFrame:

    df_teste_police_killings = df_teste_police_killings.withColumn(
        col_name,
        trim(col(col_name))
    ).withColumn(
        col_name,
        regexp_replace(col(col_name), "\\s+", " ")
    )

    df_teste_police_killings = df_teste_police_killings.withColumn(col_name, upper(col(col_name)))

    df_teste_police_killings = df_teste_police_killings.withColumn(
        col_name,
        regexp_replace(col(col_name), "[\\.,/\\-()']", "")
    )

    df_teste_police_killings = df_teste_police_killings.withColumn(
        col_name,
        regexp_replace(col(col_name), "ÃS", "AS")  # adapte para seu caso ou use UDF unicode
    )
    df_teste_police_killings = df_teste_police_killings.withColumn(
        col_name,
        when(
            col(col_name).isin("", "N/A", "UNKNOWN", "UNINCORPORATED", "—"),
            lit("UNKNOWN")
        )
        .when(col(col_name).isNull(), "UNKNONW")
      .otherwise(col(col_name))
    )
    return df_teste_police_killings

df_spark_Police_Killings = normalize_city(df_spark_Police_Killings, "City")

city_corrections = {
    "ST LOUIS": "SAINT LOUIS",
    "FT WORTH": "FORT WORTH",
    # adicione quantos quiser...
}

city_map = create_map(*[lit(x) for pair in city_corrections.items() for x in pair])

df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "City",
    when(col("City").isin(list(city_corrections.keys())), city_map[col("City")])
    .otherwise(col("City"))
)

# Corrige ameaça percebida
df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "Alleged Threat Level (Source: WaPo)",
    when(col("Alleged Threat Level (Source: WaPo)") == "attack", "ATTACK")
    .when(col("Alleged Threat Level (Source: WaPo)").isin("undetermined", "Other"), "OTHER")
    .otherwise("UNKNOWN")
)
df_spark_Police_Killings= df_spark_Police_Killings.withColumn("Fleeing (Source: WaPo)",
                                  when(col("Fleeing (Source: WaPo)").isin("Not fleeing", "not fleeing"), "NOT FLEEING")
                                .when(col("Fleeing (Source: WaPo)").isin("Vechile", "car","Car"), "VECHILE" )
                                .when(col("Fleeing (Source: WaPo)") == "foot", "FOOT").otherwise("UNKNOWN"))

df_spark_Police_Killings = df_spark_Police_Killings.withColumn("Date of Incident (month/day/year)",
                                   when(col("Date of Incident (month/day/year)").isNull(), lit("2200/01/01"))
                                   .otherwise(
                                       date_format(
                                          to_date(col("Date of Incident (month/day/year)"), "MM/dd/yyyy"), "yyyy-MM-dd"
                                   ) ))

valid_weapons = [
    "bb gun",
    "bb gun and vehicle",
    "taser",
    "vehicle",
    "air pistol",
    "axe",
    "axe and knife",
    "barstool",
    "baseball bat",
    "baseball bat and bottle",
    "baseball bat and fireplace poker",
    "baseball bat and knife",
    "baseball bat and screwdriver",
    "bat",
    "bayonet",
    "bean-bag gun",
    "blunt weapon",
    "bottle",
    "fireworks",
    "gun",
    "gun and car",
    "gun and explosives",
    "gun and hatchet",
    "gun and knife",
    "gun and knives",
    "gun and sword",
    "gun and vehicle",
    "hammer",
    "hammer and knife",
    "hand torch",
    "hatchet",
    "hockey stick",
    "hot glue gun"
]
# Transformação

df_spark_Police_Killings = df_spark_Police_Killings.withColumn(
    "Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)",
    when(col("Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)").isin
     (
    "bb gun",
    "bb gun and vehicle",
    "taser",
    "vehicle",
    "air pistol",
    "axe",
    "axe and knife",
    "barstool",
    "baseball bat",
    "baseball bat and bottle",
    "baseball bat and fireplace poker",
    "baseball bat and knife",
    "baseball bat and screwdriver",
    "bat",
    "bayonet",
    "bean-bag gun",
    "blunt weapon",
    "bottle",
    "fireworks",
    "gun",
    "gun and car",
    "gun and explosives",
    "gun and hatchet",
    "gun and knife",
    "gun and knives",
    "gun and sword",
    "gun and vehicle",
    "hammer",
    "hammer and knife",
    "hand torch",
    "hatchet",
    "hockey stick",
    "hot glue gun"
     ), upper(col("Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)")))
    .when(col("Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)").contains("garden"), upper(col("Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)")))
    .otherwise("UNKNOWN")
)

# Renomeia colunas do killings
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Victim's age", "AGE")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Victim's race", "RACE")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Victim's gender", "GENDER")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Date of Incident (month/day/year)", "DATE")
df_spark_Police_Killings= df_spark_Police_Killings.withColumnRenamed("City", "CITY")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("State", "STATE")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Cause of death", "CAUSE")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)", "WEAPON")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Alleged Threat Level (Source: WaPo)", "THREAT")
df_spark_Police_Killings = df_spark_Police_Killings.withColumnRenamed("Fleeing (Source: WaPo)", "FLEEING")

#Renomeia do Fatal
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Subject's age", "AGE")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Subject's race", "RACE")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Subject's gender", "GENDER")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Location of death (city)", "CITY")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Location of death (state)", "STATE")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Cause of death", "CAUSE")
df_spark_Fatal_Encounters = df_spark_Fatal_Encounters.withColumnRenamed("Agency responsible for death", "AGENCY")

#Normalização do  Police Deaths
df_spark_Police_Deaths_data = df_spark_Police_Deaths.select("person", "dept_name", "cause_short", "date", "state")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("person", upper(col("person")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("dept_name", upper(col("dept_name")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("cause_short", upper(col("cause_short")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("cause_short", split("cause_short", ": ").getItem(1))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("cause_short", when(col("cause_short").isNull(), "UNKNOWN").otherwise(col("cause_short")))

df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("state",ltrim(col("state")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("state", when(length(col("state")) == 2, col("state")).otherwise("UNKNOWN"))

df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("LATITUDE",
    when(col("state") == "AK", "61.3850")
    .when(col("state") == "AL", "32.7990")
    .when(col("state") == "AR", "34.9513")
    .when(col("state") == "AZ", "33.7712")
    .when(col("state") == "CA", "36.1700")
    .when(col("state") == "CO", "39.0646")
    .when(col("state") == "CT", "41.5834")
    .when(col("state") == "DC", "38.8964")
    .when(col("state") == "DE", "39.3498")
    .when(col("state") == "FL", "27.8333")
    .when(col("state") == "GA", "32.9866")
    .when(col("state") == "HI", "21.1098")
    .when(col("state") == "IA", "42.0046")
    .when(col("state") == "ID", "44.2394")
    .when(col("state") == "IL", "40.3363")
    .when(col("state") == "IN", "39.8647")
    .when(col("state") == "KS", "38.5111")
    .when(col("state") == "KY", "37.6690")
    .when(col("state") == "LA", "31.1801")
    .when(col("state") == "MA", "42.2373")
    .when(col("state") == "MD", "39.0724")
    .when(col("state") == "ME", "44.6074")
    .when(col("state") == "MI", "43.3504")
    .when(col("state") == "MN", "45.7326")
    .when(col("state") == "MO", "38.4623")
    .when(col("state") == "MS", "32.7673")
    .when(col("state") == "MT", "46.9048")
    .when(col("state") == "NC", "35.6411")
    .when(col("state") == "ND", "47.5362")
    .when(col("state") == "NE", "41.1289")
    .when(col("state") == "NH", "43.4108")
    .when(col("state") == "NJ", "40.3140")
    .when(col("state") == "NM", "34.8375")
    .when(col("state") == "NV", "38.4199")
    .when(col("state") == "NY", "42.1497")
    .when(col("state") == "OH", "40.3736")
    .when(col("state") == "OK", "35.5376")
    .when(col("state") == "OR", "44.5672")
    .when(col("state") == "PA", "40.5773")
    .when(col("state") == "RI", "41.6772")
    .when(col("state") == "SC", "33.8191")
    .when(col("state") == "SD", "44.2853")
    .when(col("state") == "TN", "35.7449")
    .when(col("state") == "TX", "31.1060")
    .when(col("state") == "UT", "40.1135")
    .when(col("state") == "VA", "37.7680")
    .when(col("state") == "VT", "44.0407")
    .when(col("state") == "WA", "47.3917")
    .when(col("state") == "WI", "44.2563")
    .when(col("state") == "WV", "38.4680")
    .when(col("state") == "WY", "42.7475")
    .otherwise("NULL")
)

df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("LONGITUDE",
    when(col("state") == "AK", "-152.2683")
    .when(col("state") == "AL", "-86.8073")
    .when(col("state") == "AR", "-92.3809")
    .when(col("state") == "AZ", "-111.3877")
    .when(col("state") == "CA", "-119.7462")
    .when(col("state") == "CO", "-105.5511")
    .when(col("state") == "CT", "-72.7622")
    .when(col("state") == "DC", "-77.0262")
    .when(col("state") == "DE", "-75.5148")
    .when(col("state") == "FL", "-81.7170")
    .when(col("state") == "GA", "-83.6487")
    .when(col("state") == "HI", "-157.5311")
    .when(col("state") == "IA", "-93.2140")
    .when(col("state") == "ID", "-114.5103")
    .when(col("state") == "IL", "-89.0022")
    .when(col("state") == "IN", "-86.2604")
    .when(col("state") == "KS", "-96.8005")
    .when(col("state") == "KY", "-84.6514")
    .when(col("state") == "LA", "-91.8749")
    .when(col("state") == "MA", "-71.5314")
    .when(col("state") == "MD", "-76.7902")
    .when(col("state") == "ME", "-69.3977")
    .when(col("state") == "MI", "-84.5603")
    .when(col("state") == "MN", "-94.6859")
    .when(col("state") == "MO", "-92.3020")
    .when(col("state") == "MS", "-89.6812")
    .when(col("state") == "MT", "-110.3261")
    .when(col("state") == "NC", "-79.8431")
    .when(col("state") == "ND", "-99.7930")
    .when(col("state") == "NE", "-98.2883")
    .when(col("state") == "NH", "-71.5653")
    .when(col("state") == "NJ", "-74.5089")
    .when(col("state") == "NM", "-106.2371")
    .when(col("state") == "NV", "-117.1219")
    .when(col("state") == "NY", "-74.9384")
    .when(col("state") == "OH", "-82.7755")
    .when(col("state") == "OK", "-96.9247")
    .when(col("state") == "OR", "-122.1269")
    .when(col("state") == "PA", "-77.2640")
    .when(col("state") == "RI", "-71.5101")
    .when(col("state") == "SC", "-80.9066")
    .when(col("state") == "SD", "-99.4632")
    .when(col("state") == "TN", "-86.7489")
    .when(col("state") == "TX", "-97.6475")
    .when(col("state") == "UT", "-111.8535")
    .when(col("state") == "VA", "-78.2057")
    .when(col("state") == "VT", "-72.7093")
    .when(col("state") == "WA", "-121.5708")
    .when(col("state") == "WI", "-89.6385")
    .when(col("state") == "WV", "-80.9696")
    .when(col("state") == "WY", "-107.2085")
    .otherwise("NULL")
)

df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("state",
                                         when(col("state") == "AK", "ALASKA")
                                         .when(col("state") == "AL", "ALABAMA")
                                         .when(col("state") == "AR", "ARKANSAS")
                                         .when(col("state") == "AZ", "ARIZONA")
                                         .when(col("state") == "CA", "CALIFORNIA")
                                         .when(col("state") == "CO", "COLORADO")
                                         .when(col("state") == "CT", "CONNECTICUT")
                                         .when(col("state") == "DC", "DISTRICT OF COLUMBIA")
                                         .when(col("state") == "DE", "DELAWARE")
                                         .when(col("state") == "FL", "FLORIDA")
                                         .when(col("state") == "GA", "GEORGIA")
                                         .when(col("state") == "HI", "HAWAII")
                                         .when(col("state") == "IA", "IOWA")
                                         .when(col("state") == "ID", "IDAHO")
                                         .when(col("state") == "IL", "ILLINOIS")
                                         .when(col("state") == "IN", "INDIANA")
                                         .when(col("state") == "KS", "KANSAS")
                                         .when(col("state") == "KY", "KENTUCKY")
                                         .when(col("state") == "LA", "LOUISIANA")
                                         .when(col("state") == "MA", "MASSACHUSETTS")
                                         .when(col("state") == "MD", "MARYLAND")
                                         .when(col("state") == "ME", "MAINE")
                                         .when(col("state") == "MI", "MICHIGAN")
                                         .when(col("state") == "MN", "MINNESOTA")
                                         .when(col("state") == "MO", "MISSOURI")
                                         .when(col("state") == "MS", "MISSISSIPPI")
                                         .when(col("state") == "MT", "MONTANA")
                                         .when(col("state") == "NC", "NORTH CAROLINA")
                                         .when(col("state") == "ND", "NORTH DAKOTA")
                                         .when(col("state") == "NE", "NEBRASKA")
                                         .when(col("state") == "NH", "NEW HAMPSHIRE")
                                         .when(col("state") == "NJ", "NEW JERSEY")
                                         .when(col("state") == "NM", "NEW MEXICO")
                                         .when(col("state") == "NV", "NEVADA")
                                         .when(col("state") == "NY", "NEW YORK")
                                         .when(col("state") == "OH", "OHIO")
                                         .when(col("state") == "OK", "OKLAHOMA")
                                         .when(col("state") == "OR", "OREGON")
                                         .when(col("state") == "PA", "PENNSYLVANIA")
                                         .when(col("state") == "RI", "RHODE ISLAND")
                                         .when(col("state") == "SC", "SOUTH CAROLINA")
                                         .when(col("state") == "SD", "SOUTH DAKOTA")
                                         .when(col("state") == "TN", "TENNESSEE")
                                         .when(col("state") == "TX", "TEXAS")
                                         .when(col("state") == "US", "UNITED STATES")
                                         .when(col("state") == "UT", "UTAH")
                                         .when(col("state") == "VA", "VIRGINIA")
                                         .when(col("state") == "VT", "VERMONT")
                                         .when(col("state") == "WA", "WASHINGTON")
                                         .when(col("state") == "WI", "WISCONSIN")
                                         .when(col("state") == "WV", "WEST VIRGINIA")
                                         .when(col("state") == "WY", "WYOMING")
                                         .otherwise(col("state")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("state", when(length(col("state")) == 2, "OTHERS").otherwise(col("state")))

df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn(
    "date",
    date_format(to_date(col("date"), "yyyy-MM-dd"), "MM/dd/yyyy")
)
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("date", to_date(col("date"), "MM/dd/yyyy"))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("YEAR", year(col("date"))) \
                      .withColumn("MONTH", month(col("date")))\
                      .withColumn("DAY", dayofmonth(col("date")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("dept_name",ltrim(col("dept_name")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("prefixo", col("dept_name").substr(1, 23))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("prefixo",rtrim(col("prefixo")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("prefixo",regexp_replace(col("prefixo"), "[-,]+$", ""))
janela_dept = Window.partitionBy("prefixo")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("agencia_padronizada", first("dept_name").over(janela_dept))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("agencia_padronizada", split("agencia_padronizada", ",").getItem(0))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("agencia_padronizada",
                                       when(col("agencia_padronizada").isNull(), "UNKNOWN")
                                       .otherwise(col("agencia_padronizada")))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("agencia_padronizada", split("agencia_padronizada", "-").getItem(0))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("agencia_padronizada",rtrim(col("agencia_padronizada")))

df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.select("person", "agencia_padronizada", "cause_short", "date", "state", "LATITUDE", "LONGITUDE", "YEAR", "MONTH", "DAY")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumnRenamed("person", "NAME")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumnRenamed("date", "DATE")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumnRenamed("cause_short", "CAUSE")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumnRenamed("state", "STATE")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumnRenamed("agencia_padronizada", "DEPT")
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("CITY", lit("UNKNOWN"))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("AGE", lit(None))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("GENDER", lit("UNKNOWN"))
df_spark_Police_Deaths_data = df_spark_Police_Deaths_data.withColumn("RACE", lit("UNKNOWN"))

df_spark_Shootings = df_spark_Shootings.select("date", "manner_of_death", "armed", "age", "gender", "race", "city", "state", "signs_of_mental_illness", "threat_level", "flee", "body_camera")

df_spark_Shootings = df_spark_Shootings.withColumn("YEAR", year(col("date"))) \
                      .withColumn("MONTH", month(col("date")))\
                      .withColumn("DAY", dayofmonth(col("date")))

df_spark_Shootings = df_spark_Shootings.withColumn("manner_of_death",upper(col("manner_of_death")))

df_spark_Shootings = df_spark_Shootings.withColumn(
    "armed",
    when(col("armed").isNull(), "UNKNOWN")
    .otherwise(upper(col("armed"))))

df_spark_Shootings= df_spark_Shootings.withColumn("threat_level",  when(col("threat_level") == "attack", "ATTACK")
    .when(col("threat_level").isin("undetermined", "Other"), "OTHER")
    .otherwise("UNKNOWN"))

df_spark_Shootings = df_spark_Shootings.withColumn("LATITUDE",
    when(col("state") == "AK", "61.3850")
    .when(col("state") == "AL", "32.7990")
    .when(col("state") == "AR", "34.9513")
    .when(col("state") == "AZ", "33.7712")
    .when(col("state") == "CA", "36.1700")
    .when(col("state") == "CO", "39.0646")
    .when(col("state") == "CT", "41.5834")
    .when(col("state") == "DC", "38.8964")
    .when(col("state") == "DE", "39.3498")
    .when(col("state") == "FL", "27.8333")
    .when(col("state") == "GA", "32.9866")
    .when(col("state") == "HI", "21.1098")
    .when(col("state") == "IA", "42.0046")
    .when(col("state") == "ID", "44.2394")
    .when(col("state") == "IL", "40.3363")
    .when(col("state") == "IN", "39.8647")
    .when(col("state") == "KS", "38.5111")
    .when(col("state") == "KY", "37.6690")
    .when(col("state") == "LA", "31.1801")
    .when(col("state") == "MA", "42.2373")
    .when(col("state") == "MD", "39.0724")
    .when(col("state") == "ME", "44.6074")
    .when(col("state") == "MI", "43.3504")
    .when(col("state") == "MN", "45.7326")
    .when(col("state") == "MO", "38.4623")
    .when(col("state") == "MS", "32.7673")
    .when(col("state") == "MT", "46.9048")
    .when(col("state") == "NC", "35.6411")
    .when(col("state") == "ND", "47.5362")
    .when(col("state") == "NE", "41.1289")
    .when(col("state") == "NH", "43.4108")
    .when(col("state") == "NJ", "40.3140")
    .when(col("state") == "NM", "34.8375")
    .when(col("state") == "NV", "38.4199")
    .when(col("state") == "NY", "42.1497")
    .when(col("state") == "OH", "40.3736")
    .when(col("state") == "OK", "35.5376")
    .when(col("state") == "OR", "44.5672")
    .when(col("state") == "PA", "40.5773")
    .when(col("state") == "RI", "41.6772")
    .when(col("state") == "SC", "33.8191")
    .when(col("state") == "SD", "44.2853")
    .when(col("state") == "TN", "35.7449")
    .when(col("state") == "TX", "31.1060")
    .when(col("state") == "UT", "40.1135")
    .when(col("state") == "VA", "37.7680")
    .when(col("state") == "VT", "44.0407")
    .when(col("state") == "WA", "47.3917")
    .when(col("state") == "WI", "44.2563")
    .when(col("state") == "WV", "38.4680")
    .when(col("state") == "WY", "42.7475")
    .otherwise("NULL")
)

df_spark_Shootings = df_spark_Shootings.withColumn("LONGITUDE",
    when(col("state") == "AK", "-152.2683")
    .when(col("state") == "AL", "-86.8073")
    .when(col("state") == "AR", "-92.3809")
    .when(col("state") == "AZ", "-111.3877")
    .when(col("state") == "CA", "-119.7462")
    .when(col("state") == "CO", "-105.5511")
    .when(col("state") == "CT", "-72.7622")
    .when(col("state") == "DC", "-77.0262")
    .when(col("state") == "DE", "-75.5148")
    .when(col("state") == "FL", "-81.7170")
    .when(col("state") == "GA", "-83.6487")
    .when(col("state") == "HI", "-157.5311")
    .when(col("state") == "IA", "-93.2140")
    .when(col("state") == "ID", "-114.5103")
    .when(col("state") == "IL", "-89.0022")
    .when(col("state") == "IN", "-86.2604")
    .when(col("state") == "KS", "-96.8005")
    .when(col("state") == "KY", "-84.6514")
    .when(col("state") == "LA", "-91.8749")
    .when(col("state") == "MA", "-71.5314")
    .when(col("state") == "MD", "-76.7902")
    .when(col("state") == "ME", "-69.3977")
    .when(col("state") == "MI", "-84.5603")
    .when(col("state") == "MN", "-94.6859")
    .when(col("state") == "MO", "-92.3020")
    .when(col("state") == "MS", "-89.6812")
    .when(col("state") == "MT", "-110.3261")
    .when(col("state") == "NC", "-79.8431")
    .when(col("state") == "ND", "-99.7930")
    .when(col("state") == "NE", "-98.2883")
    .when(col("state") == "NH", "-71.5653")
    .when(col("state") == "NJ", "-74.5089")
    .when(col("state") == "NM", "-106.2371")
    .when(col("state") == "NV", "-117.1219")
    .when(col("state") == "NY", "-74.9384")
    .when(col("state") == "OH", "-82.7755")
    .when(col("state") == "OK", "-96.9247")
    .when(col("state") == "OR", "-122.1269")
    .when(col("state") == "PA", "-77.2640")
    .when(col("state") == "RI", "-71.5101")
    .when(col("state") == "SC", "-80.9066")
    .when(col("state") == "SD", "-99.4632")
    .when(col("state") == "TN", "-86.7489")
    .when(col("state") == "TX", "-97.6475")
    .otherwise("NULL")
)


df_spark_Shootings = df_spark_Shootings.withColumn("state",
                                         when(col("state") == "AK", "ALASKA")
                                         .when(col("state") == "AL", "ALABAMA")
                                         .when(col("state") == "AR", "ARKANSAS")
                                         .when(col("state") == "AZ", "ARIZONA")
                                         .when(col("state") == "CA", "CALIFORNIA")
                                         .when(col("state") == "CO", "COLORADO")
                                         .when(col("state") == "CT", "CONNECTICUT")
                                         .when(col("state") == "DC", "DISTRICT OF COLUMBIA")
                                         .when(col("state") == "DE", "DELAWARE")
                                         .when(col("state") == "FL", "FLORIDA")
                                         .when(col("state") == "GA", "GEORGIA")
                                         .when(col("state") == "HI", "HAWAII")
                                         .when(col("state") == "IA", "IOWA")
                                         .when(col("state") == "ID", "IDAHO")
                                         .when(col("state") == "IL", "ILLINOIS")
                                         .when(col("state") == "IN", "INDIANA")
                                         .when(col("state") == "KS", "KANSAS")
                                         .when(col("state") == "KY", "KENTUCKY")
                                         .when(col("state") == "LA", "LOUISIANA")
                                         .when(col("state") == "MA", "MASSACHUSETTS")
                                         .when(col("state") == "MD", "MARYLAND")
                                         .when(col("state") == "ME", "MAINE")
                                         .when(col("state") == "MI", "MICHIGAN")
                                         .when(col("state") == "MN", "MINNESOTA")
                                         .when(col("state") == "MO", "MISSOURI")
                                         .when(col("state") == "MS", "MISSISSIPPI")
                                         .when(col("state") == "MT", "MONTANA")
                                         .when(col("state") == "NC", "NORTH CAROLINA")
                                         .when(col("state") == "ND", "NORTH DAKOTA")
                                         .when(col("state") == "NE", "NEBRASKA")
                                         .when(col("state") == "NH", "NEW HAMPSHIRE")
                                         .when(col("state") == "NJ", "NEW JERSEY")
                                         .when(col("state") == "NM", "NEW MEXICO")
                                         .when(col("state") == "NV", "NEVADA")
                                         .when(col("state") == "NY", "NEW YORK")
                                         .when(col("state") == "OH", "OHIO")
                                         .when(col("state") == "OK", "OKLAHOMA")
                                         .when(col("state") == "OR", "OREGON")
                                         .when(col("state") == "PA", "PENNSYLVANIA")
                                         .when(col("state") == "RI", "RHODE ISLAND")
                                         .when(col("state") == "SC", "SOUTH CAROLINA")
                                         .when(col("state") == "SD", "SOUTH DAKOTA")
                                         .when(col("state") == "TN", "TENNESSEE")
                                         .when(col("state") == "TX", "TEXAS")
                                         .when(col("state") == "US", "UNITED STATES")
                                         .when(col("state") == "UT", "UTAH")
                                         .when(col("state") == "VA", "VIRGINIA")
                                         .when(col("state") == "VT", "VERMONT")
                                         .when(col("state") == "WA", "WASHINGTON")
                                         .when(col("state") == "WI", "WISCONSIN")
                                         .when(col("state") == "WV", "WEST VIRGINIA")
                                         .when(col("state") == "WY", "WYOMING")
                                         .otherwise(col("state")))

df_spark_Shootings = df_spark_Shootings.withColumn("gender", when(col("gender") == "M", "MALE")
                                      .when(col("gender") == "F", "FEMALE")
                                      .otherwise("UNKNOWN"))

df_spark_Shootings = df_spark_Shootings.withColumn("race", when(col("race") == "W", "WHITE")
                                      .when(col("race") == "B", "BLACK")
                                      .when(col("race") == "A", "ASIAN")
                                      .when(col("race") == "H", "HISPANIC")
                                      .when(col("race") == "N", "OTHERS")
                                      .when(col("race") == "O", "OTHERS")
                                      .otherwise("UNKNOWN"))

df_spark_Shootings = df_spark_Shootings.withColumn("flee", when(col("flee").isNull(), "UNKNOWN")
                                      .otherwise(col("flee")))
df_spark_Shootings = df_spark_Shootings.withColumn("flee", upper(col("flee")))

#Renomeia as colunas de shootings 
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("manner_of_death", "CAUSE")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("armed", "WEAPON")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("age", "AGE")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("gender", "GENDER")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("race", "RACE")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("city", "CITY")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("state", "STATE")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("threat_level", "THREAT_LEVEL")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("flee", "FLEE")
df_spark_Shootings = df_spark_Shootings.withColumnRenamed("body_camera", "BODY_CAMERA")

# Exibição das alterações feitas nos etls
df_spark_Dallas_Arrests_data.show(truncate=False)
df_spark_NYPD_Arrests_data.show(truncate=False)
df_spark_Chicago_Crimes_data.show(truncate=False)
df_spark_LA_Crimes_data.show(truncate=False)
df_spark_Fatal_Encounters.show(truncate=False)
df_spark_Police_Killings.show(truncate=False)
df_spark_Police_Deaths_data.show(truncate=False)
df_spark_Shootings.show(truncate=False)