import pygame
import sys
import random

from settings import *
from ui.menu import Menu
from entities.player import Player
from systems.level import criar_mapa
from entities.enemy import Enemy

# ── Inicialização ───────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Torre do Cavaleiro")

clock = pygame.time.Clock()

# ── Paths ─────────────────────────    ────────────────────────────────────
BASE = r".\assets\sprites"
SND  = r".\assets\sounds"

dungeon  = pygame.image.load(BASE + r"\Dungeon_Tileset.png").convert_alpha()
keys_img = pygame.image.load(BASE + r"\keys.png").convert_alpha()

TB = TAMANHO_BLOCO

def get_tile(sheet, col, row, tw=16, th=16):
    surf = pygame.Surface((tw, th), pygame.SRCALPHA)
    surf.blit(sheet, (0, 0), (col * tw, row * th, tw, th))
    return pygame.transform.scale(surf, (TB, TB))

# ══════════════════════════════════════════════════════════════════════
# CHÃO
# ══════════════════════════════════════════════════════════════════════
TILES_CHAO = [
    get_tile(dungeon, 1, 1),
    get_tile(dungeon, 2, 1),
    get_tile(dungeon, 3, 1),
    get_tile(dungeon, 1, 2),
    get_tile(dungeon, 2, 2),
    get_tile(dungeon, 3, 2),
    get_tile(dungeon, 1, 3),
    get_tile(dungeon, 2, 3),
    get_tile(dungeon, 3, 3),
]

# ══════════════════════════════════════════════════════════════════════
# PAREDES — auto-tiling
# ══════════════════════════════════════════════════════════════════════
T = {
    "canto_sup_esq": get_tile(dungeon, 0, 0),
    "canto_sup_dir": get_tile(dungeon, 5, 5),
    "canto_inf_esq": get_tile(dungeon, 0, 4),
    "canto_inf_dir": get_tile(dungeon, 5, 4),
    "topo":          get_tile(dungeon, 1, 0),
    "base":          get_tile(dungeon, 1, 4),
    "lat_esq":       get_tile(dungeon, 0, 1),
    "lat_dir":       get_tile(dungeon, 5, 1),
    "interior":      get_tile(dungeon, 4, 9),
    "isolado":       get_tile(dungeon, 3, 0),
    "ponta_cima":    get_tile(dungeon, 0, 3),
    "ponta_baixo":   get_tile(dungeon, 5, 1),
    "ponta_esq":     get_tile(dungeon, 4, 0),
    "ponta_dir":     get_tile(dungeon, 2, 0),
}

def escolher_tile_parede(cima, baixo, esq, dir_, gx, gy):
    c, b, e, d = cima, baixo, esq, dir_
    if not c and not b and not e and not d: return T["isolado"]
    if c and not b and not e and not d:     return T["ponta_cima"]
    if not c and b and not e and not d:     return T["ponta_baixo"]
    if not c and not b and e and not d:     return T["ponta_esq"]
    if not c and not b and not e and d:     return T["ponta_dir"]
    if not c and not e and b and d:         return T["canto_sup_esq"]
    if not c and not d and b and e:         return T["canto_sup_dir"]
    if not b and not e and c and d:         return T["canto_inf_esq"]
    if not b and not d and c and e:         return T["canto_inf_dir"]
    if not c and not b and e and d:         return T["topo"]
    if c and b and not e and not d:         return T["lat_esq"]
    if c and b and e and not d:             return T["lat_dir"]
    if c and b and d and not e:             return T["lat_esq"]
    if c and e and d and not b:             return T["base"]
    if b and e and d and not c:             return T["topo"]
    if not c and b:                         return T["topo"]
    if c and not b:                         return T["base"]
    if not e and d:                         return T["lat_esq"]
    if e and not d:                         return T["lat_dir"]
    return T["interior"]

# ── Chave ──────────────────────────────────────────────────────────────
chave_sprite  = pygame.transform.scale(keys_img, (TB, TB))
chave_hud_ico = pygame.transform.scale(keys_img, (28, 28))

# ── Porta ──────────────────────────────────────────────────────────────
PORTA_FECHADA = get_tile(dungeon, 7, 5)
PORTA_ABERTA  = get_tile(dungeon, 7, 6)

# ── Decorações ─────────────────────────────────────────────────────────
TEIA_1 = get_tile(dungeon, 4, 3)
TEIA_2 = get_tile(dungeon, 9, 5)
DECO_1 = get_tile(dungeon, 7, 7)
DECO_2 = get_tile(dungeon, 8, 6)

POSICOES_TEIA_1 = [(1, 1), (18, 1), (1, 12), (18, 12)]
POSICOES_TEIA_2 = [(2, 1), (17, 1), (2, 12), (17, 12)]
POSICOES_DECO_1 = [(5, 4), (10, 7), (14, 3)]
POSICOES_DECO_2 = [(7, 9), (13, 10)]

random.seed(99)
chao_surface = pygame.Surface((LARGURA, ALTURA))
for ry in range(ALTURA // TB + 1):
    for rx in range(LARGURA // TB + 1):
        chao_surface.blit(random.choice(TILES_CHAO), (rx * TB, ry * TB))

deco_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
for (gx, gy) in POSICOES_TEIA_1:
    deco_surface.blit(TEIA_1, (gx * TB, gy * TB))
for (gx, gy) in POSICOES_TEIA_2:
    deco_surface.blit(TEIA_2, (gx * TB, gy * TB))
for (gx, gy) in POSICOES_DECO_1:
    deco_surface.blit(DECO_1, (gx * TB, gy * TB))
for (gx, gy) in POSICOES_DECO_2:
    deco_surface.blit(DECO_2, (gx * TB, gy * TB))

# ══════════════════════════════════════════════════════════════════════
# HUD MEDIEVAL
# ══════════════════════════════════════════════════════════════════════
MAPA_ALTURA = 540          # 11 linhas × 50px  ← área do jogo
HUD_Y       = MAPA_ALTURA  # y=550, onde o HUD começa
HUD_H       = ALTURA - MAPA_ALTURA  # 50px
FASE_ATUAL  = 1

OURO       = (180, 140,  60)
OURO_ESC   = (100,  75,  25)
OURO_BRIL  = (220, 185,  90)
PERGAMINHO = (240, 230, 210)

def carregar_fonte(tamanho, bold=False):
    for nome in ["Palatino Linotype", "Book Antiqua", "Garamond", "Times New Roman"]:
        try:
            return pygame.font.SysFont(nome, tamanho, bold=bold)
        except Exception:
            continue
    return pygame.font.SysFont(None, tamanho, bold=bold)

fonte_grande  = carregar_fonte(19, bold=True)
fonte_pequena = carregar_fonte(17, bold=False)

def build_hud_bg():
    surf = pygame.Surface((LARGURA, HUD_H))
    surf.fill((0, 0, 0))
    # Borda superior tripla ornamentada
    pygame.draw.line(surf, OURO_ESC,  (0, 0), (LARGURA, 0), 1)
    pygame.draw.line(surf, OURO,      (0, 2), (LARGURA, 2), 1)
    pygame.draw.line(surf, OURO_BRIL, (0, 3), (LARGURA, 3), 2)
    pygame.draw.line(surf, OURO,      (0, 5), (LARGURA, 5), 1)
    pygame.draw.line(surf, OURO_ESC,  (0, 6), (LARGURA, 6), 1)
    # Divisor central
    cx = LARGURA // 2
    pygame.draw.line(surf, OURO_ESC, (cx - 1, 10), (cx - 1, HUD_H - 6), 1)
    pygame.draw.line(surf, OURO,     (cx,      8),  (cx,     HUD_H - 5), 1)
    pygame.draw.line(surf, OURO_ESC, (cx + 1, 10), (cx + 1, HUD_H - 6), 1)
    # Losango ornamental
    mid     = HUD_H // 2
    diamond = [(cx, 5), (cx + 6, mid), (cx, HUD_H - 6), (cx - 6, mid)]
    pygame.draw.polygon(surf, OURO,      diamond)
    pygame.draw.polygon(surf, OURO_BRIL, diamond, 1)
    # Cantos decorativos
    for cx_c in [6, LARGURA - 12]:
        pygame.draw.rect(surf, OURO,      (cx_c, 10, 6, 6))
        pygame.draw.rect(surf, OURO_BRIL, (cx_c, 10, 6, 6), 1)
    return surf

hud_bg = build_hud_bg()

def desenhar_hud(surface, chaves_col, total_chav, fase):
    surface.blit(hud_bg, (0, HUD_Y))

    cx = LARGURA // 2
    cy = HUD_Y + HUD_H // 2

    # ── Esquerdo: Fase ────────────────────────────────────────────────
    quarto = cx // 2
    lbl = fonte_pequena.render("✦  FASE  ✦", True, OURO)
    surface.blit(lbl, (quarto - lbl.get_width() // 2, HUD_Y + 9))
    num = fonte_grande.render(str(fase), True, OURO_BRIL)
    surface.blit(num, (quarto - num.get_width() // 2, HUD_Y + 24))

    # ── Direito: Chaves ───────────────────────────────────────────────
    tquarto = cx + cx // 2
    lbl_c = fonte_pequena.render("CHAVES", True, OURO)
    surface.blit(lbl_c, (tquarto - lbl_c.get_width() // 2, HUD_Y + 9))

    txt = fonte_grande.render(f"{chaves_col} / {total_chav}", True, PERGAMINHO)
    bloco_w = chave_hud_ico.get_width() + 6 + txt.get_width()
    ico_x   = tquarto - bloco_w // 2
    ico_y   = cy - chave_hud_ico.get_height() // 2 + 4
    surface.blit(chave_hud_ico, (ico_x, ico_y))
    surface.blit(txt, (ico_x + chave_hud_ico.get_width() + 6,
                        cy - txt.get_height() // 2 + 4))

# ── Menu ──────────────────────────────────────────────────────────────
menu = Menu(tela)
menu.run()

# ── Sons ──────────────────────────────────────────────────────────────
som_chave = pygame.mixer.Sound(SND + r"\mixkit-fairy-arcade-sparkle-866.wav")
som_chave.set_volume(0.5)
som_porta = pygame.mixer.Sound(SND + r"\mixkit-prison-metal-door-close-201.wav")
som_porta.set_volume(0.4)

# ── Estado do jogo ────────────────────────────────────────────────────
chaves_coletadas = 0
porta_aberta     = False

paredes, player_posicao, chaves, porta, inimigos = criar_mapa()
player = Player(player_posicao[0], player_posicao[1])
total_chaves = len(chaves)

posicoes_paredes = set((p.x // TB, p.y // TB) for p in paredes)
paredes_sprites = [
    (p, escolher_tile_parede(
        (p.x // TB,     p.y // TB - 1) in posicoes_paredes,
        (p.x // TB,     p.y // TB + 1) in posicoes_paredes,
        (p.x // TB - 1, p.y // TB    ) in posicoes_paredes,
        (p.x // TB + 1, p.y // TB    ) in posicoes_paredes,
        p.x // TB, p.y // TB
    ))
    for p in paredes
]

# ── Loop principal ────────────────────────────────────────────────────
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    player.mover(teclas, paredes)

    for inimigo in inimigos:
        inimigo.mover(player, paredes)

    for chave in chaves[:]:
        if player.rect.colliderect(chave):
            chaves.remove(chave)
            chaves_coletadas += 1
            som_chave.play()
            if len(chaves) == 0 and not porta_aberta:
                porta_aberta = True
                som_porta.play()

    if porta_aberta and player.rect.colliderect(porta):
        print("PRÓXIMA FASE")

    for inimigo in inimigos:
        if player.rect.colliderect(inimigo.rect):
            print("GAME OVER")

    # ── Desenho ───────────────────────────────────────────────────────
    tela.blit(chao_surface, (0, 0))
    tela.blit(deco_surface, (0, 0))

    for parede, sprite in paredes_sprites:
        tela.blit(sprite, (parede.x, parede.y))

    sprite_porta = PORTA_ABERTA if porta_aberta else PORTA_FECHADA
    tela.blit(sprite_porta, (porta.x, porta.y))

    for chave in chaves:
        tela.blit(chave_sprite, (chave.x - 10, chave.y - 10))

    player.desenhar(tela)
    for inimigo in inimigos:
        inimigo.desenhar(tela)

    desenhar_hud(tela, chaves_coletadas, total_chaves, FASE_ATUAL)

    pygame.display.update()