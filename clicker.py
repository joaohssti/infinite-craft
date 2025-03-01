import json
import pyautogui
import win32api
import win32con
import time

# retorna as coordenadas de todos os itens que devem ser clicados
def ler_cliques_json(arquivo_entrada):
    with open(arquivo_entrada, "r") as f:
        cliques = json.load(f)
    return cliques

# lê um dicionário de posições e arrasta de uma chave até a outra
def arrastar_objeto(coordenadas, botao_origem, botao_destino):
    origem = coordenadas.get(botao_origem)
    destino = coordenadas.get(botao_destino)

    x_inicial, y_inicial = origem["x"], origem["y"]
    x_final, y_final = destino["x"], destino["y"]

    win32api.SetCursorPos((x_inicial, y_inicial))
    time.sleep(0.1)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    
    passos = 15
    # muda a posição do mouse mais devagar para o navegador detectar
    for i in range(passos):
        x = int(x_inicial + (x_final - x_inicial) * (i / passos))
        y = int(y_inicial + (y_final - y_inicial) * (i / passos))
        win32api.SetCursorPos((x, y))
        time.sleep(0.01)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)

def clicar_soltar(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)

# clica na pesquisa e escreve o nome do item
def pesquisar_item(nome_item, coordenadas, chave):
    posicao = coordenadas.get(chave)
    x, y = posicao["x"], posicao["y"]

    clicar_soltar(x, y)

    pyautogui.write(nome_item)


def combinar(item1, item2):
    coord = ler_cliques_json("positions.json")

    # pesquisa item 1
    pesquisar_item(item1, coord, "bt_pesquisa")

    # arrasta
    arrastar_objeto(coord, "bt_1item", "bt_espacoBranco")

    # fecha pesquisa
    clicar_soltar(coord["bt_fecharPesquisa"]["x"], coord["bt_fecharPesquisa"]["y"])

    # pesquisa item 2
    pesquisar_item(item2, coord, "bt_pesquisa")
    
    # arrasta
    arrastar_objeto(coord, "bt_1item", "bt_espacoBranco")

    # fecha pesquisa
    clicar_soltar(coord["bt_fecharPesquisa"]["x"], coord["bt_fecharPesquisa"]["y"])

    # limpa 
    clicar_soltar(coord["bt_limpar"]["x"], coord["bt_limpar"]["y"])

if __name__ == "__main__":
    
    combinar("fire", "water")
