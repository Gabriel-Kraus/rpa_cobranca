import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By

def executar_rpa_cadastro():
    # 1. Carrega a planilha de entrada
    wb = openpyxl.load_workbook("clientes_input.xlsx")
    sheet = wb.active

    # 2. Inicia o navegador Chrome
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    driver.maximize_window()

    # Iterar pelas linhas a partir da segunda (pula cabeçalho)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        nome, email, telefone, endereco, valor, vencimento = row

        # Preenche os campos do formulário
        driver.find_element(By.NAME, "nome").send_keys(str(nome))
        driver.find_element(By.NAME, "email").send_keys(str(email))
        driver.find_element(By.NAME, "telefone").send_keys(str(telefone))
        driver.find_element(By.NAME, "endereco").send_keys(str(endereco))
        driver.find_element(By.NAME, "valor").send_keys(str(valor))
        driver.find_element(By.NAME, "vencimento").send_keys(str(vencimento))

        # Clica no botão de cadastrar
        driver.find_element(By.ID, "btn-cadastrar").click()
        time.sleep(1) # Aguarda processamento

    driver.quit()
    print("RPA de cadastro finalizado com sucesso!")

if __name__ == '__main__':
    executar_rpa_cadastro()