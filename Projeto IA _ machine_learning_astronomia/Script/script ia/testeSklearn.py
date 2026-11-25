import matplotlib.pyplot as plt
import pandas as p

df = p.read_csv("Estrelas_BuracosNegros_Quasares_DataSetF.csv")
#print(df.head())
print(df[['Name','Spectral Class','log_g']])



x = [10,12,12,15,15]
#x.append(175)
y = [2, 4, 6, 8, 10]

plt.plot(x, y, marker="o")
plt.title("Exemplo de Gráfico de Linha")
plt.xlabel("Eixo X")
plt.ylabel("Eixo Y")
plt.grid(True)
plt.show()