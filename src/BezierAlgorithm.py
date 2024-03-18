import customtkinter as tk
import time
import numpy as np
from GlobalData import Database as db

# Base class for handling animation
class BezierCanvasAnimation(tk.CTkCanvas):
    def __init__(self, master, control_points, iteration, animation_Speed, weight_line, weight_curve , weight_circle ,interpolated_weight):
        super().__init__(master, width=2000, height=1100, bg="white")


        # Setup Canvas Environtment
        # update all widget
        self.update_idletasks()

        # save iteration
        self.iteration = iteration

        # Animation properties
        self.animation_speed = animation_Speed  # the less, the faster

        # save weight for line styling
        self.weight_line = weight_line
        self.weight_curve = weight_curve
        self.weight_circle = weight_circle
        self.interpolated_weight = interpolated_weight
        self.control_points = control_points

    # setup variables used to save the line data
    def setup_bezier_animation(self):
        # Draw all the control points and its line
        self.draw_points()
        self.prev_lines = []
        self.interpolated_lines = []

    # Draw all the control points and its line
    def draw_points(self):
        points_container = None
        for i in range(len(self.control_points)):
            x0, y0 = self.control_points[i]
            w = self.weight_circle
            w2 = self.weight_line
            self.create_oval(x0 - w, y0 - w, x0 + w, y0 + w, fill="blue")
            if points_container:
                self.create_line(points_container[0], points_container[1], x0, y0, fill='blue', width=w2)
            points_container = (x0, y0)

    # Creating an interpolation line to animate the helping line for bezier curves creation
    def interpolate_line(self, p1, p2, t):
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        return x, y
    
    # Main function to animate the bezier curves and its helping line
    def animation(self, bezier_points, counter=0):

        # Delete all the helping lines for each new iteration
        for line_id in self.interpolated_lines:
            self.delete(line_id)
        self.interpolated_lines.clear()

        # get the sync time for the helping lines corresponding to current creation of the bezier curves
        t = counter / self.length_bezier
        x1 = bezier_points[0][0]
        y1 = bezier_points[0][1]
        x2 = bezier_points[1][0]
        y2 = bezier_points[1][1]
        
        # Createing the bezier curves
        line_id = self.create_line(x1, y1, x2, y2, fill='red',width=2)
        w = self.weight_circle
        self.create_oval(x2 -w , y2 - w, x2 + w, y2 + w, fill='red')
        self.prev_lines.append(line_id)
        bezier_points.pop(0)

        # Creating the helping lines
        temp_points = self.control_points.copy()
        temp_of_dots = []
        while len(temp_points) != 2:
            temp_of_dots.clear()
            for i in range(len(temp_points) - 1):
                interpolate_points = self.interpolate_line(temp_points[i], temp_points[i + 1], t)
                temp_of_dots.append(interpolate_points)
    
            temp_points = temp_of_dots.copy()
            for i in range(len(temp_of_dots) - 1):
                line_id = self.create_line(temp_of_dots[i][0], temp_of_dots[i][1], temp_of_dots[i + 1][0], temp_of_dots[i + 1][1], width=self.interpolated_weight, fill="green")
                self.interpolated_lines.append(line_id)
        
        # bind the last line to the last control points
        last_interpolated_point = temp_of_dots[-1]
        x_last, y_last = last_interpolated_point
        x_second_control, y_second_control = bezier_points[-1]

        line_id = self.create_line(x_last, y_last, x_second_control, y_second_control, width= self.interpolated_weight)
        self.interpolated_lines.append(line_id)

        # Re animate the canvas widgets
        if len(bezier_points) > 1:
            self.after(self.animation_speed, lambda: self.animation(bezier_points, counter + 1))
        else:
            for line_id in self.interpolated_lines:
                self.delete(line_id)
            self.interpolated_lines.clear()
        


class DNC_Algorthm(BezierCanvasAnimation):
    def __init__(self,master,control_points,iteration,animation_speed, weight_line = 0, weight_circle = 5, weight_curve = 0, interpolated_weight = 1):
        super().__init__(master, control_points, iteration,animation_speed,weight_circle=weight_circle,weight_line=weight_line,weight_curve= weight_curve, interpolated_weight=interpolated_weight)
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

    def make_bezier_three_point(self, control_points, iterations):
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


    def make_bezier(self, control_points, iterations):
        for line_id in self.interpolated_lines:
            self.delete(line_id)
        self.interpolated_lines.clear()

        self.control_points = list(control_points)
        # Jumlah titik kontrol harus minimal 3
        if len(control_points) < 3:
            print("Error: Minimum 3 control points required.")
            return

        # Jika jumlah titik kontrol sama dengan 3, gunakan make_bezier_three_point
        elif len(control_points) == 3:
            self.curve_points = self.make_bezier_three_point(control_points, iterations=iterations)
            return

        else:
            self.make_bezier_n_point(control_points,iterations = iterations)

            self.leftmid.extend(self.first_iterate[1:len(self.first_iterate)//2+1])

            self.rightmid.extend(self.first_iterate[len(self.first_iterate)//2+1:])

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
               
                second_half_sorted = sorted(second_half, key=lambda p: p[1])
                # Gabungkan kedua setengah yang sudah diurutkan
                sorted_rightmid = first_half_sorted + second_half_sorted
                # Perpanjang self.curve_points dengan self.rightmid yang sudah diurutkan
                self.curve_points.extend(sorted_rightmid)
            else:
                self.curve_points.extend(self.first_iterate)
                self.curve_points = sorted(self.curve_points,key=lambda p:p[0])

    def make_bezier_n_point(self, control_points, iterations):
        first_iterate = []
        new_control_points = []
        for i in range(len(control_points) - 1):
            midpoint = self.midpoint(control_points[i], control_points[i + 1])
            new_control_points.append(midpoint)

        if len(new_control_points) > 3:
            new_control_points = self.make_bezier_n_point(new_control_points, iterations=1)

        elif len(new_control_points) == 3:
            first_iterate = self.make_bezier_three_point(new_control_points, iterations=1)
            self.first_iterate.extend(first_iterate)


        left_points = []
        right_points = []
        if(iterations > 1):
            left_index = len(self.midpoints) - 1
            pola = 2

            for i in range(len(control_points)-1):
                left_points.insert(0, self.midpoints[left_index])
                left_index -= pola
                pola += 1
    
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
            hasil_kiri = self.make_bezier_n_point(left_points, iterations=iterations - 1)
            hasil_kanan = self.make_bezier_n_point(right_points, iterations=iterations - 1)

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
    
    def change_control_points(self, canvas_height, canvas_width):
        self.control_points = db.handle_control_points(canvas_height, canvas_width)

    def bezier_curve(self):
        self.start_time = time.time()
        for line_id in self.prev_lines:
            self.delete(line_id)
        self.prev_lines.clear()

        self.make_bezier(self.control_points,iterations= self.iteration)
        self.endtime = time.time()
        db.set_time_execution(self.endtime - self.start_time)
        self.length_bezier = len(self.curve_points)
        # Menghubungkan titik kontrol pertama dengan titik kurva pertama
        if len(self.curve_points) > 0:
            self.curve_points.insert(0, self.control_points[0])
            
        # Menghubungkan titik kontrol terakhir dengan titik kurva terakhir
        if len(self.curve_points) > 0:
            self.curve_points.append(self.control_points[-1])
        
        # self.animation(self.first_iterate)
        self.animation(self.curve_points)

class BruteForce_Algorithm(BezierCanvasAnimation):
    def __init__(self,master,control_points,iterations,animation_speed, weight_line = 0,weight_circle = 5, weight_curve = 0, interpolated_weihgt= 1):
        super().__init__(master, control_points, iterations,animation_speed,weight_circle=weight_circle, weight_curve=weight_curve, interpolated_weight=interpolated_weihgt,weight_line=weight_line)

    def change_control_points(self, canvas_height, canvas_width):
        self.control_points = db.handle_control_points(canvas_height, canvas_width)

    def bezier_curve(self):
        
        bezier_points = []
        self.start_time = time.time()
        if (len(self.control_points) == 3):
            p0, p1, p2 = self.control_points
            N = 2**self.iteration + 1

            t_base = np.linspace(0, 1, num=N)
            t_values = np.zeros(N)

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
                    if new_points not in bezier_points:
                        bezier_points.append(new_points)
            if self.control_points[-1] not in bezier_points:
                bezier_points.append(self.control_points[-1])
        
            self.length_bezier = len(bezier_points) - 2
            self.end_time = time.time()
            db.set_time_execution(self.end_time - self.start_time)
            self.animation(bezier_points)

def algorithm_decider(algorithm):
    if(algorithm == "DNC"):
        return "DNC"
    else:
        return "BF"