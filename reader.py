from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import combinations
import clicker
import time

# por enquanto a unica solucao foi executar o navegador em modo depuração
# para iniciar o navegador neste modo, o comando abaix no cmd
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"

url = "https://neal.fun/infinite-craft/"

options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9222"

def gerar_pares(lista):
    pares_sem_repeticao = list(combinations(lista, 2))    
    pares_com_repeticao = [(x, x) for x in lista]
    return pares_com_repeticao + pares_sem_repeticao

driver = webdriver.Chrome(options=options)

driver.get(url)
print(driver.title)

time.sleep(1)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
elementos = soup.find_all("div", class_="item")
resultados = []
for elemento in elementos:
    texto = "".join(
        child.strip() for child in elemento.contents
        if isinstance(child, str)  # Filtra apenas nós de texto
    )
    if texto:  # Ignora elementos vazios
        resultados.append(texto)

resultados.pop() #remove um water maldito escondido no site

time.sleep(2)

print(f"Elementos encontrados ({len(resultados)}):", resultados)

for par in gerar_pares(resultados):
    print(par)
    clicker.combinar(par[0], par[1])

driver.quit()

