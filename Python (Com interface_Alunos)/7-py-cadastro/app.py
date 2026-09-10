# Cadastro com Login — CustomTkinter + SQLite
# Fluxo: TelaLogin -> (credenciais corretas) -> TelaCadastro -> TelaLista

import customtkinter as ctk
import sqlite3
import hashlib
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import sys


# Obtém p caminho absolutonpara um recurso (imagem/icones), funcionando tanto 
# rodando o .py normalmente quanto depois de empacotado com PyInstaller.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Decide onde o arquivo .db deve ficar: ao lado do .exe quando empacotado,
# ou ao lado do script durante o desenvolvimento - assim os cadastros não 
# se perdem a cada nova versão gerada do executável.
def get_db_path():
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, "cadastro.db")


# Transforma uma senha em texto em um hash SHA-256 (não reversível).
# Simples e sem dependências externas - mais seguro do q guardar a 
# senha em texto puro, mesmo sem ser um esquema de nível produção
# (que normalmente usaria salt + bcrypt/argon2).
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


#Chamada de acesso ao banco de dados: usuário cadastrados + credenciais de login.
class Database:

    def __init__(self, db_name=None):
        self.conn = sqlite3.connect(db_name or get_db_path())
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_admin_user()

    # Criar as tabelas de usuário e cresenciais, se ainda não existirem
    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS credenciais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    # Criar o usuário admin/admin na primeira execução. se ele ainda não existir
    def create_admin_user(self):
        self.cursor.execute("SELECT * FROM credenciais WHERE nome_usuario = 'admin'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(
                "INSERT INTO credenciais (nome_usuario, senha) VALUES (?, ?)",
                ("admin", gerar_hash_senha("admin")),
            )
            self.conn.commit()
            print("Uauário adimin criado com sucesso.")

    # Verificar se usuário e senha batem com o hash salvo no banco
    def verificar_credenciais(self, nome_usuario, senha):
        self.cursor.execute(
            "SELECT * FROM credenciais WHERE nome_usuario =? AND senha = ?",
            (nome_usuario, gerar_hash_senha(senha)),
        )
        return self.cursor. fetchone() is not None

    # Insere um novo usuário cadastrado
    def insert_user(self, nome, email, telefone):
        self.cursor.execute(
            "INSERT INTO usuario (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone),
        )
        self.conn.commit()

    # Retorna todos os usuários cadastrados 
    def get_all_user(self):
        self.cussor.execute("SELECT * FROM usuarios")
        return self.cursor.fetchall()

    # Atualiza os dados de um usuário existente
    def update_user(self, id, nome, email, telefone):
        self.cursor.execute(
            "UPDATE usuarios SET nome=?, email=?, telefone=? WHERE id=?", 
            (nome, email, telefone, id),
        )
        self.conn.commit

    # Remove um usuário do banco de dados
    def delete_user(self, id):
        self.cursor.execute("DELETE FROM usuario WHERE id=?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


# Fosrmata progressivamente um telefone digitado para (xx) xxxxx-xxxx.
# Função solta porque é usada em dois lugares (cadastro e edição) sem 
#  depender de nenhuma instância específica de tela.
def formatar_telefone(texto):
    numeros = "".join(c for c in texto if c.isdigit())[:11]
    formatado = ""

    if len(numeros) > 0:
        formatado += f"({numeros[:2]}"
        if len(numeros) > 2:
            formatado += f") {numeros[2:7]}"
            if len(numeros) > 7:
                formatado += f"-{numeros[7:]}"

    return formatado


class TelaLogin(ctk.CTk):

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.title("Login")
        self.geometry("300x250")

        icon_path = resource_path("entrada.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Login", font=("Roboto", 24))
        self.label.pack(pady=10)

        self.nome_usuario_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome de usuario")
        self.nome_usuario_entry.pack(pady=5, padx=10, fill="x")

        self.senha_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*")
        self.senha_entry.pack(pady=5, padx=10, fill="x")

        self.login_btn = ctk.CTkButton(self.frame, text="Entrar", command=self.fazer_login)
        self.login_btn.pack(pady=10)

# Verifica as credencias digitadas e, se corretas, abre a tela de cadastro
    def fazer_login(self):
        nome_usuario = self.nome_usuario_entry.get()
        senha = self.senha_entry.get()

        if self.db.verificar_credenciais(nome_usuario, senha):
            self.destroy()
            app = TelaCadastro(self.db)
            app.mainloop()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha inválidos.")


class TelaCadastro(ctk.CTk):

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.title("Cadastro de Usuários")
        self.geometry("400x400")

        icon_path = resource_path("entrada.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Ícones para o botão de troca de tema
        self.light_icon = ctk.CTkImage(
            light_image=Image.open(resource_path("light_icon.png")), size=(20, 20)
        )
        self.dark_icon = ctk.CTkImage(
            light_image=Image.open(resource_path("dark_icon.png")), size=(20, 20)
        )

        self.tema_btn = ctk.CTkButton(
            self, image=self.dark_icon, text="", width=30, height=30, command=self.alternar_tema,
        )
        self.tema_btn.place(relx=0.95, rely=0.05, anchor="ne")

        self.label = ctk.CTkLabel(self.frame, text="Cadastro de Usuários", font=("Roboto", 24))
        self.label.pack(pady=10)

        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome")
        self.nome_entry.pack(pady=5, padx=10, fill="x")

        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="E-mail")
        self.email_entry.pack(pady=5, padx=10, fill="x")

        self.telefone_entry = ctk.CTkEntry(self.frame, placeholder_text="Telefone")
        self.telefone_entry.pack(pady=5, padx=10, fill="x")
        self.telefone_entry.bind("<KeyRelease", self.formatar_telefone)

        self.btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.cadastrar_icon = ctk.CTkImage(
            light_image=Image.open(resource_path("cadastrar_icon.png")), size=(20, 20)
        )
        self.cadastrar_icon = ctk.CTkImage(
            light_image=Image.open(resource_path("cancelar_icon.png")), size=(20, 20)
        )
        self.cadastrar_icon = ctk.CTkImage(
            light_image=Image.open(resource_path("listar_icon.png")), size=(20, 20)
        )

        self.cadastrar_btn = ctk.CTkButton(
            self.btn_frame, text="Cadastrar", image=self.cadastrar_icon, compound="left", fg_color="green", hover_color="darkgreen", command=self.cadastrar,
        )
        self.cadastrar_btn.pack(side="left", padx=5)

        self.cancelar_btn = ctk.CTkButton(
            self.btn_frame, text="Cancelar", image=self.cancelar_icon, compound="left", fg_color="darkred", hover_color="red", command=self.quit,
        )
        self.cancelar_btn.pack(side="left", padx=5)

        self.listar_btn = ctk.CTkButton(
            self.frame, text="Listar Cadastros", image=self.listar_icon, compound="left", command=self.abrir_lista,
        )
        self.listar_btn.pack(pady=10, padx=10, fill="x")

    # Formata o telefone enquanto o usuário digita (usa a função solta formatar_telefone)
    def formatar_telefone(self, event):
        formatado = formatar_telefone(self.telefone_entry.get())
        self.telefone_entry.delete(0, "end")
        self.telefone_entry.insert(0, formatado)

    # Valida e cadastra um novo usuário
    def cadastrar(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()

        if nome and email and telefone:
            self.db.insert_user(nome, email, telefone)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def limpar_campos(self):
        self.nome_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")

    # Abra a janela de listagem, escondendo a tela de cadastro por trás
    def abrir_lista(self):
        self.withdraw()
        lista_window = TelaLista(self, self.db)
        lista_window.grab_set()

    def alternar_tema(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.tema_btn.configure(image=self.light_icon)
        else:
            ctk.set_appearance_mode("Dark")
            self.tema_btn.configure(image=self.dark_icon)


class TelaLista(ctk.CTkToplevel):

    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        self.title("Lista de Usuários")
        self.geometry("600x400")

        icon_path = resource_path("entrada.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Lista de Usuário", font=("Roboto", 28))
        self.label.pack(pady=12, pady=10)

        self.style = ttk.Style(self)
        self.configurar_estilo_treeview()

        self.tree = ttk.Treeview(
            self.frame, columns=("ID", "Nome", "E-mail", "Telefone"),
            show="headings", style="Treeview",
        )
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Nome", text="Nome", anchor="center")
        self.tree.heading("E-mail", text="E-mail", anchor="center")
        self.tree.heading("Telefone", text="Telefone", anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=150, anchor="center")
        self.tree.column("E-mail", width=200, anchor="center")
        self.tree.column("Telefone", width=150, anchor="center")
        self.tree.pack(pady=12, padx=10, fill="both", expand=True)

