import numpy as np
from .equation import Equation

def find_equation_ids(preds):
    equation_label = 12
    equation_ids = np.where(preds[:, 0] == equation_label)[0]
    return equation_ids

def get_equations(prediction, equations_id):
    results = []
    for idx in equations_id:
        results.append(Equation(idx, prediction))
    return results