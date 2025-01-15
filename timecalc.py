from pagerank_script1 import *
from pagerank_script2 import *
from pagerank_script3 import *

import time
import csv

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0.0

    def start(self):
        if self.start_time is None:              
            self.start_time = time.perf_counter()


    def stop(self):
        if self.start_time is not None:
            self.elapsed_time += time.perf_counter() - self.start_time
            self.start_time = None

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0.0

    def get_elapsed_time(self):
        if self.start_time is None:
            return self.elapsed_time
        else:
            return self.elapsed_time + (time.perf_counter() - self.start_time)


CSV_FILENAME = 'timecalc2.csv'

HEADERS = ["nodes", "connections", "eig_vector", "recursive", "iterative_matrix"]

def generate_time_calc(d, number_of_graphs):

    try:

        file = open(CSV_FILENAME, 'w', newline='')
        writer = csv.writer(file)
        writer.writerow(HEADERS)
        
        assert(number_of_graphs >= 10)

        CONNECTIONS = 10
        MAX_ITERATIONS = 10**7
        TOLERANCE = 0.01
    
        for i in range(CONNECTIONS, number_of_graphs):
            print(f'calculating for graph with {i} nodes and {CONNECTIONS-1}')
            # generate the web
            web = make_web(i,CONNECTIONS-1)

            timer = Timer()

            timer.start()
            true_ranking = eigenvector_pagerank(web, d)
        
            timer.stop()
            print(true_ranking)

            eig_time = timer.get_elapsed_time()
            timer.reset()


            timer.start()
            recursive_rating = recursive_pagerank(web, true_ranking, TOLERANCE, MAX_ITERATIONS, timer, d) 
            timer.stop()
            recursive_time = timer.get_elapsed_time()
            timer.reset()
            print(recursive_rating)


            timer.start()
            matrix_iterative_power = matrix_pagerank_iterative(web, true_ranking, MAX_ITERATIONS, TOLERANCE, timer,d)
            timer.stop()
            matrix_iterative_time = timer.get_elapsed_time()
            print(matrix_iterative_power)

            writer.writerow([i, CONNECTIONS-1, eig_time, recursive_time, matrix_iterative_time])
    finally:
        file.close()
    
if __name__ == '__main__':
    generate_time_calc(0.85, 1000)
   




# timer.start()
# sample_rating = random_surf_with_thresholds(web,true_ranking, timer, MAX_ITERATIONS, TOLERANCE, d)
# timer.stop()
# sample_time = timer.get_elapsed_time()
# timer.reset()
# print(sample_rating)
