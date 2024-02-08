import socket
import os
from threading import Thread
from tkinter import *


IP_SERVIDOR = '10.16.90.122'
PORTA_DO_SERVIDOR = 8080

def verificar_primeira_execucao(root):
        if not os.path.exists('primeira_execucao.txt'):
            janela_identificacao = JanelaIdentificacao(root)
            root.withdraw()  # Hide the main window temporarily
            root.wait_window(janela_identificacao.janela)
            with open('primeira_execucao.txt', 'w') as f:
                pass
        else:
            tela_principal = TelaPrincipal(root)
            tela_principal.criar_tela().root.mainloop()

class Application:
    def __init__(self, root):
        self.root = root

    def executar(self):
        verificar_primeira_execucao(self.root)

class Executar:
    @staticmethod
    def executar():
        root = Tk()
        Executar.inicializar_janela(root)
        Application(root).executar()
        root.mainloop()

    @staticmethod
    def inicializar_janela(root):
        root.title('Emergency Button')
        root.geometry('400x400')
        #root.withdraw()  # Hide the main window temporarily
        root.resizable(False, False)
       
    
class JanelaIdentificacao:
    def __init__(self, root):
        self.root = root

    
        # Cria uma caixa de diálogo para o usuário digitar o número do consultório
        self.janela = Toplevel(self.root)
        self.janela.title('Identificação do Consultório')

        # Cria os widgets da janela
        self.criar_widgets()

        # Define o comportamento do botão "Confirmar"
        self.botao_confirmar = Button(self.janela, text='Confirmar', command=self.confirmar_numero_consultorio)
        self.botao_confirmar.pack(padx=10, pady=10)

        # Adiciona um método para tratar o fechamento da janela
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def criar_widgets(self):
        # Cria um widget de texto para a instrução
        self.texto_instrucao = Label(self.janela, text='Por favor, digite o número do Consultório:')
        self.texto_instrucao.pack(padx=10, pady=10)

        # Cria um widget de entrada para o número do consultório
        self.numero_consultorio_var = StringVar()
        self.numero_consultorio_entry = Entry(self.janela, textvariable=self.numero_consultorio_var)
        self.numero_consultorio_entry.pack(padx=10, pady=5)

    def confirmar_numero_consultorio(self):
        # Valida o número do consultório
        if not self.numero_consultorio_var.get().isdigit():
            # Exibe uma mensagem de erro
            mensagem_erro = Label(self.janela, text='Número do consultório inválido')
            mensagem_erro.pack()
            return

        if int(self.numero_consultorio_var.get()) <= 0:
            # Exibe uma mensagem de erro
            mensagem_erro = Label(self.janela, text='Número do consultório inválido')
            mensagem_erro.pack()
            return

        # Grava o número do consultório no arquivo
        with open('identificacao_cliente.txt', 'w') as f:
            f.write(str(self.numero_consultorio_var.get()))

        # Cria o arquivo "primeira_execucao.txt"
        with open('primeira_execucao.txt', 'w') as f:
            pass

        # Fecha a janela de identificação
        self.janela.destroy()

    def fechar_janela(self):
        # Grava o número do consultório no arquivo
        with open('identificacao_cliente.txt', 'w') as f:
            f.write(str(self.numero_consultorio_var.get()))

        # Cria o arquivo "primeira_execucao.txt"
        with open('primeira_execucao.txt', 'w') as f:
            pass

        # Fecha a janela de identificação
        self.janela.destroy()

class TelaPrincipal:
    def __init__(self, root):
        self.root = root

    def criar_tela(self):
        self.tela()
        self.criar_interface()
        self.root.mainloop()

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
            solicitacao = 'alerta,Consultorio' + open('identificacao_cliente.txt', 'r').read()
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
    #root = Tk()
    #app = Application(root)
    #app.executar()
    Executar.executar()
