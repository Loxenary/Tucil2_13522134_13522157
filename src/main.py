import gui2
import Bezier_dnc
import customtkinter as tk
if __name__ == "__main__":
    # gui2.main()
    root = tk.CTk()
    
    
    control_points = [(100,200),(200,300),(500,100),(500,400),(200,500)]  
    iterations = 3
    Bezier_dnc.DncAnimation(root,control_points,iterations)
    root.mainloop()


'''

        for line_id in self.prev_lines:
                self.delete(line_id)
        self.prev_lines.clear()
                
        points = list(points)
        t = self.step / self.steps
        prev_x, prev_y = points[0]
        x = (1 - t) ** 3 * points[0][0] + 3 * t * (1 - t) ** 2 * points[1][0] + 3 * t ** 2 * (1 - t) * points[2][0] + t ** 3 * points[3][0]
        y = (1 - t) ** 3 * points[0][1] + 3 * t * (1 - t) ** 2 * points[1][1] + 3 * t ** 2 * (1 - t) * points[2][1] + t ** 3 * points[3][1]

        temp_of_dots = []
        if self.step > 0:
            temp_points = self.lines_container.copy()
            container = []
            while(len(temp_points) != 2): 
                temp_of_dots.clear()               
                for i in range(len(temp_points)-1):
                    interpolated_points = self.interpolate_line(temp_points[i],temp_points[i+1],t)
                    temp_of_dots.append(interpolated_points)

                print("Interpolate: ", temp_of_dots)
                temp_points = temp_of_dots.copy()
                for i in range(len(temp_of_dots)-1):
                    line_id= self.create_line(temp_of_dots[i][0] + 5,temp_of_dots[i][1] + 5,temp_of_dots[i+1][0] + 5,temp_of_dots[i+1][1]+ 5)   
                    self.prev_lines.append(line_id)        
            print("c1: ",temp_of_dots)
            # container.append(temp_points.copy())
            # print("c2: ",container)

            prev_x, prev_y = self.point_curve[-1]
            self.create_line(prev_x, prev_y, x, y, fill="red")
        self.point_curve.append((x, y))
        self.step += 1
        if self.step <= self.steps:
            time.sleep(0.25)
            self.after(1
            , lambda: self.bezier_curve(self.point_curve))  

'''