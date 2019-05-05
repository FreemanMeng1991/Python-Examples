import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
f = 10
duty_cycle = 0.5
omgea = 2*pi*f
t = np.linspace(-1/f,1/f,100)
fourier_coef = np.array([])
frequecy = np.array([])
sin = np.sin
cos = np.cos

def sa(x):
	if x == 0:
		return 1
	else:
		return sin(x)/x

start = -5
end = 5
Fn = duty_cycle*sa(start*pi*duty_cycle)
wave = Fn*cos(start*pi*t)
fourier_coef = np.append(fourier_coef,[Fn])
frequecy = np.append(frequecy,start*f)
for n in range(start+1,end+1): #让设置步长，确保n为奇数
	Fn = duty_cycle*sa(n*pi*duty_cycle)
	harmonic_wave = Fn*cos(n*omgea*t)
	fourier_coef = np.append(fourier_coef,[Fn])
	frequecy = np.append(frequecy,f*n)
	wave = wave+harmonic_wave

plt.figure("wave")
plt.plot(t,wave)
plt.figure("spectrum")
plt.stem(frequecy,fourier_coef)

plt.pause(0)

