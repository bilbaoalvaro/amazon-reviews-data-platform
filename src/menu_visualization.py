#ÁLVARO BILBAO PARDO 
#menu_visualizacion.py

import pymysql
from pymongo import MongoClient
from config import *
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#Cartel puramente decorativo 
def imprimir_cartel():
    print("""
     __  __ ______ _   _ _    _  __      _______  _____ _    _         _      _____ ______         _____ _____ ____  _   _ 
    |  \/  |  ____| \ | | |  | | \ \    / /_   _|/ ____| |  | |  /\   | |    |_   _|___  /   /\   / ____|_   _/ __ \| \ | |
    | \  / | |__  |  \| | |  | |  \ \  / /  | | | (___ | |  | | /  \  | |      | |    / /   /  \ | |      | || |  | |  \| |
    | |\/| |  __| | . ` | |  | |   \ \/ /   | |  \___ \| |  | |/ /\ \ | |      | |   / /   / /\ \| |      | || |  | | . ` |
    | |  | | |____| |\  | |__| |    \  /   _| |_ ____) | |__| / ____ \| |____ _| |_ / /__ / ____ \ |____ _| || |__| | |\  |
    |_|  |_|______|_| \_|\____/      \/   |_____|_____/ \____/_/    \_\______|_____/_____/_/    \_\_____|_____\____/|_| \_|
                                                                                                                            
                                                                                                                            """)
    print("""
                 ▗▄▖ ▗▖  ▗▖  ▗▖ ▗▄▖ ▗▄▄▖  ▗▄▖     ▗▄▄▖ ▗▄▄▄▖▗▖   ▗▄▄▖  ▗▄▖  ▗▄▖     ▗▄▄▖  ▗▄▖ ▗▄▄▖ ▗▄▄▄   ▗▄▖     
                ▐▌ ▐▌▐▌  ▐▌  ▐▌▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌  █  ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌  █ ▐▌ ▐▌    
                ▐▛▀▜▌▐▌  ▐▌  ▐▌▐▛▀▜▌▐▛▀▚▖▐▌ ▐▌    ▐▛▀▚▖  █  ▐▌   ▐▛▀▚▖▐▛▀▜▌▐▌ ▐▌    ▐▛▀▘ ▐▛▀▜▌▐▛▀▚▖▐▌  █ ▐▌ ▐▌    
                ▐▌ ▐▌▐▙▄▄▖▝▚▞▘ ▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘    ▐▙▄▞▘▗▄█▄▖▐▙▄▄▖▐▙▄▞▘▐▌ ▐▌▝▚▄▞▘    ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▙▄▄▀ ▝▚▄▞▘    
                                                                                                        
                                                                                                        
                                                                                                        """)


#Nos conectamos a MySQL y a MongoDB
def conectar_mysql():
    return pymysql.connect(host=host, user=user, password=password, database=db_sql)


def conectar_mongodb():
    client = MongoClient(mongo_uri)
    db = client[db_mongo]
    return db[coleccion]

#Creamos un diccionario con los tipos de productos para poder elegir cuál queremos estudiar en las consultas
tipos = {"1": "Video Games", "2": "Toys and Games", "3": "Digital Music", "4": "Musical Instruments"}

def pedir_tipo(permitir_todo=True): 
    if permitir_todo: #Si la consulta permite elegir la ocpión de todos los productos a la vez entonces añadimos este caso
        print("0 - Todo")
    for clave, nombre in tipos.items():
        print(f"{clave} - {nombre}") #Imprimimos todas las opción del diccionario con su clave-valor respectiva
    print("s - salir") #Además, incluimos la opción de salir de esta consulta

    while True:
        opcion = input("Selecciona una categoría:").strip().lower()
        if opcion == "s":
            return None #Salimos sin hacer nada
        if permitir_todo and opcion == "0":
            return "todo" #Elegimos la opción todo
        if opcion in tipos:
            return tipos[opcion] #Buscamos en el diccionario el valor (tipo de producto) que tiene esa clave numérica
        print("La opción elegida no es válida! Inténtelo otra vez!")


#CONSULTA 1
def evolucion_reviews_ano():
    print("")
    print("La evolución de reviews por años")
    tipo = pedir_tipo(permitir_todo=True)
    if tipo is None:
        return

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if tipo == "todo":
        sql = """
            SELECT YEAR(review_time) AS ano, COUNT(*)
            FROM REVIEW
            GROUP BY ano
            ORDER BY ano
        """
        cursor.execute(sql)
        titulo = "Reviews por año de todos los productos"
    else:
        sql = """
            SELECT YEAR(r.review_time) AS ano, COUNT(*)
            FROM REVIEW r
            JOIN ARTICULO a ON r.asin = a.asin
            WHERE a.tipo = %s
            GROUP BY ano
            ORDER BY ano
        """
        cursor.execute(sql, (tipo,))
        titulo = f"Reviews por año de {tipo}"

    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()

    anos = [] #Metemos en unas listas todos los resultados para poder graficarlos luego
    reviews = []

    for elemento in resultado:
        anos.append(str(elemento[0]))
        reviews.append(elemento[1])

    plt.bar(anos, reviews)
    plt.title(titulo)
    plt.xlabel("Años")
    plt.ylabel("Número de reviews")
    plt.xticks(rotation=45)
    plt.show()


#CONSULTA 2
def evolucion_popularidad():
    print("Evolución de la popularidad de los artículos")
    tipo = pedir_tipo(permitir_todo=True)
    if tipo is None: #para salir
        return

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if tipo == "todo":
        sql = """
            SELECT asin, COUNT(*)
            FROM REVIEW
            GROUP BY asin
            ORDER BY COUNT(*) DESC
        """
        cursor.execute(sql)
        titulo = "Evolución de popularidad de todos los productos"
    else:
        sql = """
            SELECT r.asin, COUNT(*)
            FROM REVIEW r
            JOIN ARTICULO a ON r.asin = a.asin
            WHERE a.tipo = %s
            GROUP BY r.asin
            ORDER BY COUNT(*) DESC
        """
        cursor.execute(sql, (tipo,))
        titulo = f"Evolución de la popularidad de {tipo}"

    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    popularidades = []

    for elemento in resultado:
        popularidades.append(elemento[1])

    plt.plot(range(len(popularidades)), popularidades)
    plt.title(titulo)
    plt.xlabel("Artículos")
    plt.ylabel("Número de reviews")
    plt.show()


#CONSULTA 3
def histograma_por_nota():
    print("")
    print("Histograma por nota")
    print("1 - Por tipo de producto (o todos)")
    print("2 - Por artículo individual (asin)")
    print("c - Cancelar")
    opcion = input("Selecciona:").strip().lower()

    if opcion == "c":
        return

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if opcion == "1":
        tipo = pedir_tipo(permitir_todo=True)
        if tipo is None:
            cursor.close()
            conexion.close()
            return

        if tipo == "todo":
            sql = """
                SELECT overall, COUNT(*)
                FROM REVIEW
                GROUP BY overall
                ORDER BY overall
            """
            cursor.execute(sql)
            titulo = "Reviews por nota de todos los productos"
        else:
            sql = """
                SELECT r.overall, COUNT(*)
                FROM REVIEW r
                JOIN ARTICULO a ON r.asin = a.asin
                WHERE a.tipo = %s
                GROUP BY r.overall
                ORDER BY r.overall
            """
            cursor.execute(sql, (tipo,))
            titulo = f"Reviews por nota de {tipo}"

    elif opcion == "2":
        asin = input("Introduce el asin del artículo:").strip()

        cursor.execute("SELECT asin FROM ARTICULO WHERE asin = %s", (asin,))

        if cursor.fetchone() is None: #Comprobamos que exista el artículo
            print(f"El artículo «{asin}» no existe en la base de datos.")
            cursor.close()
            conexion.close()
            return

        sql = """
            SELECT overall, COUNT(*)
            FROM REVIEW
            WHERE asin = %s
            GROUP BY overall
            ORDER BY overall
        """
        cursor.execute(sql, (asin,))
        titulo = f"Reviews por nota de artículo {asin}"

    else:
        print("La opción elegida no es posible. Intente otra opción.")
        cursor.close()
        conexion.close()
        return

    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()

    notas = []
    total = []

    for elemento in resultado:
        notas.append(str(int(elemento[0])))
        total.append(elemento[1])

    plt.bar(notas, total)
    plt.title(titulo)
    plt.xlabel("Nota")
    plt.ylabel("Número de reviews")
    plt.show()


#CONSULTA 4
def evolucion_reviews_tiempo():
    print("")
    print("Evolución de reviews a lo largo del tiempo")

    tipo = pedir_tipo(permitir_todo=True)
    if tipo is None:
        return

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if tipo == "todo":
        sql = """
            SELECT unix_review_time
            FROM REVIEW
            ORDER BY unix_review_time
        """
        cursor.execute(sql)
        titulo = "Evolución de las reviews a lo largo del tiempo de todos los productos"
    else:
        sql = """
            SELECT r.unix_review_time
            FROM REVIEW r
            JOIN ARTICULO a ON r.asin = a.asin
            WHERE a.tipo = %s
            ORDER BY r.unix_review_time
        """
        cursor.execute(sql, (tipo,))
        titulo = f"Evolución de las reviews a lo largo del tiempo de {tipo}"

    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    tiempos = []
    for fila in resultado:
        tiempos.append(fila[0])

    acumulado = []
    for i in range(len(tiempos)):
        acumulado.append(i + 1)

    plt.plot(tiempos, acumulado)
    plt.title(titulo)
    plt.xlabel("Tiempo")
    plt.ylabel("Número de reviews")
    plt.show()


#CONSULTA 5
def histograma_reviews_usuario():
    print("")
    print("Histograma de reviews por usuario")

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT reviewer_id, COUNT(*)
        FROM REVIEW
        GROUP BY reviewer_id
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    reviews_por_usuario = []
    for elemento in resultado:
        reviews_por_usuario.append(elemento[1])

    plt.hist(reviews_por_usuario, bins=800)
    plt.title("Reviews por usuario")
    plt.xlabel("Número de reviews")
    plt.ylabel("Número de usuarios")
    plt.show()


#CONSULTA 6
def nube_palabras():
    print("")
    print("Nube de palabras por categoría")

    tipo = pedir_tipo(permitir_todo=False)
    if tipo is None:
        return

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("SELECT asin FROM ARTICULO WHERE tipo = %s", (tipo,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    asins = []
    for elemento in resultado:
        asins.append(elemento[0])

    coleccion = conectar_mongodb()
    documentos = coleccion.find({"asin": {"$in": asins}},{"summary": 1, "_id": 0})

    texto = ""

    for doc in documentos:
        if "summary" in doc:
            resumen = doc["summary"]

            palabras = resumen.split(" ")
            for palabra in palabras:
                if len(palabra) > 3:
                    texto += palabra + " "

    wc = WordCloud().generate(texto)
    plt.imshow(wc)
    plt.axis("off")
    plt.title(f"Nube de palabras de {tipo}")
    plt.show()


#CONSULTA 7
def usuarios_por_categoria():
    print("")
    print("Usuarios únicos por categoría")

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT a.tipo, COUNT(DISTINCT r.reviewer_id)
        FROM REVIEW r
        JOIN ARTICULO a ON r.asin = a.asin
        GROUP BY a.tipo
        ORDER BY COUNT(DISTINCT r.reviewer_id) DESC
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    categorias = []
    usuarios = []

    for elemento in resultado:
        categorias.append(elemento[0])
        usuarios.append(elemento[1])

    plt.bar(categorias, usuarios)
    plt.title("Usuarios únicos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Número de usuarios")
    plt.xticks(rotation=45)
    plt.show()

#CONSULTA EXTRA PARTE 5 (AÑADIDO MÁS TARDE)
def recomendar_articulos_no_consumidos():
    print("")
    print("Recomendación de artículos no consumidos")

    reviewer_id = input("Introduce el reviewer_id del usuario:").strip()
    tipo = pedir_tipo(permitir_todo=False)

    if tipo is None:
        return

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT r.asin, COUNT(*)
        FROM REVIEW r
        JOIN ARTICULO a ON r.asin = a.asin
        WHERE a.tipo = %s
        AND r.asin NOT IN (SELECT asin FROM REVIEW WHERE reviewer_id = %s)
        GROUP BY r.asin
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """

    cursor.execute(sql, (tipo, reviewer_id))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    print("")
    print("Artículos recomendados:")

    if len(resultado) == 0:
        print("No se han encontrado artículos que recomendar")
        return

    for elemento in resultado:
        print(f"ASIN: {elemento[0]} // Número de reviews: {elemento[1]}")


#MENU VISUALIZACION
def menu():
    print("")
    print("-" * 125)
    print("Menú de visualización con las Reviews de Amazon")
    print("-" * 125)
    print("1 - Evolución de reviews por años")
    print("2 - Evolución de popularidad de artículos")
    print("3 - Histograma por nota (overall)")
    print("4 - Evolución de reviews a lo largo del tiempo")
    print("5 - Histograma de reviews por usuario")
    print("6 - Nube de palabras por categoría")
    print("7 - Usuarios únicos por categoría")
    print("8 - (Parte 5) Recomendación de artículos no consumidos")
    print("0 - Salir")
    print("-" * 125)


if __name__ == "__main__":
    imprimir_cartel()
    opciones = {
        "1": evolucion_reviews_ano,
        "2": evolucion_popularidad,
        "3": histograma_por_nota,
        "4": evolucion_reviews_tiempo,
        "5": histograma_reviews_usuario,
        "6": nube_palabras,
        "7": usuarios_por_categoria,
        "8": recomendar_articulos_no_consumidos}
    
    seguir = True
    while seguir:
        menu()
        seleccion = input("Elige una opción: ").strip()
        if seleccion == "0":
            print("")
            print("Has elegido salir del programa")
            seguir = False

        elif seleccion in opciones:
            opciones[seleccion]()
            
        else:
            print("")
            print("Inténtalo de nuevo, la opción elegida no es válida")