from geopy import distance

from app.grafo import Mapa

CAMINHO_ARQUIVO = input("Caminho arquivo: ")
DISTANCIA_MAX = float(input("Raio em metros: "))
PROFISSIONAIS = set(map(lambda x: x.strip().lower(), 
    input("Profissionais separados por ',': ").split(',')))

mapa = Mapa(CAMINHO_ARQUIVO, PROFISSIONAIS)
mapa.buscar(DISTANCIA_MAX)
