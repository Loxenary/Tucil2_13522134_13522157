from beziercurve import BezierCurve

def main():
    bezier = BezierCurve()
    control_points = [(0,0), (2, 3), (5,1)]  
    iterations = 1 
    bezier.make_bezier(*control_points, iterations=iterations)
    bezier.plot_curve()

if __name__ == "__main__":
    main()
