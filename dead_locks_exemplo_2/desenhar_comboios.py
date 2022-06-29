
from graphics import *

# Apenas para introduzir o numero dos Comboios Corretos e não começar no 0
contador = 1

# Lista de Imagens vazia
listaImagens = []

# Class Animacao Comboio
class AnimacaoComboio:
    def __init__(self, janela, comboio_tamanho):

        #lista de Cores da animacao dos comboios 
        self.colours = [color_rgb(233, 33, 40), color_rgb(78, 151, 210),
                        color_rgb(251, 170, 26), color_rgb(11, 132, 54)]     
        # o tamanho do comboio e enviado na instanciacao do objeto de animacaoComboio
        # possui o valor de 200
        self.comboio_tamanho = comboio_tamanho
        # Criacao dos objetos do tipo Linha para desenhar os caminhos de ferro
        pista0 = Line(Point(10, 330), Point(790, 330))
        pista1 = Line(Point(10, 470), Point(790, 470))
        pista2 = Line(Point(330, 10), Point(330, 790))
        pista3 = Line(Point(470, 10), Point(470, 790))
        #Desenhar os caminhos de Ferro
        self.desenharCaminhoFerro(janela, pista0)
        self.desenharCaminhoFerro(janela, pista1)
        self.desenharCaminhoFerro(janela, pista2)
        self.desenharCaminhoFerro(janela, pista3)
        
        # Criacao dos objetos do tipo Linha para desenhar os comboios
        self.comb0 = Line(Point(10, 330), Point(10 - comboio_tamanho, 330))
        self.comb1 = Line(Point(470, 10), Point(470, 10 - comboio_tamanho))
        self.comb2 = Line(Point(790, 470), Point(790 + comboio_tamanho, 470))
        self.comb3 = Line(Point(330, 790), Point(330, 790 + comboio_tamanho))
        
        # Desenhar os 4 combooios na janela
        self.desenharComboios(janela, self.comb0, self.colours[0], x=self.comb0.getP1().getX()+40, 
                                                           y=self.comb0.getP1().getY()+20)
        self.desenharComboios(janela, self.comb1, self.colours[1], x=self.comb1.getP1().getX()+50, 
                                                           y=self.comb1.getP1().getY()+20)
        self.desenharComboios(janela, self.comb2, self.colours[2], x=self.comb2.getP1().getX()-50, 
                                                           y=self.comb2.getP1().getY()+20)
        self.desenharComboios(janela, self.comb3, self.colours[3], x=self.comb3.getP1().getX()-50, 
                                                           y=self.comb3.getP1().getY()-20)
        
        # Inserir as imagens nas posições corretas
        combVermelhoImg = Image(Point(-115, 330), "vermelho_final.gif")
        combVermelhoImg.setPixel(200, 20, "red")
        combVermelhoImg.draw(janela)
        combAzulImg = Image(Point(470, -145), "azul_final.gif")
        combAzulImg.setPixel(20, 200, "blue")
        combAzulImg.draw(janela)
        combAmareloImg = Image(Point(945, 470), "amarelo_final.gif")
        combAmareloImg.setPixel(200, 20, "yellow")
        combAmareloImg.draw(janela)
        combVerdeImg = Image(Point(330, 950), "verde_final.gif")
        combVerdeImg.setPixel(20, 200, "green")
        combVerdeImg.draw(janela)
        # Adiciona o comboio à lista de imagens
        listaImagens.append(combVermelhoImg)
        listaImagens.append(combAzulImg)
        listaImagens.append(combAmareloImg)
        listaImagens.append(combVerdeImg)


        # "SINAIS de Transito"
        self.circulos = [Circle(Point(360, 360), 15),
                         Circle(Point(440, 360), 15),
                         Circle(Point(440, 440), 15),
                         Circle(Point(360, 440), 15) ]
        # Para cada circulo existente teremos que desenha-lo junto ao cruzamento
        for circulo in self.circulos:
            self.desenharCruzamento(janela, circulo)

       
    # Atualiza as Posicoes dos Comboios
    def atualizarPosComboios(self, comboios, intersecoes):
        # Dependendo do comboio e se anda no eixo do X ou do Y retiramos 10
        # à posicao previa do mesmo
        x_Atual = self.comb0.getP2().getX() - 10 + self.comboio_tamanho
        self.comb0.move(comboios[0].frente - x_Atual, 0)
        listaImagens[0].move(comboios[0].frente - x_Atual, 0)

        x_Atual = 790 - self.comb2.getP2().getX() + self.comboio_tamanho
        self.comb2.move(x_Atual - comboios[2].frente, 0)
        listaImagens[2].move(x_Atual - comboios[2].frente, 0)

        y_Atual = self.comb1.getP2().getY() - 10 + self.comboio_tamanho
        self.comb1.move(0, comboios[1].frente - y_Atual)
        listaImagens[1].move(0, comboios[1].frente - y_Atual)

        y_Atual = 790 - self.comb3.getP2().getY() + self.comboio_tamanho
        self.comb3.move(0, y_Atual - comboios[3].frente)
        listaImagens[3].move(0, y_Atual - comboios[3].frente)
        
        
        
        # Se a intersecao não estiver presa por um comboio o valor será -1
        # muda a cor para preto 
        for i in range(4):
            if intersecoes[i].locked_by < 0:
                self.circulos[i].setFill(color_rgb(0, 0, 0))
            else:
                # Caso seja maior ou igual a 0 colocara a cor do comboio respetivo
                # da lista de cores do objeto Animacao Comboio
                self.circulos[i].setFill(self.colours[intersecoes[i].locked_by])

    # Desenha os sinais que se encontram nos cruzamentos
    def desenharCruzamento(self, janela, circulo):
        circulo.setFill(color_rgb(255, 255, 255))
        circulo.setOutline(color_rgb(255, 255, 255))
        circulo.draw(janela)

    # Desenha os caminhos de Ferro nos quais o comboio se movimenta
    def desenharCaminhoFerro(self, janela, line):
        line.setFill(color_rgb(185, 185, 185))
        line.setWidth(4)
        line.draw(janela)
        
    # Desenha os Comboios
    def desenharComboios(self, janela, line, colour, x, y):
        global contador
        # Desenha a linha que simboliza um comboio
        line.setFill(color_rgb(185, 185, 185))
        line.setWidth(2)
        line.draw(janela)
        # Desenha os nomes dos comboios na Janela
        label = Text(Point(x, y) , f'Comboio {contador}')
        label.setFill(colour)
        label.setSize(15)
        label.setStyle('bold')
        label.draw(janela)
        contador += 1
        

