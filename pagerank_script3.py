
from pagerank_script1 import *
from pagerank_script2 import *
import numpy as np
import math

def modified_link_matrix(web,pagelist,d=0.85):
    """ 
    Create a modified link matrix from web
    Input: web is a dictionary whose keys are contained in the list pagelist,
           pagelist is just a list of the keys (to give the keys and ordering)
           d is the damping factor
    Output: d*A^T+(1-d)*E/N
          where A is an NxN numpy array, for which
          row j has non-zero entries only in the columns corresponding 
          to pagelist to which page j links.  In a given row, all non-zero entries have the 
          same value, and these values sum to 1. Special case: if page j does not link
          to any page, then all entries in row j are given the same value (1/N).
          E is np.ones([N,N])
    """
    fix_zero_columns(web)
    N = len(web)
    # Create a N*N matrix with zeroes 
    A = np.zeros(shape=(N, N))

    for i, row in enumerate(A):
        outlinks = web[pagelist[i]]
        outlinks_len = len(outlinks)

        for j, elem in enumerate(row):
            if pagelist[j] in outlinks:
                A[i,j] = 1/outlinks_len 
    return (d * A.T) + (1-d)*np.ones(shape=(N, N))/N

def eigenvector_pagerank(web,d=0.85):
    """
    Returns the pagerank of web as the eigenvector of the modified link matrix
    Input: web is a dictionary of web pages and lines. 
           d is a positive float, the damping constant
    Output: A dictionary with the same keys as web, and the values the pageranks of the keys
    """
    ranking=dict()
    pages=list(web.keys())
    M=modified_link_matrix(web,pages,d)
    lambdas, V=np.linalg.eig(M)
    eigvector = []

    # Select the eigenvalue = 1
    for i, _lambda in enumerate(lambdas):
        # Since some of the eigenvalues can be complex we also check it
        if math.isclose(_lambda.real, 1.00) and math.isclose(_lambda.imag, 0.00): 
            eigvector = V[:,i]
            break
    else:
        raise Exception("ERROR: no eig value with 1 found")

    # normalize the vector
    eigvector = eigvector / sum(eigvector)

    # assign the ranking to each page
    for i, page in enumerate(web):
        ranking[page] = eigvector[i].real 

    return ranking

def matrix_pagerank(web,power,d=0.85):
    """
    Returns the pagerank as the first column of the power'th power of the modified link matrix

    Input: web is a dictionary of web pages and lines. 
           d is a positive float, the damping constant
    Output: A dictionary with the same keys as web, and the values the pageranks of the keys
    """
    ranking=dict()

    pages=list(web.keys())
    M=modified_link_matrix(web,pages, d)

    M_p = np.linalg.matrix_power(M, power)
    for i, page in enumerate(web):
        ranking[page] = M_p[:, 0][i] 
    return ranking

def matrix_pagerank_iterative(web, true_ranking, max_iterations, tolerance,timer,d=0.85):
    """
    Returns the pagerank as the first column of the power'th power of the modified link matrix

    Input: web is a dictionary of web pages and lines. 
           d is a positive float, the damping constant
    Output: A dictionary with the same keys as web, and the values the pageranks of the keys
    """
    ranking=dict()
    pages=list(web.keys())
    M=modified_link_matrix(web,pages, d)
    new_M = M

    def check_ranking(mat):
        for i, page in enumerate(web):
            ranking[page] = mat[:, 0][i] 

        for key in true_ranking:
            if key not in ranking:
                return False
            elif not (math.isclose(ranking[key], true_ranking[key], rel_tol = tolerance)):
                return False
        return True

    current_iterations = 0
    while True:
        timer.start()
        current_iterations+=1
        if current_iterations == max_iterations:
            raise Exception('not found')

        new_M = np.matmul(new_M, M)
        timer.stop()
        if check_ranking(new_M):
            return ranking

def matrix_pagerank_csv(web, true_ranking, max_iterations, tolerance,writer,d=0.85):
    """
    Returns the pagerank as the first column of the power'th power of the modified link matrix

    Input: web is a dictionary of web pages and lines. 
           d is a positive float, the damping constant
    Output: A dictionary with the same keys as web, and the values the pageranks of the keys
    """
    ranking=dict() #convert to dictionary

    pages=list(web.keys())
    M=modified_link_matrix(web,pages, d)
    new_M = M
    true_vec = get_vector(true_ranking)

    def check_ranking(mat):
        for i, page in enumerate(web):
            ranking[page] = mat[:, 0][i] 

        curr_rank = get_vector(ranking)
        max_matrix_norm = np.max(np.abs(true_vec - curr_rank))
        writer.writerow([str(max_matrix_norm)])

        for key in true_ranking:
            if key not in ranking:
                return False
            elif not (math.isclose(ranking[key], true_ranking[key], rel_tol = tolerance)):
                return False
        return True
    current_iterations = 0
    while True:
        current_iterations+=1
        if current_iterations == max_iterations:
            raise Exception('not found')

        new_M = np.matmul(new_M, M)
        if check_ranking(new_M):
            return ranking

# # test the function modified_link_matrix
web={1: {2}, 2: {3}, 3: {}}

M = modified_link_matrix(web, list(web.keys()), 1)
# print(M)

# ranking2, iterations = recursive_pagerank(web,0.00001, 200)
# random_surf_rank = random_surf(web, 100000)
# print(ranking2)
# print(eigenvector_pagerank(web))
# print(random_surf_rank)
# print("###")
# print(matrix_pagerank(web, 100))


# ranking = random_surf(web, 1000000)
# print(ranking)


# M=modified_link_matrix(web,pages)
# # print(M)


# #get the eigenvalues and eigenvectors:
# lamda, V=np.linalg.eig(M)
# print(np.round(lamda,3))
# V1=V[:,0:1]    # the eigenvalue method
# print(V1)
# # normalize the eigenvector so that it's components sum to 1
# V1=np.real(V1)
# ranking3=V1/(np.sum(V1))  # ranking from eigenvector 1

# #compute the 10th power:
# M10=np.linalg.matrix_power(M,100)
# ranking4=M10[:,0:1]  # the matrix power method

# ## compare the these with the recursive ranking
# print(ranking2)
# print(ranking3.T)
# print(ranking4.T)
# """
# Expected output:
# >>> print(ranking2)
# {0: 0.24624590505340951, 1: 0.14236766036275778, 2: 0.14236766036275778, 3: 0.14236714465910533, 4: 0.13310350804075904, 5: 0.19360998286898337}
# >>> print(ranking3.T)
# [[0.24622845 0.14235873 0.14235873 0.14235873 0.13309646 0.19359892]]
# >>> print(ranking4.T)
# [[0.24616676 0.14236384 0.14236384 0.14236384 0.13310638 0.19363533]]
# """



# # Test the functions matrix_pagerank and eigenvector_pagerank
# web={0: {4}, 1: {0, 4, 7}, 2: {0, 9, 5}, 3: set(), 4: {2}, 5: {1, 2, 3, 7}, \
#  6: {2, 5}, 7: {8, 5, 6}, 8: {9, 5, 1}, 9: {8, 1, 0}}
# ranking1 = random_surf(web, 100000)
# ranking2, iterations = recursive_pagerank(web,0.0000001)
# ranking3=eigenvector_pagerank(web)
# ranking4=matrix_pagerank(web,20)
# print_rank(ranking1)
# print(iterations)
# print_rank(ranking2)
# print_rank(ranking3)
# print_rank(ranking4)
# """
# Expected output:
# >>> print_rank(ranking1)
# 0:  0.1256,  1:  0.0907,  2:  0.1916,  3:  0.0471,  4:  0.1513,  5:  0.1285, 
#      6:  0.0386,  7:  0.0707,  8:  0.065,  9:  0.0909,  
# >>> print(iterations)
# 39
# >>> print_rank(ranking2)
# 0:  0.1247,  1:  0.0907,  2:  0.191,  3:  0.0463,  4:  0.1506,  5:  0.1286,  
#     6:  0.0393,  7:  0.072,  8:  0.0653,  9:  0.0915,  
# >>> print_rank(ranking3)
# 0:  0.1247,  1:  0.0907,  2:  0.191,  3:  0.0463,  4:  0.1506,  5:  0.1286,  
#     6:  0.0393,  7:  0.072,  8:  0.0653,  9:  0.0915,  
# >>> print_rank(ranking4)
# 0:  0.1247,  1:  0.0907,  2:  0.191,  3:  0.0463,  4:  0.1506,  5:  0.1286,
      # 6:  0.0393,  7:  0.072,  8:  0.0653,  9:  0.0915,  

#"""




