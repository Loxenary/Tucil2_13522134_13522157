import matplotlib.pyplot as plt
import numpy as np
import time

from bruteforce import BezierCurve

bezier = BezierCurve()
bezier.quadratic_brute_Force((0, 0), (2,3), (5, 1),iterations = 3)
bezier.plot_curve()


