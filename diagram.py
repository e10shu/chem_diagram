import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class Group:
    def __init__(self, name, homo, lumo, color = ""):
        self.name = name
        self.homo = float(homo)
        self.lumo = float(lumo)
        self.color = color
        self.id = datetime.now().strftime("%f")


class Diagram:
    def __init__(self,x,y,groups):
        self.x = x
        self.y = y
        self.groups = groups

    def plot(self,path):
        labels = list(map(lambda g: g.name,self.groups))
        ticks = np.arange(0.5, len(labels)*2, 2)
        plt.xticks(ticks, labels)
        plt.xlabel(self.x)
        plt.ylabel(self.y)

        dup_labels = {}
        pre_index = 0
        for group in self.groups:
            index = pre_index
            if group.name in dup_labels:
                index = dup_labels[group.name]
            else:
                dup_labels[group.name] =  index

            x = [2*index, 2*(index+1) - 1]
            homo_y = [group.homo, group.homo]
            lumo_y = [group.lumo, group.lumo]

            plt.plot(x, homo_y, color=group.color)
            plt.plot(x, lumo_y, color=group.color)
            pre_index += 1

        plt.savefig(path)
        plt.close()
        #plt.show()

if __name__ == '__main__':
    d = Diagram("","",[])
    d.plot("")






