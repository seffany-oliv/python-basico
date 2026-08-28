import os #Biblioteca para habilitar cmd's terminal
import sqlite3 #Banco de dados

#variavel com nome do BD a ser criado
CAMINHO_BANCO = "jogos.db"

def exibir_cabecalho(texto):
    os.system('cls')

    #criar um efeito visul na palavra "GameVault"
    linha ="*" *len(texto)
    print(linha)
    print(texto)
    print(linha)
    print()#Linha em branco

exibir_cabecalho("GameVault")

def inicializar_banco():
    #Abre a conexão com o banco de dados (O indicado em: "CAMINHO_BANCO" no caso: "jogo.db")
    conn = sqlite3.connect(CAMINHO_BANCO)

    #Diz ao BD que de fato SQL está habilitado
    cursor = conn.cursor()

    #Executa de fato o comando Sql descrito abaixo
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            zerado BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )

    #Funciona como"Ctrl + S" ou salva, ele que grava
    conn.commit()
    #Fecha conexão
    conn.close()

# Chama a função
inicializar_banco()


def listar_jogos():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, plataforma, zerado FROM jogos")

    #"fetchall" - Devolve todas as linhas do resultado como uma Tupla
    jogos = cursor.fetchall()

    conn.close()

    # Se bd vasio mostra a mensagen abaixo
    if not jogos:
        print("Nenhum jogo cadastrado ainda!\n")
        return

    # Formam o cabeçalho visual antes de listar com 55 traços e alinhamento a esquerda "ljust"
    print(f"{'Título'.ljust(25)} | {'Plataforma'.ljust(12)} | Status")
    print("-" * 55)

    # Laço para exibir todos os jogos cadastrados
    for titulo, plataforma, zerado in jogos:
        status = "zerado" if zerado else "jogando"
        print(f"{titulo.ljust(25)} | {plataforma.ljust(12)} | {status}")

    print() # Linha em branco para não colar no próximo print

def adicionar_jogo(titulo, plataforma):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor() 
    # SQL - Para inserir novos jogos
    cursor.execute("INSERT INTO jogos (titulo, plataforma, zerado) VALUES (?, ?, ?)", (titulo, plataforma, False),
    )

    conn.commit()
    conn.close()

def excluir_jogo(titulo, plataforma):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor() 
    # SQL - Para inserir novos jogos
    cursor.execute("DELETE FROM jogos WHERE titulo = ? AND plataforma = ?", (titulo, plataforma),
    )

    conn.commit()
    conn.close()    

def marcar_como_zerado(titulo):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    #sql - Para atualizar status de jogo zerado
    cursor.execute("UPDATE jogos SET zerado = ? WHERE titulo = ?", (True, titulo),
    )

    #Guarda quantas linhas foram afetadas
    encontrou = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return encontrou

def buscar_jogo(titulo, plataforma):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor() 
    # SQL - Para inserir novos jogos
    cursor.execute("UPDATE jogos SET zerado = ? WHERE titulo = ?", (True, titulo),
    )

    #Pegar somente o exto nome que bater (Somente ele)
    jogo = cursor.fetchone()

    conn.close()
    return jogo

def atualizar_jogo(titulo_atual, novo_titulo, nova_plataforma):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    #SQL - Para atualizar a informação do BD
    cursor.execute("UPDATE jogo SET titulo = ?, plataforma =?",(titulo_atual, novo_titulo, nova_plataforma)
    )    

    #Guarda quantas linhas foram afetadas na atualização
    encontrou = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return encontrou

def exibir_menu():
    exibir_cabecalho("GameVault")
    print("1. Adicionar jogo")
    print("2. Listar jogo")
    print("3. Marcar jogo como zerado")
    print("4. Excuir")
    print("5. Editar jogo")
    print("6. Sair\n")



def pausar():
    input("pressione Enter para voltar ao menu")

def main():
    inicializar_banco()

    while True:
        exibir_menu()
        opcao = input("Escolher uma opção:")

        if opcao == "1":
            exibir_cabecalho("Adicionar jogo")
            titulo = input("Título do jogo: ")
            plataforma = input("Plataforma: ")
            adicionar_jogo(titulo, plataforma)
            print(f"\n'{titulo} adicionado com sucesso")
            pausar()

        elif opcao == "2":
            exibir_cabecalho("Seus jogos")
            listar_jogos()
            pausar()
        elif opcao == "3":
            exibir_cabecalho("Marcar como zerado")
            titulo = input("Título do jogo que zerou: ")

            if marcar_como_zerado(titulo):
                print(f"\n'{titulo}' marcar como zerado")
            else:
                print(f"\n'{titulo}'Não encontrado!")
                print("Confira se digitou corretamente.")
                pausar()

        elif opcao == "4":
            exibir_cabecalho("Execluir jogo")
            titulo = input("Título do jogo: ")
            plataforma = input("Plataforma: ")
            excluir_jogo(titulo, plataforma)
            print(f"\n'{titulo} excluido com sucesso")
            pausar()

        elif opcao == "5":
            exibir_cabecalho("Editar jogo")
            titulo = input("Título do jogo que deseja atualizar: ")

            jogo = buscar_jogo(titulo)

            if jogo is None:
                print(f"\n'{titulo}' Não encontrado!")
                print("cofira se digitou corretamente.")
            else:
                titulo_atual, plataforma_atual = jogo
                print(f"\n Jogo encontrado: '{titulo_atual}'({plataforma_atual})")

                novo_titulo = input(f" Novo título (Enter para manter)'{titulo_atual}' ): ")
                novo_plataforma = input(f" Novo plataforma (Enter para manter)'{plataforma_atual}' ): ")               

                if novo_titulo.split() =="":
                    novo_titulo = titulo_atual
                if novo_plataforma.split() =="":
                    novo_plataforma = plataforma_atual

                atualizar_jogo(titulo_atual, novo_titulo, novo_plataforma)
                input(f" Novo título atualizado para: '{novo_titulo}' ({novo_plataforma}) com sucesso")

                pausar()          



            
        elif opcao == "6":
            print("Até a próxima!")
            break

        else:
            # Caso o usuário digite uma opsão invalida
            print("Opição inválida! Escolha um número de 1 a 6.")
            pausar()         

# Fechar função main
if __name__ == "__main__":
    main()




