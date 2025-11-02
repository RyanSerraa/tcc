import psycopg2
from psycopg2.extras import DictCursor
from typing import Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class DB:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def get_connection(self, db_url: str) -> psycopg2.extensions.connection:
        return psycopg2.connect(db_url, cursor_factory=DictCursor)

    def close_connection(self, connection: psycopg2.extensions.connection):
        if connection:
            connection.close()

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None):
        connection = self.get_connection(self.db_url)
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
        except Exception as e:
            print("Error executing query:", e)
            result = []
        self.close_connection(connection)
        return result

    def getExemplaryData(self):
        consultas = [
            "SELECT * FROM vprisao v WHERE (v.arma_usada IS NOT NULL AND v.droga IS NOT NULL AND v.data_prisao = '2020-01-21' AND v.sexo_criminoso = 'FEMININO') OR (v.nome_crime = 'VENDA DE MACONHA' AND v.data_prisao = '2010-09-01' AND v.raca_criminoso = 'BRANCO' AND v.faixa_etaria_criminoso = '1 - 17') ORDER BY raca_criminoso DESC LIMIT 2;",
            "SELECT * FROM vcrime v WHERE (v.arma_usada = 'ESPANCAMENTO' AND v.data_crime = '2016-01-06' AND v.nome_crime = 'AGRESSÃO DE PARCEIRO ÍNTIMO' AND v.faixa_etaria_criminoso = '18 - 24' AND v.raca_criminoso = 'NEGRO') OR (v.arma_usada = 'ADAGA' AND v.data_crime = '2011-08-31') ORDER BY data_crime DESC LIMIT 2;",
            "SELECT * FROM vmortepolicial v WHERE (v.departamento_policial = 'ETOWAH COUNTY SHERIFFS OFFICE' AND v.data_morte = '1997-10-10') OR v.departamento_policial = 'MIAMISBURG POLICE DEPARTMENT';",
            "SELECT * FROM vconfrontofatal v WHERE (v.departamento_policial = 'PAWTUCKET POLICE DEPARTMENT' AND v.data_morte =  '2018-07-09') OR (v.departamento_policial = 'LEXINGTON COUNTY SHERIFF''S DEPARTMENT' AND v.data_morte = '2016-01-08');",
            "SELECT * FROM vtiroteio v WHERE (v.arma_usada = 'FACA' AND v.status_fuga = 'VEÍCULO' AND v.policial_com_camera IS TRUE AND v.sexo_vitima = 'FEMININO') OR (v.status_ameaca = 'DESCONHECIDO' AND v.arma_usada = 'DESARMADO' AND V.status_fuga = 'A PÉ' AND V.data_morte = '2016-03-12');",
        ]
        with ThreadPoolExecutor(max_workers=5) as executor:
            resultados = list(executor.map(self.execute_query, consultas))
            tables = {
                "vPrisao": resultados[0],
                "vCrime": resultados[1],
                "vMortePolicial": resultados[2],
                "vConfrontoFatal": resultados[3],
                "vTiroteio": resultados[4],
            }
            dataframes = {key: pd.DataFrame(value) for key, value in tables.items()}
            return dataframes
