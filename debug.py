import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def debug_plot(array, linewidth='0.5'):
    ''' plot the array, when debug in VSCode

    input:
        array - the numpy array to plot
        linewidth - the width of the line
    '''
    plt.figure()
    plt.plot(array, linewidth=linewidth)
