

import time


def bloquearIntersecoes_aDistancia(id, reserva_inicio, reserva_fim, cruzamentos):
    """
    Nesta funcao criamos uma lista vazia de intersecoes a bloquear e percorremos todos os cruzamentos
    e se a posicao do cruzamento for maior ou igual ao inicio da reserva e a reserva final 
    maior ou igual a posicao do cruzamento realizamos o append do cruzamento a lista 
    e efetivamento o lock da intersecao e introduzimos o id do comboio no lock
    """
    intersecoes_aBloquear = []
    # Para cada cruzamento nos cruzamentos enviados 
    for cruzamento in cruzamentos:
        # Verificamos se o cruzamento está entre a posicao do cruzamento e o inicio
        # e o fim do cruzamento que é o cruzamento mais o tamanho do comboio 
        if reserva_fim >= cruzamento.posicao >= reserva_inicio and cruzamento.intersecao.locked_by != id:
            intersecoes_aBloquear.append(cruzamento.intersecao)

    #Percorremos as intersecoes a bloquear
    for intersecao in intersecoes_aBloquear:
        # Aqui acessamos o objeto intersecao adquirimos e adquirimos os mesmos
        # Introduzindo o id do comboio ao attributo locked_by
        intersecao.mutex.acquire()
        intersecao.locked_by = id
        time.sleep(0.01)



def mover_comboio(comboio, distancia, cruzamentos):
    """
    Nesta funcao recebemos como parametros um comboio a distancia que o comboio que
    tera de percorrer e os cruzamentos e enquanto a frente do comboio for inferior 
    a distancia ele vai continuar a movimentar-se quando a frente do comboio se encontrar
    igual a posicao do cruzamento ai o comboio vai tentar bloquear as intersecoes, quando
    a traseira passar pela intersecao ele desbloqueia a intersecao
    """
    # Enquanto a parte da frente do comboio for menor que a distancia que o comboio tem de 
    # percorrer 
    while comboio.frente < distancia:
        # Incrementa 1 a frente
        comboio.frente += 1
        # Percorre a lista de cruzamento
        for cruzamento in cruzamentos:
            # Se a frente for igual a posicao do cruzamento 
            if comboio.frente == cruzamento.posicao:
                # Chama a funcao bloquearIntersecoes_aDistancia
                bloquearIntersecoes_aDistancia(comboio.uid, cruzamento.posicao,
                                               cruzamento.posicao + comboio.comboio_tamanho, cruzamentos)
            # muda o valor da trazeira pois a frente foi modificada em cima e tira os 200 do tamanho do comboio de
            # sendo assim a traseira e incrementada em 1 tambem acompanhando o tamanho do comboio
            traseira = comboio.frente - comboio.comboio_tamanho
            # quando a traseira estiver na posicao do cruzamento
            if traseira == cruzamento.posicao:
                # volta a colocar o locked_by como -1 ou seja sem nenhum comboio
                # e faz realease ao objeto de exclusao multipla
                cruzamento.intersecao.locked_by = -1
                cruzamento.intersecao.mutex.release()
        time.sleep(0.01)