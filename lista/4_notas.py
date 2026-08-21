# Lista de notas de 5 alunos
notas = [
    [8.5, 7.0, 9.0],  # Notas do aluno 1
    [6.0, 5.5, 7.5],  # Notas do aluno 2
    [9.0, 8.5, 10.0], # Notas do aluno 3
    [4.0, 6.5, 5.0],  # Notas do aluno 4
    [7.5, 8.0, 6.5]   # Notas do aluno 5
]

# calcular a media dos alunos e exibir so a maior media
maior_media = 0
for i, aluno in enumerate(notas):
    media = sum(aluno) / len(aluno)
    print(f"Aluno {i + 1}: Média = {media:.2f}")
    if media > maior_media:
        maior_media = media

print(f"A maior média da sala é: {maior_media:.2f} do aluno {notas.index(max(notas, key=lambda x: sum(x)/len(x))) + 1}")

#calcular a media da sala
media_sala = sum(sum(aluno) for aluno in notas) / (len(notas) * len(notas[0]))
print(f"A média da sala é: {media_sala:.2f}")

