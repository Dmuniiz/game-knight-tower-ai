from collections import deque

# =========================================================
# Converte posição em pixels para posição do grid
# Exemplo:
# pixel 150x200 -> grid 3x4 se o tile for 50
# =========================================================
def pixel_para_grid(x, y, tile_size):

    return (
        x // tile_size,
        y // tile_size
    )


# =========================================================
# Procura o melhor caminho até o player
# usando BFS (busca em largura)
# =========================================================
def buscar_caminho(inicio, fim, mapa):

    # fila de posições que serão analisadas
    fila = deque()

    # começa pela posição inicial
    # guarda:
    # (posição atual, caminho até ela)
    fila.append((inicio, []))

    # posições já visitadas
    visitados = set()

    # enquanto existir posição na fila
    while fila:

        # pega o primeiro da fila
        posicao, caminho = fila.popleft()

        # evita repetir posição
        if posicao in visitados:
            continue

        # marca como visitado
        visitados.add(posicao)

        # se chegou no player
        if posicao == fim:
            return caminho

        # posição atual
        x, y = posicao

        # posições vizinhas
        # direita, esquerda, baixo, cima
        vizinhos = [

            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)

        ]

        # percorre vizinhos
        for vx, vy in vizinhos:

            # verifica se está dentro do mapa
            dentro_do_mapa = (

                0 <= vy < len(mapa)
                and
                0 <= vx < len(mapa[0])

            )

            if dentro_do_mapa:

                # verifica se NÃO é parede
                if mapa[vy][vx] != "1":

                    # adiciona na fila
                    fila.append(

                        (
                            (vx, vy),
                            caminho + [(vx, vy)]
                        )

                    )

    # se não encontrar caminho
    return []