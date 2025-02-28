from selenium import webdriver
import clicker
import time

# por enquanto a unica solucao foi executar o navegador em modo depuração
# para iniciar o navegador neste modo, o comando abaix no terminal
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"

url = "https://neal.fun/infinite-craft/"

options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9222" 
driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(1)

clicker.teste()

time.sleep(3)
driver.quit()

