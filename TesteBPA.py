import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import os.path

#salvando os dados
def salva():
    local_save = "data\dados.csv"
    file_exists = os.path.isfile(local_save)
    now = datetime.now()

    with open(local_save, "a") as file:
        headers = ['data','nome produto', 'valor produto']
        writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        writer.writerow({'data': now.strftime("%Y-%m-%d"),'nome produto':nome, 'valor produto': preco})

#Url a ser utilizada
url= "https://www.amazon.com.br/"

#browser a ser usado
driver = webdriver.Firefox(executable_path=r'geck\geckodriver.exe')

driver.get(url)
driver.implicitly_wait(10)
#path do site
driver.find_element_by_xpath("// *[@id='twotabsearchtextbox']").send_keys("iphone")
driver.find_element_by_xpath("//*[@id='nav-search-submit-text']/input").click()

url = driver.current_url
response = urlopen(url)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

#percorrendo os dados da primira pagina
index_list = range(0,24,1)
for i in index_list:
    item = soup.find('div', {"data-index": str(i)})
    nome = item.find('span', {'dir':'auto'}).get_text()

    try:
        preco = item.find('span', class_='a-offscreen').text.replace("R$",'').replace('.','')
    except:
        preco = None
    salva()


driver.quit()