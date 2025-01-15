
CSV_FILENAME = 'timecalc.csv'

HEADERS = ["nodes", "connections", "eig_vector", "random_surf", "recursive", "iterative_matrix"]

import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_lines(csv_filename):
    df = pd.read_csv(csv_filename)

    x = df['nodes']
    
    columns_to_plot = ['eig_vector', 'random_surf', 'recursive', "iterative_matrix"]

    plt.figure(figsize=(8, 5))
    
    for col in columns_to_plot:
        plt.plot(x, df[col], marker='o', label=col)

    plt.yscale("log")
    plt.xlabel('Nodes')
    plt.ylabel('Values')
    plt.title('Plot of CSV Data')

    plt.legend()

    plt.show()

if __name__ == '__main__':
    plot_csv_lines(CSV_FILENAME)





    
        

 
