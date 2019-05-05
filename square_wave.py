import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
f = 20
omgea = 2*pi*f
t = np.linspace(0,10,100)
fourier_coef = np.array([])
frequecy = np.array([])
sin = np.sin
cos = np.cos

y = sin(omgea*t)
y1 = sin(2*t)
y2 = cos(3*t)

wave = sin(omgea*t)
fourier_coef = np.append(fourier_coef,[4/pi])
frequecy = np.append(frequecy,f)
for n in range(3,10,2): #让设置步长，确保n为奇数
	harmonic_wave = (4/(n*pi))*sin(n*omgea*t)
	print(n)
	fourier_coef = np.append(fourier_coef,[4/(n*pi)])
	frequecy = np.append(frequecy,f*n)
	wave = wave+harmonic_wave

plt.figure("wave")
plt.plot(t,wave)
plt.figure("spectrum")
plt.stem(frequecy,fourier_coef)

plt.pause(0)

