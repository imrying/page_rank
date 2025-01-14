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
        inbounddict = {}
        for _page in web:
            inbounddict[_page] = []
            for outpage in web:
                if _page in web[outpage]:
                    inbounddict[_page].append(outpage)
        return inbounddict

def fix_zero_columns(web):
    for fixpage in web:
        if len(web[fixpage]) == 0:
            newreferences = []
            for p in web:
                newreferences.append(p)
            web[fixpage] = set(newreferences)
    

###### Programming Task 2

def rank_update(web,pageranks,_page,inbounddic, d):
    ''''
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

        for inboundvector in inbounddic[page]:
            inboundsum += pageranks[inboundvector]/len(web[inboundvector])

        pagerank = (1-d)/len(web) + d*inboundsum
    
        increments.append(abs(pageranks[page] - pagerank))

        newpageranks[page] = pagerank
        

    for page in pageranks:
        pageranks[page] = newpageranks[page]
    
    return increments


def recursive_pagerank(web,true_ranking,tolerance,max_iterations,timer,d=0.85):

    def check_ranking():
        for key in true_ranking:
            if key not in pageranks:
                return False
            elif not (math.isclose(pageranks[key], true_ranking[key], rel_tol = tolerance)):
                # print(f'not close enough {ranking[key], true_ranking[key]}')
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



##########   test it with this code #####
# web={0: {1, 7}, 1: {3, 6}, 2: {0, 1, 3}, 3: set(), 4: set(), 5: {3, 4, 6}, 6: {0}, 7: {4, 6}}
# ranking1 = random_surf(web, 100000)
# ranking2, iterations = recursive_pagerank(web,0.00001)
# print_rank(ranking1,4)
# print_rank(ranking2,4)
# print(iterations)
