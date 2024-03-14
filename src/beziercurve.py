import matplotlib.pyplot as plt
import numpy as np

class BezierCurve:
    def __init__(self):
        self.curve_points = []
        self.control_points = []

    def make_bezier(self, *control_points, iterations):
        self.curve_points.clear()
        self.control_points = list(control_points)
        self.calculate_bezier(control_points, 0, iterations)

    def calculate_bezier(self, control_points, current_iteration, iterations):
        new_control_points = []
        if current_iteration < iterations:
            if current_iteration == 0:
                # Hitung midpoint antara P0 dan P1 (Q0)
                midpoint_Q0 = self.mid_point(control_points[0], control_points[1])
                self.curve_points.append(midpoint_Q0)
                # Hitung midpoint antara P1 dan P2 (Q1)
                midpoint_Q1 = self.mid_point(control_points[1], control_points[2])
                self.curve_points.append(midpoint_Q1)
                # Hitung midpoint antara Q0 dan Q1 (R0)
                midpoint_R0 = self.mid_point(midpoint_Q0, midpoint_Q1)
                self.curve_points.append(midpoint_R0)
                new_control_points = [control_points[0],midpoint_Q0, midpoint_R0,control_points[1],midpoint_Q1]  
            else:
                for _ in range(iterations - 1):  
                    new_points = [control_points[0]]  # Titik awal
                    # Iterasi untuk menambahkan midpoint dan titik kontrol berikutnya
                    for i in range(len(control_points) - 1):
                        # Hitung midpoint antara titik kontrol i dan i+1
                        midpoint = self.mid_point(control_points[i], control_points[i + 1])
                        new_points.extend([midpoint, control_points[i + 1]])  # Tambahkan midpoint dan titik kontrol berikutnya
                    control_points = new_points  # Update titik kontrol
                new_control_points.extend(control_points)
            current_iteration += 1
            self.calculate_bezier(new_control_points, current_iteration, iterations)



    def mid_point(self, control_point1, control_point2):
        return ((control_point1[0] + control_point2[0]) / 2, (control_point1[1] + control_point2[1]) / 2)

    def plot_curve(self):
        plt.plot(*zip(*self.control_points), marker='o', color='red', label='Control Points')
        plt.plot(*zip(*self.curve_points), linestyle='--', color='gray')
        plt.plot(*zip(*self.curve_points), marker='o', color='blue', label='Bezier Curve')
        plt.legend()
        plt.title('Bezier Curve')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()