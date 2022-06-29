
#Class Comboio
class Comboio:
    #Metodo para instanciar um objecto da class Comboio
    def __init__(self, uid, comboio_tamanho, frente):
        self.uid = uid
        self.comboio_tamanho = comboio_tamanho
        self.frente = frente

#Class Intersecao
class Intersecao:
    #Metodo para instanciar um objecto da class Intersecao
    def __init__(self, uid, mutex, locked_by):
        self.uid = uid
        self.mutex = mutex
        self.locked_by = locked_by

#Class Cruzamento
class Cruzamento:
    #Metodo para instanciar um objecto da class Cruzamento
    def __init__(self, posicao, intersecao):
        self.posicao = posicao
        self.intersecao = intersecao
