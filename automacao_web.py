from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os 
import time 
from bs4 import BeautifulSoup as soup
import pandas as pd 

# Caminho do chromedriver
PATH_EXE = os.getcwd()
PATH_CHROME_DRIVER = os.path.join(PATH_EXE, 'chromedriver.exe')

# Inicialize o navegador Chrome usando o ChromeDriver
driver = webdriver.Chrome(PATH_CHROME_DRIVER)

# Acesse o site da upf
driver.get('https://ge.globo.com/')
driver.maximize_window()

# Verifica se carregou a pagina
while True:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="feed-placeholder"]')))
        break
    except:
        pass 

# Seleciona os itens menu
driver.find_element(By.XPATH, '//div[@class="menu-area"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="menu-1-tabelas"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="menu-2-nacionais"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="menu-3-brasileirao-serie-a"]').click()
time.sleep(1)

# Verifica se carregou a pagina
while True:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//table[@class="tabela__equipes tabela__equipes--com-borda"]')))
        break
    except:
        pass 

page_html = driver.page_source
page_soup = soup(page_html, "html.parser")

#table equipes
table = page_soup.find_all('table', attrs={'class': 'tabela__equipes tabela__equipes--com-borda'})
df_equipe = pd.read_html(str(table))[0].dropna(axis=1, how='all')

#table equipes
table = page_soup.find_all('table', attrs={'class': 'tabela__pontos'})
df_pontos = pd.read_html(str(table))[0].dropna(axis=1, how='all')

# realiza o merge entre os dois dataframes
merged_df = pd.concat([df_equipe, df_pontos], axis=1)
merged_df = merged_df.drop('Classificação.2', axis=1)
merged_df.to_csv('classificao_brasileirao.csv', index=False, sep=';', encoding='utf-8-sig')
merged_df = merged_df.drop('Classificação', axis=1)
merged_df.to_json('classificao_brasileirao.json', indent=4, force_ascii=False)


# LTE preencher formularios
driver.get('https://adminlte.io/themes/AdminLTE/pages/forms/general.html')

# Verifica se carregou a pagina
while True:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="content-wrapper"]')))
        break
    except:
        pass 

# preenche campo de de email
driver.find_element(By.XPATH, '//*[@id="exampleInputEmail1"]').send_keys('mbarquette97@gmail.com')
time.sleep(1)
# preenche campo de de password
driver.find_element(By.XPATH, '//*[@id="exampleInputPassword1"]').send_keys('mbarquette97@gmail.com')
time.sleep(1)
# preenche campo de de file
file = os.path.join(PATH_EXE, 'classificao_brasileirao.json')
driver.find_element(By.XPATH, '//*[@id="exampleInputFile"]').send_keys(f'{file}')
time.sleep(1)
# preenche campo de de checkbox
driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
time.sleep(1)

# preenche campo de de submit
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(1)

# Fecha navegador
driver.quit()