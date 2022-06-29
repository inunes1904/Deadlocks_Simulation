
import threading
import time


# Arbitrario é uma bocado de código que vai decidir que comboio(s) irão utilizar os recursos neste caso os recursos/locks. 
# No nosso exemplo ele será o tipo que está na Sala Central de Controlo de Comboios (exemplo)


# Esta classe implementa objectos variáveis de condição. Uma variável de condição permite que um ou mais threads esperem até serem notificados por outra thread.
# Se o argumento da lock for dado e não None, deve ser um objecto Lock ou RLock, e é utilizado como a fechadura subjacente. Caso contrário, um novo objecto RLock
# é criado e utilizado como a fechadura subjacente.
controlador = threading.Condition()

# Se estiver locked retorna False se não estiver locked retorna True
def todos_livres(instersecoesParaBloquear):
    # Percorre todas as interseções a bloquear
    for it in instersecoesParaBloquear:
        # Se o objecto intersecao tiver o locked_by >= 0 significa que tem um id de um comoboio logo retornará Falso
        if it.locked_by >= 0:
            return False
    # Caso não se verifique a consição em cima retorna True
    return True


def bloquearIntersecoes_aDistancia(id, reserva_inicio, reserva_fim, cruzamentos):
    instersecoesParaBloquear = []
    for cruzamento in cruzamentos:
        if reserva_fim >= cruzamento.posicao >= reserva_inicio and cruzamento.intersecao.locked_by != id:
            instersecoesParaBloquear.append(cruzamento.intersecao)
    # Uma lock primitiva está num de dois estados, "trancada" ou "desbloqueada". É criada no estado desbloqueado. Tem dois métodos básicos, 
    # aquire() e release(). Quando o estado é desbloqueado, aquire() muda o estado para bloqueado e regressa imediatamente. Quando o estado
    # está bloqueado, acquire() bloqueia até que uma chamada para release() noutra thread o altere para desbloqueado, depois a chamada acquire() 
    # repõe o estado bloqueado e devolve-o. O método release() só deve ser chamado no estado bloqueado; muda o estado para desbloqueado e retorna
    # imediatamente. Se for feita uma tentativa de desbloquear uma lock desbloqueada, será levantado um RuntimeError.
    controlador.acquire()
    # Equanto os recursos não estiverem livres o controlador faz a thread esperar
    while not todos_livres(instersecoesParaBloquear):
        controlador.wait()
    # Coloca o id do comboio nas interseções bloqueadas
    for intersecao in instersecoesParaBloquear:
        intersecao.locked_by = id
        time.sleep(0.01)
    # liberta o lock do controlador
    controlador.release()


def mover_comboio(comboio, distancia, cruzamentos):
    # Enquanto a parte da frente do comboio for menor que a distancia que o comboio tem de 
    # percorrer 
    while comboio.frente < distancia:
        # Incrementa 1 a frente
        comboio.frente += 1
        # Percorre todos os cruzamentos enviados como parametro na função
        for cruzamento in cruzamentos:
            # Se a frente do comboio for igual a posicao do cruzamento
            if comboio.frente == cruzamento.posicao:
                # chama a funcao bloquarIntersecoes_aDistancia e passa os argumentos
                # id comboio / cruzamento.posicao / cruzamento.posicao + tamanho_comboio = tamanho do comboio / todos os cruzamentos
                bloquearIntersecoes_aDistancia(comboio.uid, cruzamento.posicao,
                                               cruzamento.posicao + comboio.comboio_tamanho, cruzamentos)
            # como adicionamos um a frente temos de calcular a nova traseira que e nada mais que a noca frente menos o tamanho do comboio
            traseira = comboio.frente - comboio.comboio_tamanho
            # se a traseira for igual a posicao do cruzamento
            if traseira == cruzamento.posicao:
                # controlador adquire o recurso
                controlador.acquire()
                # Muda atributo do objeto cruzamento chamdo locked_by para -1 ou seja sem nenhum id de um comboio associado
                cruzamento.intersecao.locked_by = -1
                # Acorda todos as threads à espera desta condição. Este método age como notify(), mas acorda todos as threads à
                # espera em vez de uma única. Se a thread de chamada não tiver adquirido a lock quando este método é chamado, 
                # é levantado um RuntimeError.
                controlador.notify_all()
                #liberta o controlador
                controlador.release()
        time.sleep(0.01)
