import customtkinter as tk
import time
import numpy as np
from GlobalData import Database as db

class BezierCanvasAnimation(tk.CTkCanvas):
    def __init__(self, master, control_points, iteration, animation_Speed, weight_line, weight_curve , weight_circle ,interpolated_weight):
        super().__init__(master, width=2000, height=1100, bg="white")
    
        # Setup Canvas Environtments
        self.start_time = time.time()
        self.update_idletasks()
    
        self.iteration = iteration

        # Animation properties
        self.animation_speed = animation_Speed  # the less, the faster

        self.weight_line = weight_line
        self.weight_curve = weight_curve
        self.weight_circle = weight_circle
        self.interpolated_weight = interpolated_weight


    def setup_bezier_animation(self):
        self.draw_points()
        self.prev_lines = []
        self.interpolated_lines = []

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
    def animation(self, bezier_points, counter=0):

        for line_id in self.interpolated_lines:
            self.delete(line_id)
        self.interpolated_lines.clear()

        t = counter / self.length_bezier
        x1, y1 = bezier_points[0]
        x2, y2 = bezier_points[1]
        line_id = self.create_line(x1, y1, x2, y2, fill='red',width=self.weight_curve)
        w = self.weight_circle
        self.create_oval(x2 -w , y2 - w, x2 + w, y2 + w, fill='red')
        self.prev_lines.append(line_id)
        bezier_points.pop(0)

        temp_points = self.control_points.copy()
        temp_of_dots = []
        while len(temp_points) != 2:
            temp_of_dots.clear()
            for i in range(len(temp_points) - 1):
                interpolate_points = self.interpolate_line(temp_points[i], temp_points[i + 1], t)
                temp_of_dots.append(interpolate_points)
    
            temp_points = temp_of_dots.copy()
            for i in range(len(temp_of_dots) - 1):
                line_id = self.create_line(temp_of_dots[i][0], temp_of_dots[i][1], temp_of_dots[i + 1][0], temp_of_dots[i + 1][1], width=self.interpolated_weight)
                self.interpolated_lines.append(line_id)
        last_interpolated_point = temp_of_dots[-1]
        x_last, y_last = last_interpolated_point
        x_second_control, y_second_control = bezier_points[-1]

        line_id = self.create_line(x_last, y_last, x_second_control, y_second_control, width= self.interpolated_weight)
        self.interpolated_lines.append(line_id)
        if len(bezier_points) > 1:
            self.after(100, lambda: self.animation(bezier_points, counter + 1))
        else:
            print("Counter: ", counter)
            print("Length: ", self.length_bezier)


class DNC_Algorthm(BezierCanvasAnimation):
    def __init__(self,master,control_points,iteration,animation_speed, weight_line = 0, weight_circle = 5, weight_curve = 0, interpolated_weight = 1):
        super().__init__(master, control_points, iteration,animation_speed,weight_circle=weight_circle,weight_line=weight_line,weight_curve= weight_curve, interpolated_weight=interpolated_weight)
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
            return curve_points1 + curve_points2
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

    def midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def midpoint_of_three(self, a, b, c):
        # Menghitung midpoint dari tiga titik
        return self.midpoint(self.midpoint(a, b), self.midpoint(b, c))

    def change_control_points(self, canvas_width, canvas_height):
        self.control_points = db.handle_control_points(canvas_height,canvas_width)

    def bezier_curve(self):
        for line_id in self.prev_lines:
            self.delete(line_id)
        self.prev_lines.clear()
        if len(self.control_points) == 3:

            bezier_points = self.make_bezier_three_point(*self.control_points, iterations=self.iteration)
            end_time = time.time()

            
            self.length_bezier = len(bezier_points) - 2
            db.set_time_execution(end_time - self.start_time)
            self.animation(bezier_points)
        else:
            segments = [self.control_points[i:i + 3] for i in range(0, len(self.control_points) - 2, 1)]

            bezier_points = []
            for segment in segments:
                
                segment_curve_points = self.make_bezier_three_point(*segment, iterations=self.iteration)
                # print (segment_curve_points)
                bezier_points.extend(segment_curve_points)
            self.length_bezier = len(bezier_points) - 2
            print("lenght: ",self.length_bezier)
            self.end_time = time.time()
            db.set_time_execution(self.end_time - self.start_time)
            self.animation(bezier_points)

class BruteForce_Algorithm(BezierCanvasAnimation):
    def __init__(self,master,control_points,iterations,animation_speed, weight_line = 0,weight_circle = 5, weight_curve = 0, interpolated_weihgt= 1):
        super().__init__(master, control_points, iterations,animation_speed,weight_circle=weight_circle, weight_curve=weight_curve, interpolated_weight=interpolated_weihgt,weight_line=weight_line)

    def change_control_points(self, canvas_height, canvas_width):
        self.control_points = db.handle_control_points(canvas_height, canvas_width)

    def bezier_curve(self):
        
        bezier_points = []
        if (len(self.control_points) == 3):
            p0, p1, p2 = self.control_points
            t_values = np.linspace(0,1,num=1 + self.iteration * 2)
            for i in range(len(self.control_points) - 2):
                for t in t_values:
                    qx0 = (1 - t) * p0[0] + t * p1[0]
                    qy0 = (1 - t) * p0[1] + t * p1[1]
                    qx1 = (1 - t) * p1[0] + t * p2[0]
                    qy1 = (1 - t) * p1[1] + t * p2[1]
                    x_new = (1 - t) * qx0 + t * qx1
                    y_new = (1 - t) * qy0 + t * qy1
                    bezier_points.append((x_new, y_new))
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