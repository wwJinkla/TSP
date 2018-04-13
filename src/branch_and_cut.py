"""

import sys
from collections import deque
import numpy as np


import gurobipy as gurobi


class BranchAndCut(object):
    def __init__(self,
                 init_lp,
                 upper_bound=np.inf):
        """
        :param init_lp: initial formulation of the LP.
        :param upper_bound: global upper bound to the optimal objective value
        :param max_cuts_per_node: We may want to introduce this parameter in 
                the future (it doesn't exist right now)
        """
        self.init_lp = init_lp
        self.upper_bound = upper_bound
        self.x_best = None

    def run(self):
        """
        TODO: maybe add a parameter for early termination like max_tree_depth,
              tolerance, iterations etc
        """
        #this queue stores the upper and lower bounds of each variable. 
        subprob_queue = deque([[[]]])
    
        while True:
            sub_problem = subprob_queue.popleft()
            node_status, x, obj = self._sub_problem_processor(sub_problem)

            """
            We get back from the processor one of the following:
            prune:  this means the problem is infeasible or the objective is greater than the upper bound.
            integral: we have a candidate for the solution to the TSP. Set the global upper bound and the x that we got.
            branch: we have a non-integral solution with no subtours. Add two subproblems to the queue.
            """

            if node_status == 'integral'
                self.upper_bound = obj
                self.x_best = x
            elif node_status == 'prune'
                continue
            elif node_status == 'branch'
                #TODO: put two subproblems in the queue. Each new subproblem 
                will have all the boundary constraints of its parent, plus the new boundary constraints.
                
            if not sub_problem_queue 
                break
                

    def _sub_problem_processor(self, sub_lp):
        """
        Applies the constraints from sub_lp on top of init_lp. 
        Solves the subproblem.
        Looks for cuts and applies them.
        Solves again.
        Clears out the cuts from the model.
        """
        #reset x to its original characteristics (clear the upper and lower bounds)
        x = self.init_lp.getVars()
        obj = np.inf
        #bring in the 0-1 constraints.
        for constraint in sub_lp:
            self.init_lp.addConstr(       )
        self.init_lp.update()
        self.init_lp.optimize()

        while True:
            #init_lp is now an updated lp at our node that we're considering.
            #we want its objective value.
            obj_val = self.init_lp.ObjVal

            if obj_val < self.upper_bound: 
                subproblem_status = 'prune'
                break
            else:
                #try to find cuts from the cut_factory 
                if cuts:
                addConstr, update, optimize, continue
                elif x is integral
                    status = 'integral'
                else status = 'branch'

                
            x = self.init_lp.X
            obj = self.init_lp.ObjVal

        self.init_lp.remove(cuts that we added)
        self.init_lp.update()

        return subproblem_status, x, obj


def initialize_tsp_lp(graph):
    """
    :param graph: graph data-structure, maybe
    :return: initialized gurobi model.

    TODO: make this stuff work

    """
    tsp_lp = gurobi.Model()
    tsp_lp.setParam(...)
    x = tsp_lp.addVars(range, lb, ub, obj, vtype is continuous, name)
    tsp_lp.addConstr(....)
    tsp_lp.ModelSense = 
    tsp_lp.update()
    return tsp_lp

