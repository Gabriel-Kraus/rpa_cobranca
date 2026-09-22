import sqlite3
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def enviar_emails_cobranca():
    # Insira seu e-mail e Senha de Aplicativo caso queira realizar o envio real
    EMAIL_REMETENTE = "seu_email@gmail.com"
    SENHA_REMETENTE = "sua_senha_de_aplicativo"

    conn = sqlite3.connect('cobranca.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT f.id, c.nome, c.email, f.valor, f.vencimento
        FROM faturas f
        JOIN clientes c ON f.cliente_id = c.id
    ''')
    faturas = cursor.fetchall()
    conn.close()

    # Identifica se o usuário manteve os dados padrão para rodar apenas como simulação
    simulacao = (EMAIL_REMETENTE == "seu_email@gmail.com" or SENHA_REMETENTE == "sua_senha_de_aplicativo")

    server = None
    if not simulacao:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        except Exception as e:
            print(f"Aviso: Não foi possível conectar ao servidor SMTP. Executando em modo simulação: {e}")
            simulacao = True

    for fat in faturas:
        fatura_id, nome, email_destino, valor, vencimento = fat
        pdf_path = f"boletos/boleto_fatura_{fatura_id}.pdf"

        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = email_destino
        msg['Subject'] = f"Fatura de Cobrança - TechSolutions (Nº {fatura_id})"

        corpo = f"Olá {nome},\n\nSegue em anexo a sua fatura no valor de R$ {valor:.2f} com vencimento para {vencimento}.\n\nAtenciosamente,\nTechSolutions Ltda."
        msg.attach(MIMEText(corpo, 'plain'))

        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
                msg.attach(part)

        if not simulacao and server:
            server.send_message(msg)
            print(f"E-mail enviado via SMTP para {nome} ({email_destino})")
        else:
            print(f"[SIMULAÇÃO] E-mail preparado com sucesso para {nome} ({email_destino}) com o anexo {pdf_path}")

    if server:
        server.quit()
        
    print("Envio de e-mails concluído!")

if __name__ == '__main__':
    enviar_emails_cobranca() 