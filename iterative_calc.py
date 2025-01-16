from pagerank_script1 import *
from pagerank_script2 import *
from pagerank_script3 import *

import csv



def run():

    web = make_web(100, 10)
    d = 0.85
    tolerance = 0.01
    max_iterations = 10**6

    true_ranking = eigenvector_pagerank(web,d)
    CSV_FILENAME = 'recursive.csv'
    file = open(CSV_FILENAME, 'w', newline='')
    writer = csv.writer(file)

    recursive_rating = convergence_recursive_pagerank(web, true_ranking,tolerance, max_iterations, writer, d) 

    file.close()

    MATRIX_FILENAME = 'matrix.csv'
    file = open(MATRIX_FILENAME, 'w', newline='')
    writer = csv.writer(file)

    matrix_pagerank_csv(web, true_ranking, max_iterations, tolerance, writer,d)
    file.close()

if __name__ == '__main__':
    run()


