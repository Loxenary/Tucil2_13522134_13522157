import numpy as np
import matplotlib.pyplot as plt
class BezierCurve:
    def __init__(self):
        self.curve_points = []
        self.control_points = []

    def quadratic_brute_Force(self, *control_points, iterations):
        self.curve_points.clear()
        self.control_points = list(control_points)

        # Jumlah titik kontrol harus sama dengan tiga
        if len(control_points) != 3:
            print("Error: Exactly 3 control points required for quadratic Bezier curve.")
            return
        
        p0, p1, p2 = control_points
        
        # Evaluasi kurva Bezier dengan menggunakan iterasi sebagai jumlah titik
        t_values = np.linspace(0, 1, num=1+iterations*2)
        for i in range(len(self.control_points) - 2):
            for t in t_values:
                qx0 = (1 - t) * p0[0] + t * p1[0]
                qy0 = (1 - t) * p0[1] + t * p1[1]
                qx1 = (1 - t) * p1[0] + t * p2[0]
                qy1 = (1 - t) * p1[1] + t * p2[1]
                x_new = (1 - t) * qx0 + t * qx1
                y_new = (1 - t) * qy0 + t * qy1
                self.curve_points.append((x_new, y_new))

        # Tambahkan titik terakhir
        self.curve_points.append(self.control_points[-1])

    def plot_curve(self):
        # Plot titik kontrol
        plt.plot(*zip(*self.control_points), marker='o', color='red', label='Control Points')
        
        # Plot kurva Bezier
        plt.plot(*zip(*self.curve_points), linestyle='--', color='gray')
        plt.plot(*zip(*self.curve_points), marker='o', color='blue', label='Bezier Curve')
        
        plt.legend()
        plt.title('Quadratic Bezier Curve')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()
