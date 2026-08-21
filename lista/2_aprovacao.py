# Notas do aluno
nota1 = 8.5
nota2 = 7.0
nota3 = 9.0

# Cálculo da média
media = (nota1 + nota2 + nota3) / 3

# Faltas do aluno
faltas = 9

# Verificação de aprovação
if media >= 6.0 and faltas <= 15:
    print(f"Aluno aprovado com média {media:.2f} e {faltas} faltas.")
else:
    print(f"Aluno reprovado com média {media:.2f} e {faltas} faltas.")