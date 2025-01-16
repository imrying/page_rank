
from pagerank_script3 import *
from pagerank_script1 import *


d=0.85
web = make_web(15, 2)
true_ranking = eigenvector_pagerank(web,d)


plot_ranking(web, true_ranking, d)
