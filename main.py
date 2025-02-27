import clicker
import ui

positions_file = "posicao_cliques.json"



def main():
    positions = clicker.ler_cliques_json(positions_file)

    clicker.arrastar_objeto()

if __name__ == "__main__":
    main()