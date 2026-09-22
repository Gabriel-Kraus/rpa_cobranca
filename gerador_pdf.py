import os
import sqlite3
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def gerar_qrcode_pix(fatura_id, valor):
    # Payload Pix simulado
    payload = f"00020126360014BR.GOV.BCB.PIX0114+55489999999995204000053039865405{valor:.2f}5802BR5913TechSolutions6009PALHOCA62070503***6304"
    qr = qrcode.make(payload)
    
    os.makedirs('boletos', exist_ok=True)
    qr_path = f"boletos/qr_{fatura_id}.png"
    qr.save(qr_path)
    return qr_path

def gerar_boletos_pdf():
    conn = sqlite3.connect('cobranca.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT f.id, c.nome, c.email, c.telefone, c.endereco, f.valor, f.vencimento
        FROM faturas f
        JOIN clientes c ON f.cliente_id = c.id
    ''')
    faturas = cursor.fetchall()

    for fat in faturas:
        fatura_id, nome, email, telefone, endereco, valor, vencimento = fat
        pdf_path = f"boletos/boleto_fatura_{fatura_id}.pdf"
        
        qr_img_path = gerar_qrcode_pix(fatura_id, valor)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # --- CABEÇALHO BANCÁRIO ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, 750, "BANCO TECH")
        c.drawString(150, 750, "| 001-9 |")
        
        # Linha Digitável Fictícia
        linha_digitavel = f"00190.00009 01234.567004 00000.000181 8 {fatura_id}00000{int(valor)}"
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(570, 750, linha_digitavel)
        
        c.setLineWidth(1.5)
        c.line(40, 742, 570, 742)

        # --- TABELA DE INFORMAÇÕES DO BOLETO ---
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.gray)

        # Linha 1: Beneficiário e Vencimento
        c.rect(40, 690, 380, 45)
        c.rect(420, 690, 150, 45)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(45, 725, "BENEFICIÁRIO")
        c.drawString(425, 725, "VENCIMENTO")
        c.setFont("Helvetica", 10)
        c.drawString(45, 705, "TechSolutions Ltda. - CNPJ: 12.345.678/0001-90")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(425, 705, str(vencimento))

        # Linha 2: Pagador e Valor
        c.rect(40, 630, 380, 55)
        c.rect(420, 630, 150, 55)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(45, 675, "PAGADOR")
        c.drawString(425, 675, "VALOR DO DOCUMENTO")
        c.setFont("Helvetica", 9)
        c.drawString(45, 660, f"{nome} - CPF/CNPJ: 000.000.000-00")
        c.drawString(45, 647, f"Endereço: {endereco}")
        c.drawString(45, 635, f"Contato: {email} | {telefone}")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(425, 645, f"R$ {valor:.2f}")

        # --- SEÇÃO PIX / QR CODE ---
        c.rect(40, 480, 530, 140)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(55, 600, "PAGUE COM PIX - FÁCIL E RÁPIDO")
        
        c.setFont("Helvetica", 9)
        c.drawString(55, 570, "1. Abra o app do seu banco preferido.")
        c.drawString(55, 550, "2. Escolha a opção de pagamento via QR Code / Pix.")
        c.drawString(55, 530, "3. Aponte a câmera para a imagem ao lado.")
        c.drawString(55, 500, f"Identificador da Fatura: #{fatura_id}")

        # Inserção do QR Code
        c.drawImage(qr_img_path, 425, 490, width=120, height=120)

        # --- CÓDIGO DE BARRAS SIMULADO (LINHAS SEPARADORES) ---
        c.setFont("Helvetica", 8)
        c.drawString(40, 460, "CÓDIGO DE BARRAS (ILUSTRATIVO)")
        
        c.setFillColor(colors.black)
        x_pos = 40
        # Desenha barramento fictício variando espessuras
        for i in range(65):
            w = 2 if i % 3 == 0 else 1
            c.rect(x_pos, 400, w, 55, fill=True, stroke=False)
            x_pos += w + (3 if i % 5 == 0 else 1.5)

        # Rodapé
        c.setFillColor(colors.gray)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(305, 370, "Este boleto é uma demonstração do módulo de automação RPA.")

        c.save()
        
        # Limpa arquivo temporário de QR Code
        if os.path.exists(qr_img_path):
            os.remove(qr_img_path)

        print(f"Boleto bancário em PDF gerado: {pdf_path}")

    conn.close()
    print("Todos os boletos em PDF foram gerados com sucesso!")

if __name__ == '__main__':
    gerar_boletos_pdf()