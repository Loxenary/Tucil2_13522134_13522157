from beziercurve import BezierCurve

def main():
    bezier = BezierCurve()
    control_points = [(0.5,0), (2, 3), (5,1), (8,9)]  
    iterations = 3
    bezier.make_bezier(*control_points, iterations=iterations)
    bezier.plot_curve()

if __name__ == "__main__":
    main()
