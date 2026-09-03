# Exemplo de Interface — versão orientada a objetos
# Janela simples: digita um texto, clica no botão, o texto aparece no rótulo.


import tkinter as tk

# Classe principal
class InterfaceExemplo:
    # Metodo construtor (Para criar a janela "tela" principal)
    def __init__(self):
        self.janela = tk.Tk()  # Cria a janela
        self.janela.title("Exemplo de Interface")  # Define o título da janela
        self.janela.geometry("400x150")  # Define o tamanho da janela
        self.janela.configure(bg="#25394c")  # Define a cor de fundo da janela
        self.criar_widgets()  # Chama o método para criar os widgets
        

    # Montar todos os elementos da interface
    def criar_widgets(self):
        # Caixa de entrada"Entry" ou input onde o usuário digita algo "texto"
        self.caixa_texto = tk.Entry(self.janela, width=60)
        self.caixa_texto.pack(pady=10)  # Adiciona a caixa de entrada à janela

        # botão que, quando clicado, chama o método "exibir_texto"
        self.botao = tk.Button(self.janela, text="Mostrar Texto", command=self.mostrar_mensagem)
        self.botao.pack(pady=5)  # Adiciona o botão à janela

        # Rótulo "Label" que mostra a menssagem se o usuário clicar no botão
        self.label_resultado = tk.Label(self.janela, text="", fg="red")
        self.label_resultado.pack(pady=10)  # Adiciona o rótulo à janela

    # Captura o texto digitado pelo usuário (No Entry ou "input") e mostra no Label (Rótulo) da interface
    def mostrar_mensagem(self):
        texto = self.caixa_texto.get()  # Obtém o texto digitado na caixa de entrada
        self.label_resultado.config(text=texto)  # Atualiza o rótulo com o texto digitado

    #Inici o loop princinpal da tela (Isso mantem a tela sendo exibida)
    def executar(self):
        self.janela.mainloop()  # Inicia o loop principal da janela

# ConECTA A CLASSE PRINCIPAL "InterfaceExemplo" e roda o método "executar" para fazer o programa funcionar
if __name__ == "__main__":
    app = InterfaceExemplo()  # Cria uma instância da classe InterfaceExemplo
    app.executar()  # Chama o método para executar a interface

