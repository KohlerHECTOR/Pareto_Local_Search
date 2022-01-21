from gurobipy import *
import numpy as np

def main_(X):
	P = []
	F_P = []
	while True:
		x, y, valeur, w, z = CSS(X,P)
		
		assert z != "", "Aucune preference n'a été donnée"
		
		if z=='x':
			P.append((list(x),list(y)))
			F_P.append(w)
		else:
			P.append((list(y),list(x)))
			F_P.append(w)
			
		if valeur <= 0:
			break
			
		print("P update : ", P, "\n")
	
	print("Set of preference P : ", P)
	print("Set of agregation function F_P : ", F_P, "\n")
	return P[-1][0], F_P[-1]

def CSS(X,P):

	x, y, valeur, w = MMR(X,P)
	print("valeur PL : ", valeur, " vector w : ", w)
	print("x : ", x, " y : ", y)
	z = input("x or y ?")
	
	return x, y, valeur, w, z
	
def MMR(X,P):

	min_ = 10e5
	x_ = 0
	y_ = 0
	w_ = []
	
	for x in X :
		y, valeur, w = MR(x, X, P)

		if valeur < min_ :
			min_ = valeur 
			x_ = x
			y_ = y
			w_ = w

	return x_, y_, min_, w_

def MR(x, X, P):

	max_ = -10e5
	y_ = 0
	w_ = []

	for y in X:
		if not np.array_equal(x,y):
			valeur, w = PMR_owa(x,y,P)

			if max_ < valeur :
				max_ = valeur
				y_ = y
				w_ = w

	return y_, max_, w_

def PMR_owa(x,y,P):

	x_rearr = np.sort(x)
	y_rearr = np.sort(y)

	return PMR_ws(x_rearr,y_rearr,P)
	
#Implementation de PMR par Programme Linéaire
def PMR_ws(x,y,P):
	
	nbvar = len(x)
	columns = np.arange(nbvar, dtype=int)
	
	#create model
	m = Model("PMR")
	#aucun affichage de l'optimisation
	m.Params.LogToConsole = 0

	#decision variables declaration
	w = []
	for i in columns:
		w.append(m.addVar(vtype=GRB.CONTINUOUS, name="w%d" %(i+1)))
		
	#integration of new variable
	m.update()
	
	#objective function
	w = np.array(w)
	obj = (w @ y - w @ x)
	
	m.setObjective(obj, GRB.MAXIMIZE)

	#constraints
	for i in columns[:-1]:
		m.addConstr(w[i], GRB.GREATER_EQUAL, 0, "Constraint 1_%d" % (i+1))
		m.addConstr(w[i], GRB.GREATER_EQUAL, w[i+1], "Constraint 2_%d" % (i+1))
	m.addConstr(w[nbvar-1], GRB.GREATER_EQUAL, 0, "Constraint 1_%d"%(nbvar+1))
	
	m.addConstr(sum(w), GRB.EQUAL, 1, "Constraint 3")
	
	for (a,b) in P:

		a_rearr = np.sort(a)
		b_rearr = np.sort(b)
		m.addConstr(w @ a_rearr, GRB.GREATER_EQUAL, w @ b_rearr)
		
	# Resolution
	m.optimize()
	"""
	print("")
	print('Solution optimale:')
	for i in columns:
		print('w%d'%(i+1), '=', w[i].x)
	print("")
	print('Valeur de la fonction objectif :', m.objVal)
	"""

	return round(m.getObjective().getValue(),3), [round(w[i].x, 3) for i in columns]
	
if __name__ == '__main__':
	#X = np.array([[7329.0, 6088.0, 7854.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7571.0, 5758.0, 7250.0], [7243.0, 6486.0, 7912.0], [7329.0, 6088.0, 7854.0], [6543.0, 5712.0, 8155.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [6543.0, 5712.0, 8155.0], [7243.0, 6486.0, 7912.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [7521.0, 5236.0, 7486.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [6543.0, 5712.0, 8155.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7571.0, 5758.0, 7250.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7243.0, 6486.0, 7912.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [7521.0, 5236.0, 7486.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7571.0, 5758.0, 7250.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [6543.0, 5712.0, 8155.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7571.0, 5758.0, 7250.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [7569.0, 5984.0, 7115.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [6543.0, 5712.0, 8155.0], [7243.0, 6486.0, 7912.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [7521.0, 5236.0, 7486.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7571.0, 5758.0, 7250.0], [7243.0, 6486.0, 7912.0], [7329.0, 6088.0, 7854.0], [7571.0, 5758.0, 7250.0], [7521.0, 5236.0, 7486.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7571.0, 5758.0, 7250.0], [7243.0, 6486.0, 7912.0], [7569.0, 5984.0, 7115.0], [7329.0, 6088.0, 7854.0], [6629.0, 5314.0, 8097.0], [7243.0, 6486.0, 7912.0]])
	X = np.array([[6855.0, 6406.0], [7567.0, 5972.0], [6261.0, 6688.0], [7447.0, 5986.0], [6855.0, 6406.0], [7440.0, 6348.0], [6855.0, 6406.0], [7567.0, 5972.0], [6855.0, 6406.0], [7447.0, 5986.0], [7992.0, 5343.0], [7440.0, 6348.0], [7985.0, 5705.0], [7992.0, 5343.0], [7985.0, 5705.0], [7567.0, 5972.0], [6855.0, 6406.0], [6555.0, 6419.0], [7440.0, 6348.0], [7865.0, 5719.0], [7567.0, 5972.0], [7992.0, 5343.0], [7440.0, 6348.0], [7865.0, 5719.0], [7992.0, 5343.0], [7447.0, 5986.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [7865.0, 5719.0], [7985.0, 5705.0], [7440.0, 6348.0], [7440.0, 6348.0], [7447.0, 5986.0], [7992.0, 5343.0], [7440.0, 6348.0], [7985.0, 5705.0], [7440.0, 6348.0], [7992.0, 5343.0], [7985.0, 5705.0], [7567.0, 5972.0], [7440.0, 6348.0], [7865.0, 5719.0], [7567.0, 5972.0], [7992.0, 5343.0], [8266.0, 5036.0], [7985.0, 5705.0], [7865.0, 5719.0], [7567.0, 5972.0], [7447.0, 5986.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [8266.0, 5036.0], [7992.0, 5343.0], [7865.0, 5719.0], [7567.0, 5972.0], [7440.0, 6348.0], [8266.0, 5036.0], [7985.0, 5705.0], [7865.0, 5719.0], [7567.0, 5972.0], [7447.0, 5986.0], [7992.0, 5343.0], [8345.0, 4444.0], [8266.0, 5036.0], [8266.0, 5036.0], [7992.0, 5343.0], [7865.0, 5719.0], [7567.0, 5972.0], [7440.0, 6348.0], [7985.0, 5705.0], [8266.0, 5036.0], [7447.0, 5986.0], [7992.0, 5343.0], [7440.0, 6348.0], [7985.0, 5705.0], [7440.0, 6348.0], [6261.0, 6688.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [8266.0, 5036.0], [7985.0, 5705.0], [7992.0, 5343.0], [7440.0, 6348.0], [7447.0, 5986.0], [7447.0, 5986.0], [7992.0, 5343.0], [7440.0, 6348.0], [7985.0, 5705.0], [8266.0, 5036.0], [7985.0, 5705.0], [7865.0, 5719.0], [7567.0, 5972.0], [7447.0, 5986.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [8266.0, 5036.0], [7985.0, 5705.0], [7992.0, 5343.0], [7440.0, 6348.0], [7447.0, 5986.0], [7865.0, 5719.0], [8345.0, 4444.0], [8266.0, 5036.0], [8266.0, 5036.0], [7985.0, 5705.0], [8079.0, 5303.0], [7865.0, 5719.0], [7567.0, 5972.0], [7447.0, 5986.0], [7992.0, 5343.0], [8266.0, 5036.0], [7440.0, 6348.0], [7865.0, 5719.0], [7567.0, 5972.0], [7992.0, 5343.0], [7440.0, 6348.0], [7440.0, 6348.0], [7865.0, 5719.0], [7567.0, 5972.0], [7992.0, 5343.0], [8266.0, 5036.0], [7985.0, 5705.0], [7992.0, 5343.0], [7440.0, 6348.0], [7447.0, 5986.0], [7447.0, 5986.0], [7992.0, 5343.0], [7440.0, 6348.0], [7985.0, 5705.0], [8266.0, 5036.0], [7992.0, 5343.0], [7865.0, 5719.0], [7567.0, 5972.0], [7440.0, 6348.0], [8266.0, 5036.0], [7985.0, 5705.0], [8079.0, 5303.0], [7992.0, 5343.0], [7440.0, 6348.0], [7447.0, 5986.0], [7865.0, 5719.0], [8266.0, 5036.0], [8266.0, 5036.0], [7992.0, 5343.0], [7865.0, 5719.0], [7567.0, 5972.0], [7440.0, 6348.0], [7985.0, 5705.0], [8266.0, 5036.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [7440.0, 6348.0], [7865.0, 5719.0], [7567.0, 5972.0], [7992.0, 5343.0], [8266.0, 5036.0], [7985.0, 5705.0], [7865.0, 5719.0], [7567.0, 5972.0], [7447.0, 5986.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [8079.0, 5303.0], [8266.0, 5036.0], [7992.0, 5343.0], [7865.0, 5719.0], [7567.0, 5972.0], [7440.0, 6348.0], [6855.0, 6406.0], [7447.0, 5986.0], [7865.0, 5719.0], [7567.0, 5972.0], [7985.0, 5705.0], [8266.0, 5036.0], [7985.0, 5705.0], [7865.0, 5719.0], [7567.0, 5972.0], [7447.0, 5986.0], [7992.0, 5343.0], [8266.0, 5036.0], [8266.0, 5036.0], [7992.0, 5343.0], [7865.0, 5719.0], [7567.0, 5972.0], [7440.0, 6348.0], [7985.0, 5705.0], [8266.0, 5036.0], [8345.0, 4444.0], [7447.0, 5986.0], [7992.0, 5343.0], [7440.0, 6348.0], [7985.0, 5705.0]])
	sol_opti, w = main_(X)
	print("Best solution for DM : ", sol_opti, " weighted vector : ", w)
	
	
	
	
	
	
	
	
	
	
	
	
