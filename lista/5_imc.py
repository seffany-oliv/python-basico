# Peso
peso = float(input("Digite o peso (kg): "))

# Altura
altura = float(input("Digite a altura (m): "))

# Cálculo do IMC
imc = peso / (altura ** 2)

print(f"Seu IMC é: {imc:.2f}")

# Classificação do IMC
if imc < 18.5:
    print("Classificação: Abaixo do peso")

elif imc < 25:
    print("Classificação: Peso normal")

elif imc < 30:
    print("Classificação: Sobrepeso")

elif imc < 35:
    print("Classificação: Obesidade")