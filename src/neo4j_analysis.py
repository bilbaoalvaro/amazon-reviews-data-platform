#ÁLVARO BILBAO PARDO
#neo4jProyecto.py

import math
import random
import pymysql
from neo4j import GraphDatabase
from config import *

#Cartel puramente decorativo 
def imprimir_cartel():
    print("""
                                  __  __ ______ _   _ _    _   _   _ ______ ____  _  _       _ 
                                 |  \/  |  ____| \ | | |  | | | \ | |  ____/ __ \| || |     | |
                                 | \  / | |__  |  \| | |  | | |  \| | |__ | |  | | || |_    | |
                                 | |\/| |  __| | . ` | |  | | | . ` |  __|| |  | |__   _|   | |
                                 | |  | | |____| |\  | |__| | | |\  | |___| |__| |  | || |__| |
                                 |_|  |_|______|_| \_|\____/  |_| \_|______\____/   |_| \____/ 
                                                               
                                                               """)
    print("""
                 ▗▄▖ ▗▖  ▗▖  ▗▖ ▗▄▖ ▗▄▄▖  ▗▄▖     ▗▄▄▖ ▗▄▄▄▖▗▖   ▗▄▄▖  ▗▄▖  ▗▄▖     ▗▄▄▖  ▗▄▖ ▗▄▄▖ ▗▄▄▄   ▗▄▖     
                ▐▌ ▐▌▐▌  ▐▌  ▐▌▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌  █  ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌  █ ▐▌ ▐▌    
                ▐▛▀▜▌▐▌  ▐▌  ▐▌▐▛▀▜▌▐▛▀▚▖▐▌ ▐▌    ▐▛▀▚▖  █  ▐▌   ▐▛▀▚▖▐▛▀▜▌▐▌ ▐▌    ▐▛▀▘ ▐▛▀▜▌▐▛▀▚▖▐▌  █ ▐▌ ▐▌    
                ▐▌ ▐▌▐▙▄▄▖▝▚▞▘ ▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘    ▐▙▄▞▘▗▄█▄▖▐▙▄▄▖▐▙▄▞▘▐▌ ▐▌▝▚▄▞▘    ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▙▄▄▀ ▝▚▄▞▘    
                                                                                                        
                                                                                                        
                                                                                                        """)

#Diccionario con los tipos de producto
tipos = {"1": "Video Games", "2": "Toys and Games", "3": "Digital Music", "4": "Musical Instruments"}

#Nos conectamos a MySQL
def conectar_mysql():
    conexion = pymysql.connect(host=host, user=user, password=password, database=db_sql)
    return conexion

#Nos conectamos a Neo4j
def conectar_neo4j():
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    return driver

#Borramos todo lo que haya en Neo4j para empezar de cero
def limpiar_neo4j(driver):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

#Menú para elegir tipo de producto
def pedir_tipo(permitir_todo=True):
    if permitir_todo:
        print("0 - Todo")
    for clave, nombre in tipos.items():
        print(f"{clave} - {nombre}")
    print("s - salir")

    while True:
        opcion = input("Selecciona una categoría: ").strip().lower()

        if opcion == "s":
            return None
        if permitir_todo and opcion == "0":
            return "todo"
        if opcion in tipos:
            return tipos[opcion]

        print("La opción elegida no es válida! Inténtelo otra vez!")


#CONSULTA 1
def obtener_top_usuarios(n):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT reviewer_id
        FROM REVIEW
        GROUP BY reviewer_id
        ORDER BY COUNT(*) DESC
        LIMIT %s
    """
    cursor.execute(sql, (n,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    usuarios = []
    for elemento in resultado:
        usuarios.append(elemento[0])

    return usuarios


#Sacamos todas las reviews de un usuario
def obtener_reviews_usuario(reviewer_id):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT asin, overall
        FROM REVIEW
        WHERE reviewer_id = %s
    """
    cursor.execute(sql, (reviewer_id,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    reviews = {}
    for elemento in resultado:
        reviews[elemento[0]] = elemento[1]
    return reviews


#Calculamos la correlación de Pearson entre dos usuarios
def calcular_pearson(reviews_u, reviews_v):
    articulos_comunes = []

    for articulo in reviews_u:
        if articulo in reviews_v:
            articulos_comunes.append(articulo)

    if len(articulos_comunes) == 0:
        return None

    suma_u = 0
    for valor in reviews_u.values():
        suma_u += valor
    media_u = suma_u / len(reviews_u)

    suma_v = 0
    for valor in reviews_v.values():
        suma_v += valor
    media_v = suma_v / len(reviews_v)

    numerador = 0
    suma_u = 0
    suma_v = 0

    for articulo in articulos_comunes:
        diferencia_u = reviews_u[articulo] - media_u
        diferencia_v = reviews_v[articulo] - media_v

        numerador += diferencia_u * diferencia_v
        suma_u += diferencia_u ** 2
        suma_v += diferencia_v ** 2

    denominador = math.sqrt(suma_u) * math.sqrt(suma_v)

    return numerador / denominador


#Calculamos las similitudes entre todos los pares de usuarios
def calcular_similitudes(lista_usuarios):
    reviews_por_usuario = {}

    for usuario in lista_usuarios:
        reviews_por_usuario[usuario] = obtener_reviews_usuario(usuario)

    similitudes = []

    for i in range(len(lista_usuarios)):
        for j in range(i + 1, len(lista_usuarios)):
            usuario_1 = lista_usuarios[i]
            usuario_2 = lista_usuarios[j]

            similitud = calcular_pearson(reviews_por_usuario[usuario_1], reviews_por_usuario[usuario_2])
            if similitud is not None:
                similitudes.append((usuario_1, usuario_2, similitud))
            
    return similitudes


#Cargamos usuarios y similitudes en Neo4j
def cargar_similitudes_neo4j(lista_usuarios, similitudes):
    driver = conectar_neo4j()

    with driver.session() as session:
        for usuario in lista_usuarios:
            session.run("MERGE (u:USUARIO {reviewer_id: $reviewer_id})", reviewer_id=usuario)

        for elemento in similitudes:
            usuario_1 = elemento[0]
            usuario_2 = elemento[1]
            similitud = elemento[2]

            session.run("""
                MATCH (u1:USUARIO {reviewer_id: $usuario_1})
                MATCH (u2:USUARIO {reviewer_id: $usuario_2})
                MERGE (u1)-[:SIMILITUD {valor: $similitud}]->(u2)
                MERGE (u2)-[:SIMILITUD {valor: $similitud}]->(u1)
            """, usuario_1=usuario_1, usuario_2=usuario_2, similitud=similitud)

    driver.close()


#Mostramos el usuario con más vecinos
def mostrar_usuario_mas_vecinos():
    driver = conectar_neo4j()

    with driver.session() as session:
        resultado = session.run("""
            MATCH (u:USUARIO)-[:SIMILITUD]->(v:USUARIO)
            WITH u, COUNT(v) AS vecinos
            ORDER BY vecinos DESC
            LIMIT 1
            RETURN u.reviewer_id AS usuario, vecinos
        """)

        for elemento in resultado:
            print("")
            print("Usuario con más vecinos:")
            print(elemento["usuario"])
            print("Número de vecinos:")
            print(elemento["vecinos"])
            
    driver.close()


def similitudes_usuarios():
    print("")
    print("Similitudes entre usuarios con correlación de Pearson")

    texto = input("¿Cuántos usuarios con más reviews quieres analizar?:").strip()

    if not texto.isdigit() or int(texto) <= 0:
        print("Debes introducir un número entero mayor que cero")
        return

    numero = int(texto)

    driver = conectar_neo4j()
    limpiar_neo4j(driver)
    driver.close()

    usuarios = obtener_top_usuarios(numero)
    print("Usuarios obtenidos:")
    print(len(usuarios))

    similitudes = calcular_similitudes(usuarios)
    print("Similitudes calculadas:")
    print(len(similitudes))

    cargar_similitudes_neo4j(usuarios, similitudes)
    mostrar_usuario_mas_vecinos()

    print("")
    print("Datos cargados en Neo4j, están en http://localhost:7474")


#CONSULTA 2
#Pedimos cuántos artículos aleatorios quiere el usuario
def pedir_numero_articulos():
    while True:
        try:
            numero = int(input("¿Cuántos artículos aleatorios quieres coger?:").strip())
            if numero > 0:
                return numero
            print("El número debe ser mayor que 0")
        except:
            print("Debes introducir un número entero válido")


#Sacamos artículos aleatorios de una categoría
def obtener_articulos_aleatorios(tipo, numero):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = "SELECT asin FROM ARTICULO WHERE tipo = %s"
    cursor.execute(sql, (tipo,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    asins = []
    for elemento in resultado:
        asins.append(elemento[0])

    if len(asins) <= numero:
        return asins

    return random.sample(asins, numero)


#Sacamos las reviews de un artículo
def obtener_reviews_articulo(asin):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT reviewer_id, overall, unix_review_time
        FROM REVIEW
        WHERE asin = %s
    """
    cursor.execute(sql, (asin,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado


#Cargamos artículos y usuarios en Neo4j
def cargar_articulos_usuarios_neo4j(diccionario_articulos, tipo):
    driver = conectar_neo4j()

    with driver.session() as session:
        for asin in diccionario_articulos:
            session.run("""
                MERGE (a:ARTICULO {asin: $asin})
                SET a.tipo = $tipo
            """, asin=asin, tipo=tipo)

            reviews = diccionario_articulos[asin]

            for review in reviews:
                reviewer_id = review[0]
                overall = review[1]
                unix_review_time = review[2]

                session.run("MERGE (u:USUARIO {reviewer_id: $reviewer_id})", reviewer_id=reviewer_id)

                session.run("""
                    MATCH (u:USUARIO {reviewer_id: $reviewer_id})
                    MATCH (a:ARTICULO {asin: $asin})
                    MERGE (u)-[:PUNTUA {nota: $overall, tiempo: $unix_review_time}]->(a)
                """, reviewer_id=reviewer_id, asin=asin, overall=float(overall), unix_review_time=int(unix_review_time))

    driver.close()


def enlaces_usuarios_articulos():
    print("")
    print("Enlaces entre usuarios y artículos aleatorios")

    tipo = pedir_tipo(permitir_todo=False)

    numero = pedir_numero_articulos()

    driver = conectar_neo4j()
    limpiar_neo4j(driver)
    driver.close()

    articulos = obtener_articulos_aleatorios(tipo, numero)

    if len(articulos) == 0:
        print("No se han encontrado artículos de esa categoría")
        return

    diccionario_articulos = {}

    for asin in articulos:
        diccionario_articulos[asin] = obtener_reviews_articulo(asin)

    cargar_articulos_usuarios_neo4j(diccionario_articulos, tipo)

    print("")
    print("Artículos cargados en Neo4j correctamente")
    print("Puedes verlo en http://localhost:7474")


#CONSULTA 3
#Sacamos los primeros 400 usuarios ordenados por nombre
def obtener_400_usuarios():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT reviewer_id, reviewer_name
        FROM USUARIO
        ORDER BY reviewer_name
        LIMIT 400
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado


#Vemos los tipos de artículos que ha puntuado cada usuario
def obtener_tipos_usuario(reviewer_id):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT a.tipo, COUNT(*)
        FROM REVIEW r
        JOIN ARTICULO a ON r.asin = a.asin
        WHERE r.reviewer_id = %s
        GROUP BY a.tipo
    """
    cursor.execute(sql, (reviewer_id,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    tipos_usuario = {}
    for elemento in resultado:
        tipos_usuario[elemento[0]] = elemento[1]

    return tipos_usuario


#Cargamos usuarios y tipos en Neo4j
def cargar_usuarios_multitipo_neo4j(datos):
    driver = conectar_neo4j()

    with driver.session() as session:
        for elemento in datos:
            reviewer_id = elemento[0]
            reviewer_name = elemento[1]
            tipos_usuario = elemento[2]

            session.run("""
                MERGE (u:USUARIO {reviewer_id: $reviewer_id})
                SET u.nombre = $reviewer_name
            """, reviewer_id=reviewer_id, reviewer_name=reviewer_name)

            for tipo in tipos_usuario:
                cantidad = tipos_usuario[tipo]

                session.run("MERGE (t:TIPO {nombre: $tipo})", tipo=tipo)

                session.run("""
                    MATCH (u:USUARIO {reviewer_id: $reviewer_id})
                    MATCH (t:TIPO {nombre: $tipo})
                    MERGE (u)-[:CONSUME {cantidad: $cantidad}]->(t)
                """, reviewer_id=reviewer_id, tipo=tipo, cantidad=cantidad)

    driver.close()


def usuarios_multitipo():
    print("")
    print("Usuarios que han puntuado más de un tipo de artículo")

    driver = conectar_neo4j()
    limpiar_neo4j(driver)
    driver.close()

    usuarios = obtener_400_usuarios()

    datos = []

    for fila in usuarios:
        reviewer_id = fila[0]
        reviewer_name = fila[1]

        if reviewer_name is None:
            reviewer_name = ""

        tipos_usuario = obtener_tipos_usuario(reviewer_id)

        if len(tipos_usuario) >= 2:
            datos.append((reviewer_id, reviewer_name, tipos_usuario))

    if len(datos) == 0:
        print("No se han encontrado usuarios con más de un tipo de artículo")
        return

    cargar_usuarios_multitipo_neo4j(datos)

    print("")
    print("Usuarios multitipo cargados en Neo4j correctamente")
    print("Total de usuarios cargados:")
    print(len(datos))
    print("Puedes verlo en http://localhost:7474")


#CONSULTA 4
#Sacamos los 5 artículos más populares con menos de 40 reviews
def obtener_articulos_populares():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT asin, COUNT(*)
        FROM REVIEW
        GROUP BY asin
        HAVING COUNT(*) < 40
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado


#Sacamos los usuarios que han puntuado un artículo
def obtener_usuarios_articulo(asin):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT reviewer_id
        FROM REVIEW
        WHERE asin = %s
    """
    cursor.execute(sql, (asin,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    usuarios = []
    for elemento in resultado:
        usuarios.append(elemento[0])

    return usuarios


#Calculamos cuántos artículos tienen en común dos usuarios
def calcular_articulos_comunes(usuario_1, usuario_2):
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    sql = """
        SELECT COUNT(*)
        FROM REVIEW r1
        JOIN REVIEW r2 ON r1.asin = r2.asin
        WHERE r1.reviewer_id = %s AND r2.reviewer_id = %s
    """
    cursor.execute(sql, (usuario_1, usuario_2))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado[0]


#Cargamos artículos populares y relaciones en Neo4j
def cargar_articulos_populares_neo4j(articulos_usuarios):
    driver = conectar_neo4j()

    todos_los_usuarios = set()

    for elemento in articulos_usuarios:
        asin = elemento[0]
        usuarios = elemento[1]

        for usuario in usuarios:
            todos_los_usuarios.add(usuario)

    with driver.session() as session:
        for elemento in articulos_usuarios:
            asin = elemento[0]
            usuarios = elemento[1]

            session.run("MERGE (a:ARTICULO {asin: $asin})", asin=asin)

            for usuario in usuarios:
                session.run("MERGE (u:USUARIO {reviewer_id: $usuario})", usuario=usuario)

                session.run("""
                    MATCH (u:USUARIO {reviewer_id: $usuario})
                    MATCH (a:ARTICULO {asin: $asin})
                    MERGE (u)-[:PUNTUA]->(a)
                """, usuario=usuario, asin=asin)

        lista_usuarios = list(todos_los_usuarios)

        for i in range(len(lista_usuarios)):
            for j in range(i + 1, len(lista_usuarios)):
                usuario_1 = lista_usuarios[i]
                usuario_2 = lista_usuarios[j]

                comunes = calcular_articulos_comunes(usuario_1, usuario_2)

                if comunes > 0:
                    session.run("""
                        MATCH (u1:USUARIO {reviewer_id: $usuario_1})
                        MATCH (u2:USUARIO {reviewer_id: $usuario_2})
                        MERGE (u1)-[:ARTICULOS_COMUNES {cantidad: $comunes}]->(u2)
                        MERGE (u2)-[:ARTICULOS_COMUNES {cantidad: $comunes}]->(u1)
                    """, usuario_1=usuario_1, usuario_2=usuario_2, comunes=comunes)

    driver.close()


def articulos_populares():
    print("")
    print("Artículos populares con menos de 40 reviews y artículos en común")

    driver = conectar_neo4j()
    limpiar_neo4j(driver)
    driver.close()

    articulos = obtener_articulos_populares()

    if len(articulos) == 0:
        print("No se han encontrado artículos")
        return

    print("")
    print("Artículos encontrados:")
    for elemento in articulos:
        print(f"{elemento[0]} - {elemento[1]} reviews")

    articulos_usuarios = []

    for elemento in articulos:
        asin = elemento[0]
        usuarios = obtener_usuarios_articulo(asin)
        articulos_usuarios.append((asin, usuarios))

    cargar_articulos_populares_neo4j(articulos_usuarios)

    print("")
    print("Datos cargados en Neo4j, están en http://localhost:7474")


#MENU
def menu():
    print("")
    print("-" * 125)
    print("Menú Neo4j del proyecto de Bases de Datos")
    print("-" * 125)
    print("1 - Similitudes entre usuarios")
    print("2 - Enlaces entre usuarios y artículos aleatorios")
    print("3 - Usuarios que han puntuado más de un tipo de artículo")
    print("4 - Artículos populares y artículos en común entre usuarios")
    print("0 - Salir")
    print("-" * 125)


if __name__ == "__main__":
    imprimir_cartel()
    opciones = {"1": similitudes_usuarios, "2": enlaces_usuarios_articulos, "3": usuarios_multitipo, "4": articulos_populares}

    seguir = True

    while seguir:
        menu()
        seleccion = input("Elige una opción:").strip()

        if seleccion == "0":
            print("")
            print("Has elegido salir del programa")
            seguir = False

        elif seleccion in opciones:
            try:
                opciones[seleccion]()
            except Exception as e:
                print("")
                print("Se ha producido un error:")
                print(e)

        else:
            print("")
            print("Inténtalo de nuevo, la opción elegida no es válida")