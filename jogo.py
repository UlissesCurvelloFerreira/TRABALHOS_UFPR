import pygame
import random
import time
import sys
import math

# Inicialização do Pygame
pygame.init()

# Constantes
LARGURA, ALTURA = 1200, 900  # Aumentando o tamanho da tela
TAMANHO_CELULA = 15  # Diminuindo o tamanho da célula para caber mais
LINHAS = ALTURA // TAMANHO_CELULA
COLUNAS = LARGURA // TAMANHO_CELULA

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Labirinto Aleatório")
relogio = pygame.time.Clock()

# Classe para representar o jogador
class Jogador:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.raio = TAMANHO_CELULA // 2 - 2
        self.cor = AZUL
        self.visibilidade = 5  # Quantas células ao redor do jogador são visíveis
        self.blur_ativo = True  # Inicialmente, o blur está ativado
        self.blur_temporizado = False  # Controle para o blur temporário desativado
        self.tempo_blur = 0  # Tempo para controlar o blur temporizado
    
    def desenhar(self, tela):
        centro_x = self.coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
        centro_y = self.linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
        pygame.draw.circle(tela, self.cor, (centro_x, centro_y), self.raio)
    
    def mover(self, direcao, labirinto):
        nova_linha, nova_coluna = self.linha, self.coluna
        
        if direcao == "CIMA" and self.linha > 0:
            nova_linha -= 1
        elif direcao == "BAIXO" and self.linha < LINHAS - 1:
            nova_linha += 1
        elif direcao == "ESQUERDA" and self.coluna > 0:
            nova_coluna -= 1
        elif direcao == "DIREITA" and self.coluna < COLUNAS - 1:
            nova_coluna += 1
        
        # Verificar se a nova posição é válida (não é uma parede)
        if not labirinto[nova_linha][nova_coluna]:
            self.linha = nova_linha
            self.coluna = nova_coluna
            return True
        return False
    
    def alternar_blur(self):
        if not self.blur_temporizado:
            self.blur_ativo = not self.blur_ativo
    
    def desativar_blur_temporario(self):
        self.blur_temporizado = True
        self.blur_ativo = False
        self.tempo_blur = pygame.time.get_ticks()
    
    def atualizar_blur_temporario(self):
        if self.blur_temporizado:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_blur > 5000:  # 5 segundos
                self.blur_temporizado = False
                self.blur_ativo = True

# Classe para representar os itens que cancelam o blur
class ItemBlur:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.raio = TAMANHO_CELULA // 3
        self.cor = AMARELO
        self.ativo = True
    
    def desenhar(self, tela):
        if self.ativo:
            centro_x = self.coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
            centro_y = self.linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
            pygame.draw.circle(tela, self.cor, (centro_x, centro_y), self.raio)

# Função para gerar um labirinto usando o algoritmo de DFS (Depth-First Search)
def gerar_labirinto():
    # Inicializa o labirinto com paredes em todas as células
    labirinto = [[True for _ in range(COLUNAS)] for _ in range(LINHAS)]
    
    # Função para verificar se uma célula está dentro dos limites
    def dentro_limites(linha, coluna):
        return 0 <= linha < LINHAS and 0 <= coluna < COLUNAS
    
    # Função recursiva para escavar o labirinto
    def escavar(linha, coluna):
        # Marcar a célula atual como caminho
        labirinto[linha][coluna] = False
        
        # Lista de direções possíveis (em ordem aleatória)
        direcoes = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(direcoes)
        
        # Explorar cada direção
        for dl, dc in direcoes:
            nova_linha, nova_coluna = linha + dl, coluna + dc
            
            # Verificar se a nova posição está dentro dos limites e não foi visitada
            if dentro_limites(nova_linha, nova_coluna) and labirinto[nova_linha][nova_coluna]:
                # Derrubar a parede entre as células
                labirinto[linha + dl//2][coluna + dc//2] = False
                # Recursivamente escavar a partir da nova célula
                escavar(nova_linha, nova_coluna)
    
    # Começar em um ponto aleatório com coordenadas ímpares
    inicio_linha = random.randint(0, (LINHAS - 1) // 2) * 2
    inicio_coluna = random.randint(0, (COLUNAS - 1) // 2) * 2
    
    # Garantir que o início seja válido
    if inicio_linha >= LINHAS:
        inicio_linha = LINHAS - 1
    if inicio_coluna >= COLUNAS:
        inicio_coluna = COLUNAS - 1
    
    # Iniciar a escavação
    escavar(inicio_linha, inicio_coluna)
    
    # Garantir que há um caminho livre no início
    labirinto[0][0] = False
    
    # Garantir que há um caminho livre no objetivo
    labirinto[LINHAS - 1][COLUNAS - 1] = False
    
    return labirinto, (0, 0), (LINHAS - 1, COLUNAS - 1)

# Função para gerar itens que cancelam o blur
def gerar_itens_blur(labirinto, inicio, objetivo, quantidade=10):  # Aumentado para 10 itens
    itens = []
    
    # Tentativas para evitar loop infinito
    tentativas = 0
    max_tentativas = 1000
    
    while len(itens) < quantidade and tentativas < max_tentativas:
        linha = random.randint(0, LINHAS - 1)
        coluna = random.randint(0, COLUNAS - 1)
        
        # Verificar se a posição é um caminho e não coincide com o início ou objetivo
        if not labirinto[linha][coluna] and (linha, coluna) != inicio and (linha, coluna) != objetivo:
            # Verificar se já não existe um item nesta posição
            posicao_ocupada = False
            for item in itens:
                if item.linha == linha and item.coluna == coluna:
                    posicao_ocupada = True
                    break
            
            if not posicao_ocupada:
                itens.append(ItemBlur(linha, coluna))
        
        tentativas += 1
    
    return itens

def desenhar_labirinto(tela, labirinto, jogador, objetivo, itens):
    tela.fill(PRETO)
    
    # Desenhar o labirinto com base na visibilidade do jogador
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = coluna * TAMANHO_CELULA
            y = linha * TAMANHO_CELULA
            
            # Calcular a distância euclidiana do jogador (para blur circular)
            distancia = math.sqrt((linha - jogador.linha) ** 2 + (coluna - jogador.coluna) ** 2)
            
            # Se o blur estiver ativo, mostrar apenas as células próximas ao jogador
            if not jogador.blur_ativo or distancia <= jogador.visibilidade:
                if labirinto[linha][coluna]:
                    # Parede
                    pygame.draw.rect(tela, BRANCO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
                else:
                    # Caminho
                    pygame.draw.rect(tela, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
                    pygame.draw.rect(tela, (50, 50, 50), (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)
                
                # Desenhar o objetivo
                if (linha, coluna) == objetivo:
                    centro_x = coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
                    centro_y = linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
                    pygame.draw.circle(tela, VERMELHO, (centro_x, centro_y), TAMANHO_CELULA // 2)
            else:
                # Desenhar área não visível com efeito de sombra
                # Criar um gradiente de sombra baseado na distância
                intensidade = max(0, min(255, int(20 + (distancia - jogador.visibilidade) * 10)))
                cor_sombra = (intensidade // 4, intensidade // 4, intensidade // 4)
                pygame.draw.rect(tela, cor_sombra, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
    
    # Desenhar os itens de blur
    for item in itens:
        if item.ativo:
            # Verificar se o item está visível para o jogador
            distancia = math.sqrt((item.linha - jogador.linha) ** 2 + (item.coluna - jogador.coluna) ** 2)
            if not jogador.blur_ativo or distancia <= jogador.visibilidade:
                item.desenhar(tela)
    
    # Desenhar o jogador
    jogador.desenhar(tela)

def exibir_mensagem(tela, mensagem, tamanho=36):
    tela.fill(PRETO)
    fonte = pygame.font.Font(None, tamanho)
    texto = fonte.render(mensagem, True, BRANCO)
    pos_texto = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))
    tela.blit(texto, pos_texto)
    pygame.display.flip()
    time.sleep(2)

def formatar_tempo(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02d}:{segundos:02d}"

def tela_inicial():
    tela.fill(PRETO)
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_controles = pygame.font.Font(None, 30)
    
    titulo = fonte_titulo.render("LABIRINTO ALEATÓRIO", True, BRANCO)
    controles = [
        "CONTROLES:",
        "SETAS DIRECIONAIS - Movimentação",
        "R - Reiniciar o jogo",
        "ESC - Sair do jogo"
    ]
    
    instrucao = fonte_controles.render("PRESSIONE ENTER PARA COMEÇAR", True, BRANCO)
    
    pos_titulo = titulo.get_rect(center=(LARGURA // 2, ALTURA // 4))
    tela.blit(titulo, pos_titulo)
    
    for i, texto in enumerate(controles):
        controle = fonte_controles.render(texto, True, BRANCO)
        pos_controle = controle.get_rect(center=(LARGURA // 2, ALTURA // 3 + i * 40))
        tela.blit(controle, pos_controle)
    
    pos_instrucao = instrucao.get_rect(center=(LARGURA // 2, ALTURA * 3 // 4))
    tela.blit(instrucao, pos_instrucao)
    
    pygame.display.flip()
    
    # Aguardar o usuário pressionar Enter
    aguardando = True
    while aguardando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    aguardando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def jogo_principal():
    # Mostrar tela inicial
    tela_inicial()
    
    # Gerar o labirinto inicial
    labirinto, (inicio_linha, inicio_coluna), objetivo = gerar_labirinto()
    jogador = Jogador(inicio_linha, inicio_coluna)
    
    # Gerar itens que cancelam o blur
    itens_blur = gerar_itens_blur(labirinto, (inicio_linha, inicio_coluna), objetivo)
    
    rodando = True
    venceu = False
    
    # Inicializar timer
    tempo_inicio = pygame.time.get_ticks()
    tempo_limite = 5 * 60 * 1000  # 5 minutos em milissegundos
    
    # Dicionário para controlar teclas pressionadas
    teclas_pressionadas = {
        pygame.K_UP: False,
        pygame.K_DOWN: False,
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False
    }
    
    while rodando:
        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Captura de teclas pressionadas
            if evento.type == pygame.KEYDOWN:
                if evento.key in teclas_pressionadas:
                    teclas_pressionadas[evento.key] = True
                elif evento.key == pygame.K_b:
                    jogador.alternar_blur()
                elif evento.key == pygame.K_r:
                    # Reiniciar o jogo
                    labirinto, (inicio_linha, inicio_coluna), objetivo = gerar_labirinto()
                    jogador = Jogador(inicio_linha, inicio_coluna)
                    itens_blur = gerar_itens_blur(labirinto, (inicio_linha, inicio_coluna), objetivo)
                    venceu = False
                    tempo_inicio = pygame.time.get_ticks()
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False
            
            # Captura de teclas liberadas
            if evento.type == pygame.KEYUP:
                if evento.key in teclas_pressionadas:
                    teclas_pressionadas[evento.key] = False
        
        # Movimentação contínua baseada nas teclas pressionadas
        moveu = False
        if teclas_pressionadas[pygame.K_UP]:
            moveu = jogador.mover("CIMA", labirinto)
        if teclas_pressionadas[pygame.K_DOWN]:
            moveu = jogador.mover("BAIXO", labirinto)
        if teclas_pressionadas[pygame.K_LEFT]:
            moveu = jogador.mover("ESQUERDA", labirinto)
        if teclas_pressionadas[pygame.K_RIGHT]:
            moveu = jogador.mover("DIREITA", labirinto)
        
        # Atualizar o tempo do blur temporário
        jogador.atualizar_blur_temporario()
        
        # Verificar se o jogador pegou algum item de blur
        for item in itens_blur:
            if item.ativo and jogador.linha == item.linha and jogador.coluna == item.coluna:
                item.ativo = False
                jogador.desativar_blur_temporario()
        
        # Verificar tempo restante
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = tempo_atual - tempo_inicio
        
        if tempo_decorrido >= tempo_limite and not venceu:
            exibir_mensagem(tela, "O LABIRINTO VENCEU! VOCÊ PERDEU.", 36)
            # Reiniciar o jogo
            labirinto, (inicio_linha, inicio_coluna), objetivo = gerar_labirinto()
            jogador = Jogador(inicio_linha, inicio_coluna)
            itens_blur = gerar_itens_blur(labirinto, (inicio_linha, inicio_coluna), objetivo)
            venceu = False
            tempo_inicio = pygame.time.get_ticks()
        
        # Verificar se o jogador chegou ao objetivo
        if (jogador.linha, jogador.coluna) == objetivo and not venceu:
            venceu = True
            exibir_mensagem(tela, "VOCÊ VENCEU! PRESSIONE R PARA REINICIAR.", 36)
        
        # Atualizar a tela
        desenhar_labirinto(tela, labirinto, jogador, objetivo, itens_blur)
        
        # Mostrar contador de tempo
        fonte_tempo = pygame.font.Font(None, 48)  # Aumentando o tamanho da fonte
        tempo_restante_segundos = max(0, (tempo_limite - tempo_decorrido) // 1000)
        texto_tempo = fonte_tempo.render(formatar_tempo(tempo_restante_segundos), True, VERMELHO)  # Mudando cor para vermelho
        # Adicionar um fundo para o cronômetro para melhor visibilidade
        pos_tempo = texto_tempo.get_rect(center=(LARGURA // 2, 30))
        fundo_tempo = pygame.Rect(pos_tempo.x - 10, pos_tempo.y - 5, pos_tempo.width + 20, pos_tempo.height + 10)
        pygame.draw.rect(tela, (30, 30, 30), fundo_tempo)
        pygame.draw.rect(tela, BRANCO, fundo_tempo, 2)  # Borda branca
        tela.blit(texto_tempo, pos_tempo)
        
        # Informações na tela
        fonte = pygame.font.Font(None, 24)
        info_controles = fonte.render("SETAS PARA MOVER, R PARA REINICIAR, ESC PARA SAIR", True, VERDE)
        tela.blit(info_controles, (10, 10))
        
        pygame.display.flip()
        relogio.tick(30)
    
    pygame.quit()
    sys.exit()

# Iniciar o jogo
if __name__ == "__main__":
    jogo_principal()