import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('./src/results/_smallest_domain_smallest.csv')
df2 = pd.read_csv('./src/results/MAC3_smallest_domain_smallest.csv')

plt.plot(df1['total_time'], df1['n'], linestyle='-', color='blue', label= 'sans MAC3')
plt.plot(df2['total_time'], df2['n'], linestyle='-', color='red', label = 'avec MAC3')
plt.xlabel('Total Time')
plt.ylabel('n')
plt.title('n vs Total Time')

# Show the plot
plt.grid()
plt.legend()
plt.show()