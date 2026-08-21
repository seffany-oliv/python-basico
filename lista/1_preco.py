# Preço do produto
preco = 50.50

# Quantidade de produtos
quantidade = 3

# Cálculo do valor total
valor_total = preco * quantidade

print(f"Valor total sem desconto: R${valor_total:.2f}")


# Calcular desconto de 10% se o valor for maior ou igual a 200
if valor_total >= 200:
    desconto = valor_total * 0.10
    valor_total -= desconto
    print(f"Desconto aplicado: R${desconto:.2f}")
    print(f"Valor final: R${valor_total:.2f}")
