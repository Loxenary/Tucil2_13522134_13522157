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
        

    def make_bezier_three_point(self, *control_points, iterations):
        curve_points = []

        iterations1 = self.midpoint_of_three(*control_points)
        curve_points.append(iterations1)

        # Memulai rekursi untuk menghitung titik-titik kurva Bezier di iterasi yang lebih dari 1
        if iterations > 1:
            another_points_curve = self.calculate_bezier_three_point(control_points, iterations) 
            curve_points.extend(another_points_curve)

        # Hubungkan titik kontrol pertama dengan titik kurva pertama
        if len(curve_points) > 0:
            curve_points.insert(0, control_points[0])
            
        # Hubungkan titik kontrol terakhir dengan titik kurva terakhir
        if len(curve_points) > 0:
            curve_points.append(control_points[-1])

        # Urutkan titik-titik kurva berdasarkan nilai x
        curve_points = sorted(curve_points, key=lambda p: p[0])

        return curve_points

    def make_bezier(self, *control_points, iterations):
        #print(len(control_points))
        self.control_points = list(control_points)
        # Jumlah titik kontrol harus minimal 3
        if len(control_points) < 3:
            print("Error: Minimum 3 control points required.")
            return

        # Jika jumlah titik kontrol sama dengan 3, gunakan make_bezier_three_point
        elif len(control_points) == 3:
            self.curve_points = self.make_bezier_three_point(*control_points, iterations=iterations)
            return

        else:
            # Bagi control points menjadi segmen-segmen berukuran 3
            segments = [control_points[i:i+3] for i in range(0, len(control_points)-2, 1)]
            
            # Untuk setiap segmen, terapkan make_bezier_three_point dan tambahkan ke self.curve_points
            for segment in segments:
                segment_curve_points = self.make_bezier_three_point(*segment, iterations=iterations)
                #print (segment_curve_points)
                self.curve_points.extend(segment_curve_points)

        #print(self.curve_points)


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