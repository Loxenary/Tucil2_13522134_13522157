from beziercurve import BezierCurve

def main():
    bezier = BezierCurve()
    control_points = [(100,200), (200, 300), (500,100)]  
    iterations = 3
    bezier.make_bezier(*control_points, iterations=iterations)
    bezier.plot_curve()

if __name__ == "__main__":
    main()
