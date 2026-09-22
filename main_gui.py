import sys
import os
import subprocess
import threading
import customtkinter as ctk
from tkinter import messagebox

# Configuração do Tema Escuro
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def executar_script_async(nome_script, mensagem_sucesso, botao):
    def worker():
        # Animação visual de processamento no botão
        texto_original = botao.cget("text")
        botao.configure(state="disabled", text="⏳ Executando...")
        
        try:
            subprocess.run([sys.executable, nome_script], check=True)
            messagebox.showinfo("Sucesso", mensagem_sucesso)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar {nome_script}:\n{e}")
        finally:
            # Restaura o botão ao estado original
            botao.configure(state="normal", text=texto_original)

    threading.Thread(target=worker, daemon=True).start()

def abrir_planilha_excel():
    caminho_planilha = "clientes_input.xlsx"
    if os.path.exists(caminho_planilha):
        try:
            os.startfile(caminho_planilha)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a planilha:\n{e}")
    else:
        messagebox.showwarning("Aviso", f"O arquivo '{caminho_planilha}' não foi encontrado!")

# Janela Principal
app = ctk.CTk()
app.title("Sistema de Automação de Cobrança - RPA")
app.geometry("480x560")
app.resizable(False, False)

# Cabeçalho / Título
frame_topo = ctk.CTkFrame(app, fg_color="transparent")
frame_topo.pack(pady=(25, 15))

lbl_titulo = ctk.CTkLabel(frame_topo, text="Painel de Controle RPA", font=ctk.CTkFont(size=20, weight="bold"))
lbl_titulo.pack()

lbl_subtitulo = ctk.CTkLabel(frame_topo, text="Selecione um módulo para executar a automação", font=ctk.CTkFont(size=12), text_color="gray")
lbl_subtitulo.pack(pady=(2, 0))

# Frame do Conteúdo Principal
frame_botoes = ctk.CTkFrame(app, corner_radius=15)
frame_botoes.pack(fill="both", expand=True, padx=25, pady=(0, 20))

# Botões Dinâmicos e Arredondados
btn_excel = ctk.CTkButton(
    frame_botoes, text="📊 Visualizar Planilha de Clientes", 
    command=abrir_planilha_excel,
    fg_color="#1f2937", hover_color="#374151", height=42, corner_radius=10,
    font=ctk.CTkFont(size=13, weight="bold")
)
btn_excel.pack(fill="x", padx=20, pady=(20, 10))

# Separador Visual
separador = ctk.CTkFrame(frame_botoes, height=2, fg_color="#2d3748")
separador.pack(fill="x", padx=20, pady=5)

# Lista de ações do RPA
btn1 = ctk.CTkButton(frame_botoes, text="1. Cadastrar Clientes no Sistema Web", height=42, corner_radius=10, font=ctk.CTkFont(size=13))
btn1.configure(command=lambda: executar_script_async("rpa_cadastro.py", "Clientes cadastrados com sucesso!", btn1))
btn1.pack(fill="x", padx=20, pady=8)

btn2 = ctk.CTkButton(frame_botoes, text="2. Gerar Boletos em PDF com QR Code", height=42, corner_radius=10, font=ctk.CTkFont(size=13))
btn2.configure(command=lambda: executar_script_async("gerador_pdf.py", "Boletos gerados com sucesso!", btn2))
btn2.pack(fill="x", padx=20, pady=8)

btn3 = ctk.CTkButton(frame_botoes, text="3. Enviar Notificações via WhatsApp Web", height=42, corner_radius=10, font=ctk.CTkFont(size=13))
btn3.configure(command=lambda: executar_script_async("rpa_whatsapp.py", "Envio via WhatsApp finalizado!", btn3))
btn3.pack(fill="x", padx=20, pady=8)

btn4 = ctk.CTkButton(frame_botoes, text="4. Enviar Faturas por E-mail", height=42, corner_radius=10, font=ctk.CTkFont(size=13))
btn4.configure(command=lambda: executar_script_async("rpa_email.py", "Disparo de e-mails concluído!", btn4))
btn4.pack(fill="x", padx=20, pady=8)

# Rodapé
lbl_rodape = ctk.CTkLabel(app, text="TechSolutions Ltda - Módulo de Cobrança RPA", font=ctk.CTkFont(size=11, slant="italic"), text_color="gray")
lbl_rodape.pack(side="bottom", pady=12)

app.mainloop()