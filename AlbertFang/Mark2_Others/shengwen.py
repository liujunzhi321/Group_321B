import matplotlib.pyplot as plt
import numpy as np

def shengwen():
    x_1 = np.arange(0, 5.001, 0.1)
    y_1 = 0*x_1 + 40
    
    x_2 = np.arange(5, 5+110/15+0.001, 0.1)
    y_2 = 15*x_2-35

    x_3 = np.arange(5+110/15, 5+110/15+13+0.001, 0.1)
    y_3 = 0*x_3 + 150

    x_4 = np.arange(5+110/15+13, 5+110/15+13+70/10+0.001, 0.1)
    y_4 = 10*x_4 - 103.333

    x_5 = np.arange(5+110/15+13+70/10, 5+110/15+13+70/10+10+0.001,0.1)
    y_5 = 0*x_5 + 220

    plt.plot(x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4, x_5, y_5, c='black')
    plt.xlabel('Time(min)')
    plt.ylabel('Temperature($^\circ$C)')
    fp_out = r'E:\WW\shengwen.png'
    plt.savefig(fname = fp_out,
        dpi = 300,
        bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    shengwen()