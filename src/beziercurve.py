import matplotlib.pyplot as plt

class BezierCurve:
    def __init__(self):
        self.curve_points = []
        self.control_points = []

    def calculate_bezier_three_point(self, control_points, iterations):
        if len(control_points) == 3 and iterations == 1:
            # Basis case: jika ada tiga titik dan iterasi adalah 1, hitung midpoint tiga titik
            midpoint = self.midpoint_of_three(*control_points)
            return [midpoint]
        elif len(control_points) == 3 and iterations > 1:
            # Rekursi: jika ada tiga titik dan iterasi lebih dari 1
            midpoint_a = self.midpoint(control_points[0], control_points[1])
            midpoint_b = self.midpoint(control_points[1], control_points[2])
            
            for i in range(iterations):
                midpoint_of_three = self.midpoint_of_three(control_points[0], control_points[1], control_points[2])
                new_control_points1 = [control_points[0], midpoint_a, midpoint_of_three]
                new_control_points2 = [midpoint_of_three, midpoint_b, control_points[2]]
                curve_points1 = self.calculate_bezier_three_point(new_control_points1, iterations - 1)
                curve_points2 = self.calculate_bezier_three_point(new_control_points2, iterations - 1)
            return curve_points1+curve_points2
        else:
            return []
        

    def make_bezier(self, *control_points, iterations):
        self.curve_points.clear()
        self.control_points = list(control_points)

        iterations1 = self.midpoint_of_three(*control_points)
        self.curve_points.append(iterations1)
        print(self.curve_points)

        # Memulai rekursi untuk menghitung titik-titik kurva Bezier di iterasi yang lebih dari 1
        if iterations>1 :
            another_points_curve = self.calculate_bezier_three_point(control_points, iterations) 
            self.curve_points.extend(another_points_curve.copy())
        print(self.curve_points)

        
        # Hubungkan titik kontrol pertama dengan titik kurva pertama
        if len(self.curve_points) > 0:
            self.curve_points.insert(0, self.control_points[0])
        print(self.curve_points)
        
        # Hubungkan titik kontrol terakhir dengan titik kurva terakhir
        if len(self.curve_points) > 0:
            self.curve_points.append(self.control_points[-1])
        print(self.curve_points)
        self.curve_points=sorted(self.curve_points, key=lambda p: p[0])
        print(self.curve_points)


    def midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    def midpoint_of_three(self, a, b, c):
        # Menghitung midpoint dari tiga titik
        return self.midpoint(self.midpoint(a, b), self.midpoint(b, c))

    def plot_curve(self):
        # Plot titik kontrol
        plt.plot(*zip(*self.control_points), marker='o', color='red', label='Control Points')
        
        # Plot kurva Bezier
        plt.plot(*zip(*self.curve_points), linestyle='--', color='gray')
        plt.plot(*zip(*self.curve_points), marker='o', color='blue', label='Bezier Curve')
        
        plt.legend()
        plt.title('Bezier Curve')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()