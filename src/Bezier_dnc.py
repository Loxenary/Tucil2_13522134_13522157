import customtkinter as tk
import time

class DncAnimation(tk.CTkCanvas):
    def __init__(self,master, control_points, iteration):
        super().__init__(master,width=800, height=600,bg="white")
        self.pack()
        self.pack_configure(fill=tk.BOTH,expand=True)
        self.start_time = time.time()
        self.update_idletasks()
        # Bezier Curves Data
        self.control_points = control_points
        self.iteration = iteration

        self.control_points = [(x, self.winfo_reqheight() - y) for x, y in control_points]

        self.step = 0
        self.steps = 20
        self.draw_points()
        self.lines_container = self.control_points.copy()
        self.prev_lines = []
        self.interpolated_lines = []
        self.bezier_curve()
    
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

    def midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def midpoint_of_three(self, a, b, c):
        # Menghitung midpoint dari tiga titik
        return self.midpoint(self.midpoint(a, b), self.midpoint(b, c))

    # Draw Static Lines for the control points
    def draw_points(self):
        points_container = None
        for i in range(len(self.control_points)):
            x0, y0 = self.control_points[i]
            self.create_oval(x0 - 5, y0 - 5, x0 + 5, y0 + 5, fill="blue")
            if(points_container):
                self.create_line(points_container[0],points_container[1],x0,y0,fill='blue')
            points_container = (x0,y0)

    # Creating an interpolation line to animate the helping line for bezier curves creation
    def interpolate_line(self,p1,p2,t):
        x1= p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        return x, y        

    def animation(self,bezier_points,counter = 0):
        
        for line_id in self.interpolated_lines:
            self.delete(line_id)
        self.interpolated_lines.clear()
        
        t = counter / self.length_bezier
        x1, y1 = bezier_points[0]
        x2, y2 = bezier_points[1]
        line_id = self.create_line(x1, y1, x2, y2,fill='red')
        self.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='red')
        self.prev_lines.append(line_id)
        bezier_points.pop(0)


        temp_points = self.lines_container.copy()
        temp_of_dots = []
        while(len(temp_points) !=2):
            temp_of_dots.clear()
            for i in range(len(temp_points) - 1):
                interpolate_points = self.interpolate_line(temp_points[i], temp_points[i + 1],t)
                temp_of_dots.append(interpolate_points)
            print("Interpolate: ",temp_of_dots)
            temp_points = temp_of_dots.copy()
            for i in range(len(temp_of_dots)-1):
                line_id = self.create_line(temp_of_dots[i][0],temp_of_dots[i][1],temp_of_dots[i + 1][0], temp_of_dots[i+1][1])
                self.interpolated_lines.append(line_id)
        last_interpolated_point = temp_of_dots[-1]
        x_last, y_last = last_interpolated_point
        x_second_control, y_second_control = bezier_points[-1]
        line_id = self.create_line(x_last, y_last, x_second_control, y_second_control)
        self.interpolated_lines.append(line_id)
        if(len(bezier_points) > 1):
            print("t: ",t)
            iterator = len(bezier_points) / self.length_bezier
            self.after(300,lambda: self.animation(bezier_points,counter + 1))
        
    def bezier_curve(self):
        for line_id in self.prev_lines:
            self.delete(line_id)
        self.prev_lines.clear()
        if(len(self.control_points) == 3):
        
            bezier_points = self.make_bezier_three_point(*self.control_points,iterations=self.iteration)
            end_time = time.time()

            print("Time: ",end_time - self.start_time)
            self.length_bezier = len(bezier_points) - 2
        
            self.animation(bezier_points)


            # if self.step <= self.steps: