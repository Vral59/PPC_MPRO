import pandas as pd
import matplotlib.pyplot as plt
import os
import random
directory = './src/results/saved_files'

files = os.listdir(directory)
for file in files:

    df = pd.read_csv(directory + '/' + file)
    linestyles = ['-', '--', '-.', ':', '-.']
    linestyle_tuple = [
     ('dotted',                (0, (1, 1))),
     ('densely dotted',        (0, (1, 1))),
     ('long dash with offset', (5, (10, 3))),
     ('loosely dashed',        (0, (5, 10))),
     ('dashed',                (0, (5, 5))),
     ('densely dashed',        (0, (5, 1))),

     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),

     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]
    l = random.choice(linestyle_tuple)[1]
    plt.plot(df['total_time'], df['n'], linestyle= l, label = file[:-4])

plt.ylabel('n')
plt.title("Nombre d'instances résolues en fonction du temps total")

# Show the plot
plt.grid()
plt.legend()
plt.show()