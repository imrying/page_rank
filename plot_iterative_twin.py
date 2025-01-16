import pandas as pd
import matplotlib.pyplot as plt

CSV_FILENAME_RECURSIVE = 'recursive.csv'
CSV_FILENAME_MATRIX = 'matrix.csv'

data_recursive = pd.read_csv(CSV_FILENAME_RECURSIVE, header=None, names=['Max Norm Difference'])
data_matrix = pd.read_csv(CSV_FILENAME_MATRIX, header=None, names=['Max Norm Difference'])

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = 'tab:blue'
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Max Norm Difference (Recursive)', color=color1)
ax1.plot(data_recursive.index, data_recursive['Max Norm Difference'], 
         marker='o', linestyle='-', color=color1, label='Recursive')
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:orange'
ax2.set_ylabel('Max Norm Difference (Iterative Matrix)', color=color2)
ax2.plot(data_matrix.index, data_matrix['Max Norm Difference'], 
         marker='s', linestyle='--', color=color2, label='Iterative Matrix')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('PageRank Convergence to 0.1% d=0.85\nCalculated on DTU HPC')

fig.legend(loc='upper right', bbox_to_anchor=(0.85, 0.85))

ax1.grid(True)

plt.show()

