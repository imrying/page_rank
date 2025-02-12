
import numpy as np
import random
import math
##########################  Helper Functions ################
def make_web(n,k,kmin=0):
    """
    Creates a dictionary of n web pages, where each web page links to a random number
    (between kmin and k) of the web pages.
    Input: n and k are non-negative integers
    Output: web is a dictionary with n keys.  
    The value of each key is a list that is a subset of the keys
    """
    assert(k<n)
    keys=np.array(range(n))
    web=dict()
    for j in keys:
        numlinks=np.random.choice(range(kmin,k+1)) # the number of links that web[j] maps to
        web[j] = set(np.random.choice(keys[keys!=j],numlinks,replace=False)) #chose links from web-{j}
    return web

def surf_step(web, page, d=0.85):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    Input: -web is a dictionary of webpages and links
           - page is a key of the dictionary, the page from which to 
           compute the next step
           - d is the damping factor

    - If page does not link to any page, then choose any page in web at random
    - Otherwise:
          With probability `d`, choose a page at random linked to by `page`,  
          With probability `1 - d`, choose  a page at random  from all pages in the web.
    Otuput: is a dictionary with the same keys as web, and the 
            value for each key is the probability of choosing that page next.
            (The sum of all these should be 1)
    """

    def even_probability():
        distribution=dict() 
        prob = 1/len(web)
        for key in web:
            distribution[key] = prob
        return distribution

    def page_probability():
        distribution=dict() 
        prob = 1/len(web[page])
        for key in web:
            if key in web[page]:
                distribution[key] = prob
            else:
                distribution[key] = 0
        return distribution

    def dampen_probability():
        _even_probability = even_probability()
        _page_probability = page_probability()
        distribution=dict() # the distribution dictionary

        for key in _even_probability:
            distribution[key] = (_page_probability[key] * d) + (_even_probability[key] * ( 1 - d))  
        return distribution

        
    if len(web[page]) == 0:
        # if page p has no outlinks choose any page from W at random
        return even_probability()
    else:
        # else if f page p has outlinks, {q1, ..., qmp }, then, with probability d choose at random
        # one of the pages that page p links to, and with probability 1−d choose a
        # random page from the whole of W.
        return dampen_probability()
   

def random_surf(web,n,d=0.85):
    """
    Return PageRank values for each page by sampling `n` pages
    according to surf_step. 
    Input: web is a dictionary of webpages and links, 
           n is an integer, the number of steps in the simulation
           d is the damping factor, 
           
    Returns a dictionary with thes same keys as web (the pages), and
    the value for key k is the page rank of page k. The sum of all PageRank values 
    should be 1.
    """
    ranking=dict() # the ranking for each page
    sample = dict() # the samples we collect while running the simulation

    pages = list(web.keys())

    def add_sample(page_name):
        if page_name in sample:
            sample[page_name] += 1
        else:
            sample[page_name] = 1

    # adds the initial page we start the simulation from
    current_page = random.choice(pages) 
    add_sample(current_page)

    for i in range(0,n-1):
        new_page_probabilities = surf_step(web, current_page, d)
        # get a new page based on the page probabilities returned
        current_page = random.choices(list(new_page_probabilities.keys()), weights=new_page_probabilities.values(), k=1)[0]
        add_sample(current_page)

    for key in web:
        if key not in sample:
            ranking[key] = 0
        else:
            ranking[key] = sample[key]/n

    return ranking

def plot_ranking(web,ranking,d=0.85):
    """
    plots a graphical representation of the input web, indicating 
    hyperlinks with arrows, and visualizing the pagerank of each page
    by size.
    
    Input: web and ranking are dictionaries, as output by the functions
    "make_web" and "random_surf". Uses graphviz.
    """
    import graphviz
    # Create the initial dot object
    dot = graphviz.Digraph(comment='pageranking', node_attr={'shape': 'circle', 'fontsize': '10'}, edge_attr={'fontsize': '8'})

    # add a node for each key in web with its ranking
    for key in web:
        dot.node(str(key), label=f'{key}: {ranking[key]:.2f}')

    # create all edges and add the single probability from going from 
    # pag A to B
    for key in web:
        page_probality = surf_step(web, key, d)
        for value in web[key]:
            dot.edge(str(key), str(value), label=f'{round(page_probality[value]*100)}%')
            
    dot.render('file.gv', format='png',view=True)



################### Extra functions used for time and convergence data collection ###
def random_surf_with_thresholds(web,true_ranking, timer, max_iterations, tolerance, d=0.85):
    """
    Return PageRank and iteration values for each page by sampling `n` pages
    according to surf_step
    Input: web is a dictionary of webpages and links, 
           n is an integer, the number of steps in the simulation
           d is the damping factor, 
           
    Returns a dictionary with thes same keys as web (the pages), and
    the value for key k is the page rank of page k. The sum of all PageRank values 
    should be 1.
    """
    ranking=dict() # the ranking for each page
    sample = dict()

    pages = list(web.keys())
    current_page = random.choice(pages) 

    sample = dict()

    def add_sample(page_name):
        if page_name in sample:
            sample[page_name] +=1
        else:
            sample[page_name] = 1


    def create_ranking(current_iterations):
        for key in web:
            if key not in sample:
                ranking[key] = 0
            else:
                ranking[key] = sample[key]/current_iterations
    def check_sample():
        create_ranking(current_iterations)
        for key in true_ranking:
            if key not in ranking:
                return False
            elif not (math.isclose(ranking[key], true_ranking[key], rel_tol = tolerance)):
                # print(f'not close enough {ranking[key], true_ranking[key]}')
                return False
        return True

    add_sample(current_page)
    current_iterations = 1

    while True:
        if (current_iterations == max_iterations-1):
            print(ranking)
            raise Exception('never found stuff')

        timer.start()

        new_page_probabilities = surf_step(web, current_page, d)
        current_page = random.choices(list(new_page_probabilities.keys()), weights=new_page_probabilities.values(), k=1)[0]
        add_sample(current_page)
        timer.stop()

        if check_sample():
            return ranking
        current_iterations += 1

    return ranking, current_iterations



#########            Test code with this   #################3

###
# webwowo={1: {2}, 2: {3}, 3: {}}
# ranking = random_surf(webwowo, 100000, 0.5)
# print(ranking)
# plot_ranking(webwowo, ranking, 0.5)
####

# web1={0: {1, 3}, 1: {0}, 2: {0}, 3: {0}}
# ranking=random_surf(web1,100000)
# print(ranking)
# plot_ranking(web1, ranking, 0.85)
# """  
# Expected output approximately (varies due to random sample)
# {0: 0.47917, 1: 0.24081, 2: 0.03823, 3: 0.2418}
# """
# ranking=random_surf(web1,100000,0.5)  # try damping factor 0.5
# print(ranking)
# """
# Output:  {0: 0.41565, 1: 0.22766, 2: 0.12625, 3: 0.23045}
# """
# ranking=random_surf(web1,100000,0.98)  # try damping factor 0.98
# print(ranking)
# """
# Output: {0: 0.49746, 1: 0.25025, 2: 0.00481, 3: 0.24749}
# """

# web2={0: {9, 5}, 1: {0, 8, 4}, 2: set(), 3: set(), 4: {1}, 5: {0, 9, 2}, \
#         6: set(), 7: set(), 8: {6}, 9: {0, 1, 4}}
# ranking=random_surf(web2,500000)  
# plot_ranking(web2, ranking)
# print(ranking)
# """
# Output: {0: 0.14996, 1: 0.174538, 2: 0.063408, 3: 0.035674, 4: 0.12142, 5: 0.0997,
#          6: 0.107472, 7: 0.035816, 8: 0.084552, 9: 0.127462}  
# """

# web3=make_web(100,20)
# ranking=random_surf(web3,100000)
# print(ranking)
# """
# depends on the web that was randomly created by web 3, but should produce something!
# """
