from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

class DrawStat:
    def __init__(self, listgroup):
        self._listgroup = listgroup

    def draw(self):
        colors = ("red", "gold", "green", "blue", "purple", "black", "black", "black", "black", "black", "black")
        count = 0
        for ll in self._listgroup:
            self.drawone(ll, colors[count])
            count += 1

        plt.show()
        return

    def drawone(self, ll, color):
        ax = []
        ay = []
        count = 0
        ads = ll
        for a in ads:
            ax.append(count)
            ay.append(ads[count])
            count += 1

#        plt.scatter(ax, ay, color=color)
        plt.plot(ax, ay, color=color, linewidth=2)
        pass
