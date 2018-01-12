import random

dado1 = random.randint(1,6)
dado2 = random.randint(1,6)

print("Primer dado:",dado1)
print("Segundo dado:",dado2)

total = dado1 + dado2

if total == 7: 
	print("Gano")
else:
	print("Perdio")
