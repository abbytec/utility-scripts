import datetime
import osutools  # Asumiendo que existe un paquete con este nombre

osu_api_key = "--"
username = "-Abbytec-"
year = 2021

def get_top_scores(username, year, limit=100):
    # Inicializa el cliente de osu! con tu API key
    osu_client = osutools.OsuClientV1(osu_api_key)
    
    # Obtener top scores
    me = osu_client.fetch_user(username=username)
    
    best = me.fetch_best(limit=100)

    print(best)
    """ for score in best:
       beatmap = score.fetch_map()
       print(f"{score.pp}pp | {score.score} | {beatmap} | {score.mods}") """

# Llamada a la función
get_top_scores(username, year)
