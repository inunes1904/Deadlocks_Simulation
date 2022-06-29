
from threading import Lock, Thread

from arbitrario.comboio import *
from desenhar_comboios import *
from modelos import *

comboio_tamanho = 200


# Criacao da Janela
win = GraphWin('Comboios Simulação - Threads', 800, 800)  
# Definir cor do fundo da Janela
win.setBackground('white')
# Criacao do objeto da class AnimacaoComboio que vai ser responsavel 
# por todo o aspeto da Janela com os 4 comboios as 4 Pistas e os 4 sinais
animacao_comb = AnimacaoComboio(win, comboio_tamanho)

lista_comboios = []
lista_intersecoes = []

# Loop para a Criacao de 4 objectos da class Comboio
for i in range(4):
    # Sendo i o id do comboio o segundo atributo o tamanho que e sempre 200 e a frente começa a 0
    lista_comboios.append(Comboio(i, comboio_tamanho, 0))

# Loop para a Criacao de 4 objectos da class Intersecao
for i in range(4):
    # Sendo i o id da intersecao o segundo atributo o nosso objecto de exclusão mutua que é do tipo Lock e o locked_by a -1
    # que significa que o recurso não está a ser utilizado
    lista_intersecoes.append(Intersecao(i, Lock(), -1))

# Criacao das Quartro Threads na qual enviamos o objecto comboio em cada uma delas a posição inicial e
# uma lista de dois objectos do tipo cruzamento que o comboio terá de passar
t1 = Thread(target=mover_comboio,
            args=(lista_comboios[0], 780, [Cruzamento(320, lista_intersecoes[0]), Cruzamento(460, lista_intersecoes[1])]))
t2 = Thread(target=mover_comboio,
            args=(lista_comboios[1], 780, [Cruzamento(320, lista_intersecoes[1]), Cruzamento(460, lista_intersecoes[2])]))
t3 = Thread(target=mover_comboio,
            args=(lista_comboios[2], 780, [Cruzamento(320, lista_intersecoes[2]), Cruzamento(460, lista_intersecoes[3])]))
t4 = Thread(target=mover_comboio,
            args=(lista_comboios[3], 780, [Cruzamento(320, lista_intersecoes[3]), Cruzamento(460, lista_intersecoes[0])]))

#Iniciamos todas as Threads
t1.start()
t2.start()
t3.start()
t4.start()

# Enquanto os comboios nao atingirem os 780 da distancia que têm de percorrer atualiza a posicao dos Comboios
# para as posicoes atuais
while True:
    animacao_comb.atualizarPosComboios(lista_comboios, lista_intersecoes)
    time.sleep(0.01)


