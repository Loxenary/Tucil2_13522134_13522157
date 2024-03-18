import matplotlib.pyplot as plt

class BezierCurve:
    def __init__(self):
        self.curve_points = []
        self.control_points = []
        self.midpoints = []
        self.leftmid = []
        self.rightmid = []
        self.first_iterate = []

    def calculate_bezier_three_point(self, control_points, iterations):
        curve_points = []
        if len(control_points) == 3 and iterations == 1:
            # Menghitung titik tengah hanya jika iterasi = 1
            midpoint = self.midpoint_of_three(*control_points)
            curve_points.append(midpoint)
        elif len(control_points) == 3 and iterations > 1:
            # Iterasi lebih dari 1: menghitung dua set titik kurva Bezier dalam satu iterasi
            midpoint_a = self.midpoint(control_points[0], control_points[1])
            midpoint_b = self.midpoint(control_points[1], control_points[2])
            midpoint_of_three = self.midpoint_of_three(control_points[0], control_points[1], control_points[2])

            # Memanggil rekursi untuk dua set titik kurva Bezier
            curve_points1 = self.calculate_bezier_three_point([control_points[0], midpoint_a, midpoint_of_three], iterations - 1)
            curve_points2 = self.calculate_bezier_three_point([midpoint_of_three, midpoint_b, control_points[2]], iterations - 1)

            # Menggabungkan hasil dari dua set titik kurva Bezier
            curve_points.extend(curve_points1)
            curve_points.extend(curve_points2)

        return curve_points

    def make_bezier_three_point(self, *control_points, iterations):
        curve_points = []

        # Menghitung titik kurva Bezier untuk tiga titik kontrol
        iterations1 = self.midpoint_of_three(*control_points)
        curve_points.append(iterations1)

        # Menghitung titik kurva Bezier tambahan jika iterasi lebih dari 1
        if iterations > 1:
            # Hitung semua titik kurva Bezier untuk titik kontrol yang diberikan
            all_curve_points = self.calculate_bezier_three_point(control_points, iterations)

            # Bagi titik kurva Bezier menjadi dua bagian
            left = all_curve_points[:len(all_curve_points)//2]
            for point in left[::-1]:
                curve_points.insert(0, point)
            right = all_curve_points[len(all_curve_points)//2:]

            curve_points.extend(right)

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
            self.make_bezier_n_point(*control_points,iterations = iterations)
            #print(self.curve_points)
            #print(len(self.first_iterate))
            #print(self.first_iterate)
            self.leftmid.extend(self.first_iterate[1:len(self.first_iterate)//2+1])
            #print(len(self.leftmid))
            #print(self.leftmid)
            self.rightmid.extend(self.first_iterate[len(self.first_iterate)//2+1:])
            #print(len(self.rightmid))
            #print(self.rightmid)
            #kondisi 1 : x.p1 <x.p2 & y.p1<y.p2 & x.pakhir<x.psebelumakhir & y.pakhir<y.psebelum akhir
            if(control_points[-1][0] < control_points[-2][0] and control_points[-1][1] < control_points[-2][1] and control_points[0][0]<control_points[1][0] and control_points[0][1]<control_points[1][1]):
                self.curve_points.extend(self.leftmid[::-1])
                self.curve_points=sorted(self.curve_points,key=lambda p:p[0])
                self.curve_points.append(self.first_iterate[0])
                self.rightmid = sorted(self.rightmid, key=lambda p:p[1])
                self.curve_points.extend(self.rightmid[::-1])
            elif(control_points[-1][0] < control_points[-2][0] and control_points[-1][1] < control_points[-2][1] and control_points[0][0]>control_points[1][0] and control_points[0][1]<control_points[1][1]):
                #kondisi 2 : x.p1 >x.p2 & y.p1>y.p2 & x.pakhir<x.psebelumakhir & y.pakhir<y.psebelum akhir
                self.leftmid = sorted(self.leftmid, key=lambda p:p[1])
                self.curve_points.extend(self.leftmid)
                self.curve_points.append(self.first_iterate[0])
                self.rightmid = sorted(self.rightmid, key=lambda p:p[1])
                self.curve_points.extend(self.rightmid[::-1])
            elif(control_points[-1][0] < control_points[-2][0] and control_points[-1][1] > control_points[-2][1] and control_points[0][0]>control_points[1][0] and control_points[0][1]<control_points[1][1]):
                #kondisi 3 : x.p1 >x.p2 & y.p1<y.p2 & x.pakhir<x.psebelumakhir & y.pakhir>y.psebelum akhir
                self.leftmid = sorted(self.leftmid, key=lambda p:p[1])
                self.curve_points.extend(self.leftmid)
                self.curve_points.append(self.first_iterate[0])
                # Temukan nilai minimum dari self.rightmid berdasarkan x
                min_index_y = min(range(len(self.rightmid)), key=lambda i: self.rightmid[i][1])
                # Pisahkan setengah pertama dan setengah terakhir dari self.rightmid
                first_half = self.rightmid[:min_index_y+1]
                second_half = self.rightmid[min_index_y+1:]
                # Urutkan setengah pertama berdasarkan x dan setengah terakhir berdasarkan y
                first_half_sorted = sorted(first_half, key=lambda p: p[0])
                #print(first_half_sorted)
                second_half_sorted = sorted(second_half, key=lambda p: p[1])
                # Gabungkan kedua setengah yang sudah diurutkan
                sorted_rightmid = first_half_sorted + second_half_sorted
                # Perpanjang self.curve_points dengan self.rightmid yang sudah diurutkan
                self.curve_points.extend(sorted_rightmid)
            else:
                self.curve_points.extend(self.first_iterate)
                self.curve_points = sorted(self.curve_points,key=lambda p:p[0])

    def make_bezier_n_point(self, *control_points, iterations):
        first_iterate = []
        new_control_points = []
        for i in range(len(control_points) - 1):
            midpoint = self.midpoint(control_points[i], control_points[i + 1])
            new_control_points.append(midpoint)

        if len(new_control_points) > 3:
            new_control_points = self.make_bezier_n_point(*new_control_points, iterations=1)

        elif len(new_control_points) == 3:
            first_iterate = self.make_bezier_three_point(*new_control_points, iterations=1)
            self.first_iterate.extend(first_iterate)
            #print(self.first_iterate)
            #print(first_iterate)
        #print(self.midpoints)

        left_points = []
        right_points = []
        if(iterations > 1):
            left_index = len(self.midpoints) - 1
            pola = 2
            #print(left_index)
            for i in range(len(control_points)-1):
                left_points.insert(0, self.midpoints[left_index])
                left_index -= pola
                pola += 1
                #print(left_index)
            left_points.insert(0, control_points[0])

            right_index = len(self.midpoints)-1
            pola = 1
            for i in range(len(control_points)-1):
                #print(right_index)
                right_points.append(self.midpoints[right_index])
                right_index -= pola
                pola+=1
            right_points.append(control_points[len(control_points)-1])

            #print("left_points:", left_points)
            #print("right_points:", right_points)
            self.midpoints.clear()
            hasil_kiri = self.make_bezier_n_point(*left_points, iterations=iterations - 1)
            hasil_kanan = self.make_bezier_n_point(*right_points, iterations=iterations - 1)

        elif iterations == 1:
            return self.first_iterate

    def midpoint(self, p1, p2):
        midpoint = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        if midpoint not in self.midpoints:
            self.midpoints.append(midpoint)
        return (midpoint)
    
    def midpoint_of_three(self, a, b, c):
        # Menghitung midpoint dari tiga titik
        return self.midpoint(self.midpoint(a, b), self.midpoint(b, c))

    def plot_curve(self):
        # Menghubungkan titik kontrol pertama dengan titik kurva pertama
        if len(self.curve_points) > 0:
            self.curve_points.insert(0, self.control_points[0])
            
        # Menghubungkan titik kontrol terakhir dengan titik kurva terakhir
        if len(self.curve_points) > 0:
            self.curve_points.append(self.control_points[-1])

        # Plot titik kontrol
        plt.plot(*zip(*self.control_points), marker='o', color='red', label='Control Points')
        
        # Plot kurva Bezier
        plt.plot(*zip(*self.curve_points), linestyle='--', color='gray')
        plt.plot(*zip(*self.curve_points), marker='o', color='blue', label='Bezier Curve')

        # Plot midpoints
        #plt.plot(*zip(*self.midpoints), marker='o', color='green', linestyle='None',label='midpoint')
        
        plt.legend()
        plt.title('Bezier Curve')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()
        