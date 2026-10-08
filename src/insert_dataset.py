#ÁLVARO BILBAO PARDO
#inserta_dataset.py

import json
import pymysql
from pymongo import MongoClient
from config import *

def pasar_fecha(review_time):
    partes = review_time.split(" ")
    mes = partes[0]
    dia = partes[1].replace(",", "")
    ano = partes[2]

    if len(dia) == 1:
        dia = "0" + dia

    fecha = ano + "-" + mes + "-" + dia
    return fecha


def insertar_nuevo_dataset(ruta_fichero, tipo):
    client = MongoClient(mongo_uri)
    db = client[db_mongo]
    coleccion_mongo = db[coleccion]

    conexion = pymysql.connect(host=host, user=user, password=password, database=db_sql)
    cursor = conexion.cursor()

    sql_usuario = """INSERT INTO USUARIO (reviewer_id, reviewer_name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE reviewer_name = VALUES(reviewer_name)"""

    sql_articulo = """INSERT INTO ARTICULO (asin, tipo)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE tipo = VALUES(tipo)"""

    sql_review = """INSERT INTO REVIEW (reviewer_id, asin, unix_review_time, overall, review_time)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    overall = VALUES(overall),
    review_time = VALUES(review_time)"""

    with open(ruta_fichero) as f:
        for linea in f:
            doc = json.loads(linea)

            reviewer_id = doc["reviewerID"]
            if "reviewerName" in doc:
                reviewer_name = doc["reviewerName"]
            else:
                reviewer_name = ""

            asin = doc["asin"]
            overall = doc["overall"]
            unix_review_time = doc["unixReviewTime"]
            review_time = doc["reviewTime"]

            review_time_fecha = pasar_fecha(review_time)

            cursor.execute(sql_usuario, (reviewer_id, reviewer_name))
            cursor.execute(sql_articulo, (asin, tipo))
            cursor.execute(sql_review, (reviewer_id, asin, unix_review_time, overall, review_time_fecha))

            documento_mongo = {
                "reviewer_id": reviewer_id,
                "asin": asin,
                "unix_review_time": unix_review_time,
                "reviewText": doc["reviewText"],
                "summary": doc["summary"],
                "helpful": doc["helpful"]}

            coleccion_mongo.insert_one(documento_mongo)

    conexion.commit()
    cursor.close()
    conexion.close()
    client.close()


if __name__ == "__main__":
    insertar_nuevo_dataset(ruta_grocery_and_gourmet_food, "Grocery and Gourmet Food")