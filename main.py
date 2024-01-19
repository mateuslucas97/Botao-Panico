import socket
from threading import Thread
from tkinter import *

#import requests

IP_SERVIDOR = '10.16.90.122'
PORTA_DO_SERVIDOR = 8080

class Application:
    def __init__(self, root):
        self.root = root
        self.tela()
        self.criar_interface()

    def tela(self):
        self.root.title('Botão de Emergência')
        self.root.configure(background='white')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        largura = 400
        altura = 400
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')

        self.root.resizable(False, False)

    def criar_interface(self):
        self.criar_botao()
        self.criar_rotulo()

    def criar_botao(self):
        texto_do_botao = 'Chamar'
        tamanho_fonte = 16

        #self.consultorio = 1

        botao = Button(
            self.root,
            text=texto_do_botao,
            command=self.clique_do_botao,
            font=('Arial', tamanho_fonte),
        )
        botao.grid(row=0, column=0, pady=20, padx=20, sticky='nsew')

    def criar_rotulo(self):
        self.rotulo_var = StringVar()
        rotulo = Label(
            self.root, textvariable=self.rotulo_var, font=('Arial', 14)
        )
        rotulo.grid(row=1, column=0, pady=20, padx=20, sticky='nsew')

    def clique_do_botao(self):
        # Cria um thread para enviar a requisição
        thread = Thread(target=self.enviar_chamado)

        # Inicia o thread
        thread.start()

        # Atualiza o rótulo
        self.rotulo_var.set('Chamado Enviado!')

    def enviar_chamado(self):
        try:
            # Cria um socket TCP/IP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conecta-se ao servidor
            sock.connect((IP_SERVIDOR, PORTA_DO_SERVIDOR))

            # Adiciona a identificação à requisição
            solicitacao = 'alerta,' + open('identificacao_cliente.txt', 'r').read()


            # Envia a requisicao
            sock.sendall(solicitacao.encode())

            # Recebe a resposta
            resposta = sock.recv(1024).decode()

            # Fecha a conexão
            sock.close()

            # Verifica a resposta
            if resposta != 'ERRO':
                self.rotulo_var.set('Chamado Enviado!')
                pass
            else:
                self.rotulo_var.set('Erro no Servidor')
                pass
        except Exception as e:
            self.rotulo_var.set('Sem Conexão com o Servidor')
            pass
            
            if resposta == None:
                self.rotulo_var.set('Servidor Indisponivel')


if __name__ == '__main__':
    root = Tk()
    Application(root)
    root.mainloop()
