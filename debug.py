import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def debug_plot(array):
    plt.figure()
    plt.plot(array, linewidth='0.5')
