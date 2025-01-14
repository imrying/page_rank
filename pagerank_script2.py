"""
 Create a script called "pagerank_library.py" and put the functions created in this 
 project there
 """

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

#TODO jeg kan ikke lide at vi opdatere værdien af en page af gangen, vil gerne gøre det i et hug
def rank_update(web,pageranks,_page,d):
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
    
    #vil gerne opdatere en enkelt rangen af en enkelt: page, og bruger formlen samt den initiele definition: pageranks
    inbounddic = generateinbounddictionary(web)
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

#
#myweb = {1:{2},2:{3},3:{}}
#mypageranks = {1:1/3,2:1/3,3:1/3}

#print(rank_update(myweb, mypageranks, 2, 0.5))
#print(mypageranks)


def recursive_pagerank(web,stopvalue,max_iterations=200,d=0.85):
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


    for iteration in range(max_iterations):
        increments = []
        increments = rank_update(web, pageranks, "page", d)
        if all(x < stopvalue for x in increments):
            break
    return pageranks, iteration



# ##########   test it with this code #####
# web={0: {1, 7}, 1: {3, 6}, 2: {0, 1, 3}, 3: set(), 4: set(), 5: {3, 4, 6}, 6: {0}, 7: {4, 6}}
# ranking1 = random_surf(web, 100000)
# ranking2, iterations = recursive_pagerank(web,0.00001)
# print_rank(ranking1,4)
# print_rank(ranking2,4)
# print(iterations)
