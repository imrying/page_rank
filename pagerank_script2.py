"""
 Create a script called "pagerank_library.py" and put the functions created in this 
 project there
 """
import math

from pagerank_script1 import make_web, random_surf 
import numpy as np

def print_rank(ranking,k=4,title=""):
    """
    Print the ranking in tidy form with k decimal place
    """
    keys=ranking.keys()
    if len(title)>0:
        print(title, end=": ")
    for p in keys:
        print(str(p)+":  "+str(round(ranking[p],k)), end=",  ")
    print("\n")
    return



def generateinbounddictionary(web):
    '''
    generates a dictonary like web, but instead of outgoing
    links it has its ingoing links
    '''
    inbounddict = {}
    for _page in web:
        inbounddict[_page] = []
        for outpage in web:
            if _page in web[outpage]:
                inbounddict[_page].append(outpage)
    return inbounddict

def fix_zero_columns(web):
    '''
    If the page is a sink and has zero outlinks, we update the
    web st. it references all pages.
    '''
    for fixpage in web:
        if len(web[fixpage]) == 0:
            newreferences = []
            for p in web:
                newreferences.append(p)
            web[fixpage] = set(newreferences)

    
def rank_update(web,pageranks,_page,inbounddic, d):
    '''
    Updates the value of the pagerank for page based on the formula
        PR(p)= (1-d)/N + d*sum_j (PR(q)/OB(q))
    where the sum is over all pages q that link to page, PR(q) is the current
    pagerank of page q (from "pageranks") and OB(q) is the number of pages 
    outbound from page q.  Sinks are treated as linking to all pages in web.

    Input: web and pageranks are dictionaries as in the output of "make_web" and
     "random_surf", page is the key to the page whose rank we wish to update, 
         and d is the damping factor.
    Output: The (mutable) dictionary "pageranks" is updated according to the above formula,
            and this function returns a float "increment", the (absolute) difference 
            between the previous value and the updated value of PR(p).

    '''
    fix_zero_columns(web)
    
    newpageranks = {}
    increments = []
    for page in web:
        inboundsum = 0

        # go through the indbound to the page and calculate the indbound sum of probabilities.
        for inboundvector in inbounddic[page]:
            inboundsum += pageranks[inboundvector]/len(web[inboundvector])

        # calculate the pagerank from formula 2.2
        pagerank = (1-d)/len(web) + d*inboundsum
        increments.append(abs(pageranks[page] - pagerank))

        newpageranks[page] = pagerank

    for page in pageranks:
        pageranks[page] = newpageranks[page]
    
    return increments


def recursive_pagerank(web,stopvalue,max_iterations=10000,d=0.85):
    """
    Implements the recursive version of the PageRank algorithm by first creating a
    pagerank of 1/N to all pages (where N is the total number of pages)
    then applying "rank_update" repeteadly until either of two stopping conditions is
    reached:
    stopping condition 1: the maximum change from step n to step (n+1) over all pageranks 
    is less than stopvalue, 
    Stopping condition 2: the number of iterations has reached "max_iterations"
    Input: web is a dictionary as in the output of "make_web", d is the damping constant,
    stop value is a positive float, max_iterations is a positive integer
    """
    #initialize pageranks to 1/N
    pageranks=dict()
    for key in web:
        pageranks[key] = 1/len(web)

    inbounddic = generateinbounddictionary(web)

    for iteration in range(max_iterations):
        increments = rank_update(web, pageranks, "page", inbounddic, d)
        # if all the increments are smaller than our stopvalue we break and return
        if all(x < stopvalue for x in increments):
            break
    return pageranks, iteration


def recursive_pagerank_timed(web,true_ranking,tolerance,max_iterations,timer,d=0.85):
    ''' Timed version of recursive pagerank'''

    def check_ranking():
        for key in true_ranking:
            if key not in pageranks:
                return False
            elif not (math.isclose(pageranks[key], true_ranking[key], rel_tol = tolerance)):
                return False
        return True

    #initialize pageranks to 1/N
    pageranks=dict()
    for key in web:
        pageranks[key] = 1/len(web)

    inbounddic = generateinbounddictionary(web)

    for iteration in range(max_iterations):
        increments = rank_update(web, pageranks, "page",inbounddic, d)
        timer.stop()
        if check_ranking():
            break
        timer.start()
    else:
        raise Exception('did not find anything')

    return pageranks, iteration


def get_vector(pageranking):
    ''' creates a vector from the ranking '''
    mat = np.empty((0, 1))  
    for key in pageranking:
        mat = np.vstack([mat, [[pageranking[key]]]]) 
    return mat    

def convergence_recursive_pagerank(web,true_ranking,tolerance,max_iterations,writer, d=0.85):
    true_vec = get_vector(true_ranking)

    pageranks=dict()
    def check_ranking():
        curr_rank = get_vector(pageranks)

        max_matrix_norm = np.max(np.abs(true_vec - curr_rank))
        writer.writerow([max_matrix_norm])
        # add the data first
        
        for key in true_ranking:
            if key not in pageranks:
                return False
            elif not (math.isclose(pageranks[key], true_ranking[key], rel_tol = tolerance)):
                # print(f'not close enough {ranking[key], true_ranking[key]}')
                return False
        return True

    #initialize pageranks to 1/N
    for key in web:
        pageranks[key] = 1/len(web)

    inbounddic = generateinbounddictionary(web)

    for iteration in range(max_iterations):
        increments = rank_update(web, pageranks, "page",inbounddic, d)
        if check_ranking():
            break
    else:
        raise Exception('did not find anything')

    return pageranks, iteration


