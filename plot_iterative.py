# import pandas as pd
# import matplotlib.pyplot as plt

# CSV_FILENAME = 'recursive.csv'
# data = pd.read_csv(CSV_FILENAME, header=None, names=['Max Norm Difference'])

# plt.figure(figsize=(10, 6))
# plt.plot(data.index, data['Max Norm Difference'], marker='o', linestyle='-', label='Convergence Data')
# plt.xlabel('Iterations')
# plt.ylabel('Max Norm Difference')
# plt.title('PageRank Convergence to 0.1% d=0.85\nCalculated on DTU HPC')
# plt.legend()
# plt.grid(True)

# plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# File names
CSV_FILENAME_RECURSIVE = 'recursive.csv'
CSV_FILENAME_MATRIX = 'matrix.csv'

data_recursive = pd.read_csv(CSV_FILENAME_RECURSIVE, header=None, names=['Max Norm Difference'])
data_matrix = pd.read_csv(CSV_FILENAME_MATRIX, header=None, names=['Max Norm Difference'])

plt.figure(figsize=(10, 6))

plt.plot(data_recursive.index, data_recursive['Max Norm Difference'], 
         marker='o', linestyle='-', label='Recursive')

plt.plot(data_matrix.index, data_matrix['Max Norm Difference'], 
         marker='s', linestyle='--', label='Iterative Matrix')

plt.xlabel('Iterations')
plt.ylabel('Max Norm Difference')
plt.title('PageRank Convergence to 0.1% d=0.5\nCalculated on DTU HPC')
plt.legend()
plt.grid(True)

plt.show()
