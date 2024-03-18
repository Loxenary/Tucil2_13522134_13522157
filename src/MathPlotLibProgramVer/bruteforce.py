import numpy as np
import matplotlib.pyplot as plt
class BezierCurve:
    def __init__(self):
        self.curve_points = []
        self.control_points = []

    def make_bezier(self, *control_points, iterations):
        self.curve_points.clear()
        self.control_points = list(control_points)

        # Jumlah titik kontrol harus sama dengan tiga
        if len(control_points) != 3:
            print("Error: 3 control points required")
            return
        
        p0, p1, p2 = control_points
        
        # Menghitung jumlah titik berdasarkan iterasi
        N = 2**iterations + 1
        
        # Membuat basis nilai t awal
        t_base = np.linspace(0, 1, num=N)
        
        # Inisialisasi array nilai t
        t_values = np.zeros(N)
        
        # Memasukkan basis nilai t awal
        for i in range(len(t_base)):
            t_values[i] = t_base[i]
        for i in range(len(self.control_points) - 2):
            for t in t_values:
                #print(t)
                qx0 = (1 - t) * p0[0] + t * p1[0]
                qy0 = (1 - t) * p0[1] + t * p1[1]
                qx1 = (1 - t) * p1[0] + t * p2[0]
                qy1 = (1 - t) * p1[1] + t * p2[1]
                x_new = (1 - t) * qx0 + t * qx1
                y_new = (1 - t) * qy0 + t * qy1
                new_points = (x_new, y_new)
                if new_points not in self.curve_points:
                    self.curve_points.append(new_points)
        
        # Menambahkan titik terakhir
        if self.control_points[-1] not in self.curve_points:
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
