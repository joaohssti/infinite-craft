import json
import time
import win32api
import win32con

locais_clique = ["1item", "espacoBranco", "limpar", "pesquisa", "fecharPesquisa"]

def gravar_cliques_json(locais, arquivo_saida="positions.json"):

    cliques = {}

    for i in locais:

        print(f"Clique no local do botão bt{i}...")

        while True:
            
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0:
                x, y = win32api.GetCursorPos()
                cliques[f"bt_{i}"] = {"x": x, "y": y}
                print(f"bt{i} mapeado em ({x}, {y})")
                time.sleep(0.5)
                break

    with open(arquivo_saida, "w") as f:
        json.dump(cliques, f, indent=4)

    print(f"Posições dos cliques salvas em {arquivo_saida}")

if __name__ == "__main__":
    gravar_cliques_json(locais=locais_clique)