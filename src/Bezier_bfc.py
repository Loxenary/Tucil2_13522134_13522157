import customtkinter as tk
import time
import numpy as np
class BezierBruteForce(tk.CTkCanvas):
    def __init__(self,master, control_points, iteration):
        super().__init__(master)
        self.configure(width=800, height=600, bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        
        self.start_time = time.time()
        self.update_idletasks()

        self.iteration = iteration
        self.control_points = [(x, self.winfo_reqheight() - y) for x,y in control_points]

    def setup_bezier_animation(self):
        self.draw_points()
        self.prev_lines = []
        self.interpolated_lines = []
        self.bezier_curve()

    def draw_points(self):
        points_container = None
        for i in range(len(self.control_points)):
            x0, y0 = self.control_points[i]
            self.create_oval(x0, y0, x0 + 10, y0 + 10, fill="blue")
            if(points_container):
                self.create_line(points_container[0] + 5,points_container[1] + 5,x0 + 5,y0 + 5,fill='blue')

    def animation(self,*bezier_points, counter= 0):
        
    def bezier_curve(self):
        bezier_points = []
        if len(self.control_points == 3):
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
        

    