
CSV_FILENAME = 'timecalc2.csv'

HEADERS = ["nodes", "connections", "eig_vector", "recursive", "iterative_matrix"]

import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_lines(csv_filename):
    df = pd.read_csv(csv_filename)

    x = df['nodes']
    
    columns_to_plot = ['eig_vector', 'recursive', "iterative_matrix"]

    plt.figure(figsize=(8, 5))
    
    for col in columns_to_plot:
        plt.plot(x, df[col], marker='o', label=col)

    plt.yscale("log")
    plt.xlabel('Number of pages with 10 connections')
    plt.ylabel('Time in seconds (log10)')
    plt.title('Calculating pagerank to 1% error margin (d=0.85). Calculated on DTU HPC')

    plt.legend()

    plt.show()

if __name__ == '__main__':
    plot_csv_lines(CSV_FILENAME)





    
        

 
