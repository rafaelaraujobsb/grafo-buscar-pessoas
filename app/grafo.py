from pprint import pprint
from queue import PriorityQueue
from collections import defaultdict

from geopy.distance import distance


class Mapa:
    def __init__(self, caminho_arquivo, profissoes):
        self.iesb = -15.836073, -47.912019
        self.distancia = {'IESB': 0}
        self.arquivo = caminho_arquivo
        self.profissoes = profissoes
        self.grafo = self.__montar_grafo()

    def __ler_arquivo(self, f):
        while True:
            linha =  f.readline()

            if linha:
                nome, pos, profissao, ativo = linha.split(';')

                if all([profissao.lower() in self.profissoes, eval(ativo)]):
                    yield (nome, eval(pos), profissao, ativo)
            else:
                break

    def __montar_grafo(self):
        with open(self.arquivo, 'r') as f:
            linhas = list(self.__ler_arquivo(f))
            
        mapa = defaultdict(set)
        for index, (pessoa1, pos1, profissao1, *_) in enumerate(linhas):
            self.distancia[pessoa1] = float("inf")
            distancia = distance(pos1, self.iesb).km

            mapa['IESB'].add((distancia, pessoa1))
            mapa[pessoa1].add((distancia, 'IESB'))

            for pessoa2, pos2, profissao2, *_ in linhas[index+1:]:
                distancia = distance(pos1, pos2).km
                mapa[pessoa1].add((distancia, pessoa2))
                mapa[pessoa2].add((distancia, pessoa1))

        return mapa

    def buscar(self, distancia_max):
        fila_prioridade, visitados, caminho = PriorityQueue(), set(), list()
        fila_prioridade.put((0, 'IESB'))

        # pprint(self.grafo)

        while not fila_prioridade.empty():
            dist_pai, pai = fila_prioridade.get()

            for dist_filho, filho in self.grafo[pai]:
                if distancia_max > (dist_pai + dist_filho) < self.distancia[filho]:
                    self.distancia[filho] = dist_filho
                    fila_prioridade.put((dist_pai + dist_filho, filho))

            caminho.append(pai)

        caminho.append('IESB')
        print(caminho)
