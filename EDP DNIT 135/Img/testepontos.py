# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import banco.bancodedados as bancodedados

l=[]
x=[]
y=[]
l=bancodedados.getpontos135(1)
for tupla in l:
    x.append(tupla[0])
    y.append(tupla[1])

# x = np.linspace(0, 2 * np.pi, 100)
# y = np.sin(x) + np.random.random(100) * 0.2
yhat = savgol_filter(y, 51, 9)

plt.plot(x, y)
plt.plot(x, yhat, color="green")
plt.grid()
plt.show()