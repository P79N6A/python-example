import matplotlib.pyplot as plt
import numpy as np

'''
n = 3

for color in ['red', 'blue', 'green']:
    x, y = np.random.rand(2, n)
    print x
    print '===='
    print y
    scale = 100 * np.random.rand(n)
    plt.scatter(x, y, c=color, s=scale, label=color, alpha=0.6, edgecolors='white')

plt.title('Scatter')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
'''

x = np.arange(0, 5, 0.1);
y = np.sin(x)
plt.plot(x, y)


