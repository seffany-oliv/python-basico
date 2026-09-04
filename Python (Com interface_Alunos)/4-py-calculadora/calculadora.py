# Calculadora SENAI — ttkbootstrap
# Calculadora com display, botões numéricos/operadores e troca de tema.

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from functools import partial
import os
import sys



# Obtém o caminho para um recurso, funcionando tanto rodando o .py normalmente quanto depois de empacotado com PyInstaller
def resource_path(relative_path):
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho nela
        base_path = sys._MEIPASS
    except AttributeError:
        # Caso contrário, usa o caminho absoluto do diretório atual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Calculadora:
    CARACTERES_PERMITIDOS = set("0123456789.+-*/()** ")

    def __init__(self):
        self.janela = ttk.Window(themename="darkly")
        self.janela.geometry("400x750")
        self.janela.title("Calculadora SENAI")

        # Definição de cores e fontes
        self.cor_fundo = "black"
        self.cor_botao = "secondary"
        self.cor_texto = "white"
        self.cor_operador = "warning"
        self.fonte_padrao = ("roboto", 18)
        self.fonte_display = ("roboto", 36)

        self.janela.iconbitmap(resource_path("calc.ico"))

        self.criar_display()
        self.criar_botoes()
        self.criar_imagem_senai()
        self.criar_selecao_tema()

    # Área onde a expressão/resultado é exibido
    def criar_display(self):
        self.frame_display = ttk.Frame(self.janela)
        self.frame_display.pack(fill="both", expand=True)

        self.display = ttk.Label(
            self.frame_display,
            text="",
            font=self.fonte_display,
            anchor="e", # Alinha o texto á direita
            padding=(20, 10),
        )
        self.display.pack(fill="both", expand=True)

    # Grade de botões numéricos e operadores
    def criar_botoes(self):
        self.frame_botoes = ttk.Frame(self.janela)
        self.frame_botoes.pack(fill="both", expand=True)

        self.botoes = [
            ["C", "🗑️", "^", "/"],
            ["7", "8", "9", "x"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "-"],
            [".", "0", "()", "="],
        ]

        operadores = {"C", "🗑️", "^", "/", "x", "+", "-", "="}

        for i, linha in enumerate(self.botoes):
            for j, texto in enumerate(linha):
                estilo = "warning.TButton" if texto in operadores else "secondary.TButton"
                botao = ttk.Button(
                    self.frame_botoes,
                    text=texto,
                    style=estilo,
                    width=10,
                    command=partial(self.interpretar_botao, texto),
                )
                botao.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")

        # Faz linhas e colunas crecerem prporcionamente ao redimensionar
        for i in range(5):
            self.frame_botoes.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.frame_botoes.grid_columnconfigure(j, weight=1)

    # Logo do SENAI exibida abaixo dos botões
    def criar_imagem_senai(self):
        self.frame_imagem = ttk.Frame(self.janela)
        self.frame_imagem.pack(fill="both", expand=True, pady=10)

        imagem = Image.open(resource_path("senai.png"))
        imagem = imagem.resize((300, 100), Image.Resampling.LANCZOS)
        self.imagem_tk = ImageTk.PhotoImage(imagem) # Guarda a referência

        label_imagem = ttk.Label(self.frame_imagem, image=self.imagem_tk, text="")
        label_imagem.pack()

    # ComboBox para trocar o tema visual da caculadora
    def criar_selecao_tema(self):
        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill="x", pady=10, padx=10)

        self.label_tema = ttk.Label(self.frame_tema, text="Escolher Tema:", font=("roboto", 12))
        self.label_tema.pack(side="top", pady=(0, 5))

        self.temas = [
            "darkly", "cosmo", "flatly", "journal", "litera", "lumen", "minty", "pulse", "sandstone", "united", "yeti", "morph", "simplex", "cerculean",
        ]
        self.selector_tema = ttk.Combobox(self.frame_tema, values=self.temas, state="readonly")
        self.selector_tema.set("darkly")
        self.selector_tema.pack(side="top", fill="x")
        self.selector_tema.bind("<<ComboboxSelected>>", self.mudar_tema)

    def mudar_tema(self, evento):
        novo_tema = self.selector_tema.get()
        self.janela.style.theme_use(novo_tema)

    # Interpreta o botão pressionado e atualiza o display
    def interpretar_botao(self, valor):
        texto_atual = self.display.cget("text")

        if valor == "C":
            self.display.configure(text="")
        elif valor == "🗑️":
            self.display.configure(text=texto_atual[:-1])
        elif valor == "=":
            self.calcular()
        elif valor == "()":
            # DECIDE SE ABRE OU FECHA PARÊNTESES BASEADO NO TEXTO ATUAL
            if not texto_atual or texto_atual[-1] in "+-/^x":
                self.display.configure(text=texto_atual + "(")
            elif texto_atual[-1] in "0123456789)":
                self.display.configure(text=texto_atual + ")")
        else:
            self.display.configure(text=texto_atual + valor)

    # Calcular o resultado da expressão exibida no display
    def calcular(self):
        expressao = self.display.cget("text")
        expressao = expressao.replace("x", "*").replace("^", "**")

        # Só aceita avaliar a expressão se ela contiver apenas dígitos, operadores e parênteses - evita rodar qualquer código arbitrário digitado no dysplay através do eval() logo abaixo.
        if not expressao or not set(expressao) <= self.CARACTERES_PERMITIDOS:
            self.display.configure(text="Erro")
            return
        
        try:
            # eval() com_builtins_vazio: calcula só a expressão matemática, sem acesso a funções do python (import, open, etc)
            resultado = eval(expressao, {"__builtins__": {}})
            self.display.configure(text=str(resultado))
        except (SyntaxError, ZeroDivisionError, ValueError):
            self.display.configure(text="Erro")

    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = Calculadora()
    app.executar()


