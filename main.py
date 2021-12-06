from utils import read_instance, init_population, voisinage, init_population_S_weighted
from indicateurs import indicateur_P
import matplotlib.pyplot as plt
import numpy as np
from pls import PLS, PLS2

instance = read_instance("data/100_items/2KP100-TA-0")

initial_pop = init_population(instance["objects"], instance["max_weight"])
initial_pop_S = init_population_S_weighted(instance["objects"], instance["max_weight"], S = 10)

pls1 = PLS(voisinage, initial_pop, instance, iter_max = 15)
pls2 = PLS2(voisinage, initial_pop, instance)
pls3 = PLS2(voisinage, initial_pop_S, instance)

print("------------------- PLS 1 --------------------")
pls1.algorithm1()
# print("------------------- PLS 2 --------------------")
# pls2.algorithm1()
# print("------------------- PLS 3 --------------------")
# pls3.algorithm1()

sol_eff_pls1 = pls1.Xe
res_pls1 = np.array([pls1.get_sol_objective_values(s) for s in sol_eff_pls1])



plt.scatter(instance["sols_pareto"][:,0], instance["sols_pareto"][:,1], label = "Pareto Exact")
plt.scatter(res_pls1[:,0], res_pls1[:,1], label = "PLS1")
plt.legend()
# plt.scatter(res_pls2[:,0], res_pls2[:,1], label = "PLS2")
# plt.scatter(res_pls3[:,0], res_pls3[:,1], label = "PLS3")
plt.show()
