import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# MySQL
host = os.getenv("MYSQL_HOST", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "")
db_sql = os.getenv("MYSQL_DATABASE", "ProyectoBasesSQL")

# MongoDB
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
db_mongo = os.getenv("MONGODB_DATABASE", "ProyectoBasesMongo")
coleccion = os.getenv("MONGODB_COLLECTION", "Reviews")

# Input datasets
ruta_toys_and_games = str(DATA_DIR / "Toys_and_Games_5.json")
ruta_video_games = str(DATA_DIR / "Video_Games_5.json")
ruta_digital_music = str(DATA_DIR / "Digital_Music_5.json")
ruta_musical_instruments = str(DATA_DIR / "Musical_Instruments_5.json")
ruta_grocery_and_gourmet_food = str(DATA_DIR / "Grocery_and_Gourmet_Food_5.json")

# Neo4j
neo4j_uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "")
