import sqlite3
import time
import os
import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def formatar_telefone(telefone):
    # Trata o telefone para manter apenas dígitos numéricos
    num_limpo = re.sub(r'\D', '', str(telefone))
    # Adiciona o DDI do Brasil (55) se não houver
    if not num_limpo.startswith('55'):
        num_limpo = '55' + num_limpo
    return num_limpo

def enviar_notificacoes_whatsapp():
    conn = sqlite3.connect('cobranca.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.nome, c.telefone, f.valor, f.vencimento
        FROM faturas f
        JOIN clientes c ON f.cliente_id = c.id
    ''')
    faturas = cursor.fetchall()
    conn.close()

    if not faturas:
        print("Nenhuma fatura encontrada no banco de dados!")
        return

    chrome_options = Options()
    perfil_path = os.path.join(os.getcwd(), "whatsapp_profile")
    chrome_options.add_argument(f"user-data-dir={perfil_path}")
    # Desativa flags de automação que às vezes travam a abertura do perfil
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("\n[ERRO CRÍTICO] O Chrome/Selenium não conseguiu iniciar.")
        print("Certifique-se de fechar TODAS as janelas do Chrome antes de rodar!\n")
        raise e

    driver.get("https://web.whatsapp.com")
    driver.maximize_window()
    
    print("Aguardando o WhatsApp Web carregar completamente...")
    
    try:
        # Espera até 60 segundos o painel principal do WhatsApp carregar
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
        )
        print("WhatsApp Web conectado e carregado com sucesso!")
    except Exception:
        print("Tempo esgotado aguardando login ou carregamento do WhatsApp Web.")

    for fat in faturas:
        nome, telefone, valor, vencimento = fat
        
        tel_formatado = formatar_telefone(telefone)
        mensagem = f"Olá {nome}, sua fatura de R$ {valor:.2f} vence em {vencimento}. O boleto foi enviado para seu e-mail."
        msg_codificada = urllib.parse.quote(mensagem)
        
        link_chat = f"https://web.whatsapp.com/send?phone={tel_formatado}&text={msg_codificada}"
        driver.get(link_chat)
        
        time.sleep(6)

        try:
            # Aguarda e tenta clicar na caixa de texto do chat para dar Enter ou clicar no botão de envio
            caixa_texto = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            time.sleep(1)
            caixa_texto.send_keys(Keys.ENTER)
            print(f"Mensagem enviada com sucesso para {nome} ({tel_formatado})")
            time.sleep(3)
        except Exception as e:
            print(f"Não foi possível enviar para {nome} (número inexistente/inválido ou erro de carregamento).")

    input("\nPressione ENTER no terminal para fechar o navegador...")
    driver.quit()

if __name__ == '__main__':
    enviar_notificacoes_whatsapp()