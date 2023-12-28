from tkinter import *

import requests


class Application():
    def __init__(self, root):
        self.root = root
        self.tela()
        self.ip_do_servidor = "192.168.0.51"
        self.criar_interface()

    def tela(self):
        self.root.title("Botão de Emergência")
        self.root.configure(background = 'white')
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        largura = 400
        altura = 400
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela - largura)  //2
        y = (altura_tela - altura) // 2
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

        self.root.resizable(False, False)

    def criar_interface(self):
        self.criar_botao()
        self.criar_rotulo()

    def criar_botao(self):
        texto_do_botao = "Chamar"
        tamanho_fonte = 16

        botao = Button(self.root, text=texto_do_botao, command=self.clique_do_botao, font=("Arial", tamanho_fonte))
        botao.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

    def criar_rotulo(self):
        self.rotulo_var = StringVar()
        rotulo = Label(self.root, textvariable=self.rotulo_var, font=("Arial", 14))
        rotulo.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
    
    def clique_do_botao(self):
         self.enviar_chamado()

    def enviar_chamado(self):
        try:
            url = f"http://{self.ip_do_servidor}/"
            response = requests.post(url, data="Chamado Enviado!")

            if response.status_code == 220:
                self.rotulo_var.set("Chamado Enviado!")
            else:
                self.rotulo_var.set("Erro no Servidor")
        except requests.RequestException as e:
            self.rotulo_var.set("Sem Conexão com o Servidor")
            self.root.after(1000, self.enviar_chamado)
        

if __name__ == "__main__":
    root = Tk()
    Application(root)
    root.mainloop()