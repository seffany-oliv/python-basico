# Interface Avançada — versão orientada a objetos
# Formulário com Entry, RadioButtons, Checkboxes e ComboBox,
# que monta uma mensagem personalizada a partir das escolhas do usuário.

import  tkinter as tk
from tkinter import ttk

class InterfaceAvancada:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Interface Avançada")
        self.janela.geometry("400x500")
        self.criar_widgets()

    def criar_widgets(self):
        # Caixa de entrada para nome
        tk.Label(self.janela, text="Digite seu nome: ").pack(pady=5)
        # Input da caixa
        self.caixa_texto = tk.Entry(self.janela, width=40)
        self.caixa_texto.pack(pady=5)

        # Botões de radio (Escolha de apenas 1 opção)
        tk.Label(self.janela, text="Escolha sua preferência: ").pack(pady=5)
        # Opção padrão ""Café""
        self.var_radio = tk.StringVar(value="Café")
        # Laço for para as outras opções
        for opcao in ["Café", "Chá", "Suco", "Água"]:
            tk.Radiobutton(
                self.janela, text=opcao, variable=self.var_radio, value=opcao
            ).pack()

        # Caixa de seleção
        self.var_check_saudacao = tk.BooleanVar()
        tk.Checkbutton(
            self.janela,
            text="Saudação informal",
            variable=self.var_check_saudacao,
        ).pack(pady=5)

        self.var_check_personalizada = tk.BooleanVar()
        tk.Checkbutton(
            self.janela,
            text="Saudação personalizada",
            variable=self.var_check_personalizada,
        ).pack(pady=5)

        # ComboBox para escolher sua cor favorita
        tk.Label(self.janela, text="Escolha sua cor favorita:").pack(pady=5)
        self.combo_cor = ttk.Combobox(
            self.janela,
            values=["Vermelho", "Azul", "Verde", "Amarelo", "Preto", "Branco"],
        )
        self.combo_cor.pack(pady=5)

        # Botões de ação

        # Atualizar
        tk.Button(
            self.janela, text="Atualizar", command=self.atualizar_resultado
        ).pack(pady=10)

        # Limpar
        tk.Button(
            self.janela, text="Limpar", command=self.limpar_campos
        ).pack(pady=10)

        # Rótulo ou "label" onde a mensagem final é exibida
        self.label_resultado = tk.Label(self.janela, text="", wraplength=350)
        self.label_resultado.pack(pady=10)

    def montar_saudacao(self):
        # Saudação normal
        saudacao = "Olá" if self.var_check_saudacao.get() else "Bem-vindo"

        # Saudação personalizada
        if self.var_check_personalizada.get():
            saudacao = f"{saudacao}. caro(a)"

        return saudacao

    def atualizar_resultado(self):
        # Captura todas as opções escolhidas pelo usuário
        nome = self.caixa_texto.get()
        preferencia = self.var_radio.get()
        saudacao = self.montar_saudacao()
        cor_favorita = self.combo_cor.get()

        # Forma a frase dizendo as opções escolhidas pelo usuário
        mensagem = f"{saudacao} {nome}! Você prefere {preferencia}."
        if cor_favorita:
            mensagem += f" Sua cor favorita é: {cor_favorita}."

        self.label_resultado.config(text=mensagem)

    def limpar_campos(self):
        # Limpa todas as opções para voltar ao estado inicial
        self.caixa_texto.delete(0, tk.END)
        self.var_radio.set("Café")
        self.var_check_saudacao.set(False)
        self.var_check_personalizada.set(False)
        self.combo_cor.set("")
        self.label_resultado.config(text="")

    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = InterfaceAvancada()
    app.executar()