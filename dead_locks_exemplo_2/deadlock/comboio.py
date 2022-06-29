
import random

import time


def mover_comboio(comboio, distancia, cruzamentos):
    """
    Nesta funcao recebemos como parametros um comboio a distancia que o comboio que
    tera de percorrer e os cruzamentos e enquanto a frente do comboio for inferior 
    a distancia ele vai continuar a movimentar-se quando a frente do comboio se encontrar
    igual a posicao do cruzamento ai o comboio vai tentar bloquear as intersecoes, quando
    a traseira passar pela intersecao ele desbloqueia a intersecao no entanto como não 
    possui nenhum sistema de preferência todos vão bloquear a sua interseção mas não conseguiram 
    passar e acontecerá um deadlock e consequentemente um Starvation ate pararmos efetivamente 
    o programa.
    """
    while comboio.frente < distancia:
        comboio.frente += 1
        for cruzamento in cruzamentos:
            if comboio.frente == cruzamento.posicao:
                cruzamento.intersecao.mutex.acquire()
                cruzamento.intersecao.locked_by = comboio.uid
            trazeira = comboio.frente - comboio.comboio_tamanho
            if trazeira == cruzamento.posicao:
                cruzamento.intersecao.locked_by = -1
                cruzamento.intersecao.mutex.release()
        time.sleep(0.01)
