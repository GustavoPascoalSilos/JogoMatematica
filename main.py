import pygame
import random


# Inicialização do Pygame
pygame.init()
relogio = pygame.time.Clock()

# Configurações da tela
LARGURA_TELA = 1280
ALTURA_TELA = 720
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo de Matemática")

#Delta Time
dt = 0

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Configuração de fonte
fonte = pygame.font.SysFont("Arial", 40)

#Carrega as sprites para o game
folhaSpritesIdle = pygame.image.load("assets/Destroyer/Idle.png").convert_alpha()
folhaSpritesWalk = pygame.image.load("assets/Destroyer/Walk.png").convert_alpha()

#Lista de frames
listFramesIdle = []
listFramesWalk = []

# Cria os frames do personagem na lista de listFramesIdle
for i in range(5):
    # Pega um frame da folha de sprites na posição i * 0, 0 com tamanho 128x128
    frame = folhaSpritesIdle.subsurface(i * 128, 0, 128, 128)
    # Redimensiona o frame para 2 vezes o tamanho original
    frame = pygame.transform.scale2x(frame)
    # Adiciona o frame na lista de listFramesIdle
    listFramesIdle.append(frame)

for i in range(8):
    # Pega um frame da folha de sprites na posição i * 0, 0 com tamanho 128x128
    frame = folhaSpritesWalk.subsurface(i * 128, 0, 128, 128)
    # Redimensiona o frame para 2 vezes o tamanho original
    frame = pygame.transform.scale2x(frame)
    # Adiciona o frame na lista de listFramesIdle
    listFramesWalk.append(frame)

#Variaveis da animação do personagem
indexFrameIdle = 0
tempoAnimacaoIdle = 0
velocidadeAnimacaoIdle = 5

indexFrameWalk = 0
tempoAnimacaoWalk = 0
velocidadeAnimacaoWalk = 10


# Define se o personagem está andando ou não
estaAndando = False 

# Personagem
personagemRect = listFramesIdle[0].get_rect(midbottom=(LARGURA_TELA/2, 650))
personagemColisaoRect = pygame.Rect(personagemRect.x, personagemRect.x, 80, 120)
velocidadePersonagem = 5

# Lista de números e questões
class CaindoNumero:
    def __init__(self, valor, y):
        self.valor = valor
        self.rect = pygame.Rect(random.randint(0, LARGURA_TELA-50), y, 50, 50)
    #Função para fazer os numeros cairem
    def cair(self):
        self.rect.y += 5
        if self.rect.y > ALTURA_TELA:
            self.rect.y = random.randint(-100, -10)
            self.rect.x = random.randint(0, LARGURA_TELA-50)

#Função para gerar a pergunta, até que o usuário pegue a resposta correta
def gerar_pergunta():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    resultado = num1 * num2
    pergunta = f" Qual o resultado correto: {num1} x {num2} = ?"
    return pergunta, resultado

# Função principal do jogo
def main():
    # Variáveis do jogo
    pergunta, resposta_correta = gerar_pergunta()
    numeros = [CaindoNumero(resposta_correta, -50)]
    for _ in range(5):  # Número de numeros que caem da tela
        numero = random.randint(1, 100)
        numeros.append(CaindoNumero(numero, -50))
    
    # Loop principal do jogo
    jogando = True
    while jogando:
        tela.fill(BRANCO)
        
        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit() # Fecha o jogo
                exit() # Fecha o programa

        #Verifica se o personagem está andando
        estaAndando = False
        # Direção que o personagem está olhando (1 = Direita, -1 = Esquerda)
        direcaoPersonagem = 1 
        

        tempoAnimacaoIdle += dt

        if tempoAnimacaoIdle >= 1 / velocidadeAnimacaoIdle:
        # Atualiza o frame do personagem parado de acordo com a lista de frames
            indexFrameIdle = (indexFrameIdle + 1) % len(listFramesIdle)
            tempoAnimacaoIdle = 0.0 # Reseta o tempo entre os frames   

        tempoAnimacaoWalk += dt

        if tempoAnimacaoWalk >= 1 / velocidadeAnimacaoWalk:
        # Atualiza o frame do personagem andando
            indexFrameWalk = (indexFrameWalk + 1) % len(listFramesWalk)
            tempoAnimacaoWalk = 0.0    

        # Movimentação do personagem
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] and personagemRect.x > 0:
            direcaoPersonagem = -1
            estaAndando = True
                
        if teclas[pygame.K_RIGHT] and personagemRect.x < LARGURA_TELA - personagemRect.width:
            direcaoPersonagem = 1
            estaAndando = True
           
        if estaAndando:
            frame = listFramesWalk[indexFrameWalk]
        else:
            frame = listFramesIdle[indexFrameIdle]

        
        if direcaoPersonagem == -1: # Verifica se o personagem está olhando para a esquerda e inverte a imagem
            frame = pygame.transform.flip(frame, True, False) # Inverte a imagem


        # Cair números
        for numero in numeros:
            numero.cair()
            pygame.draw.rect(tela, VERMELHO, numero.rect)
            texto = fonte.render(str(numero.valor), True, BRANCO)
            tela.blit(texto, numero.rect.topleft)
            
            # Verificar se o personagem pegou o número correto
            if personagemRect.colliderect(numero.rect) and numero.valor == resposta_correta:
                pergunta, resposta_correta = gerar_pergunta()
                numeros = [CaindoNumero(resposta_correta, -50)]
                for _ in range(5):
                    numero = random.randint(1, 100)
                    numeros.append(CaindoNumero(numero, -50))
        
        # Mostrar pergunta na tela
        pergunta_texto = fonte.render(pergunta, True, AZUL)
        tela.blit(pergunta_texto, (LARGURA_TELA/2 - pergunta_texto.get_width()/2, 50))

        #Desenha o personagem
        tela.blit(frame, personagemRect)
       
        # Atualizar a tela
        pygame.display.update()

        
        # Controlar o FPS
        dt = relogio.tick(60) /1000


# Rodar o jogo
if __name__ == "__main__":
    main()