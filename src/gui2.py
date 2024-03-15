import customtkinter as tk
from tkinter import messagebox
import os
from PIL import Image

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1243x714")
        self.setupFrame()

    def setupFrame(self):
        self.InputFrame = InputFrame(self)
        self.OutputFrame = OutputFrame(self)
class InputFrame(tk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent,corner_radius=0)
        self.pack()
        self.parent = parent
        self.pack_configure(side="left",fill="both")
        self.setupScrollableContainer()
        self.container = InputContainer(self.scrollable_frame)
        self.canvas.bind_all("<MouseWheel>",self.on_mousewheel)

    def on_mousewheel(self,event):
        text = str(event.widget)
        if "inputframe" in text:
            self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        
    def setupScrollableContainer(self):
        def on_canvas_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas = tk.CTkCanvas(self,bg="#384764")
        self.scrollable_frame = tk.CTkFrame(self.canvas,fg_color='#384764')
        self.scrollable_frame.bind("<Configure>",on_canvas_configure)
        
        self.scroll_bar = tk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        self.scroll_bar.pack()
        self.scroll_bar.pack_configure(side="right",fill='y')
        self.canvas.pack()
        self.canvas.pack_configure(side="left",fill="both",expand=True)
class InputContainer(tk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent, corner_radius=0, border_width=0, border_color="#D9D9D9", fg_color="#384764")
        self.pack()
        self.pack_configure(fill="x",expand=True)
        self.font = tk.CTkFont(family="Courier New",size =20)
        self.entryplaceholder = "Max 500"
        self.default_text_color = "white"

        # Call Setup Field
        self.setupIterationField()
        self.setupPointsField()
        self.setupButton()

    # Setup the Iteration input field component
    def setupIterationField(self):
        def validate_iteration(action, value_if_allowed):
            if not value_if_allowed: 
                return True
            if value_if_allowed == self.entryplaceholder:
                return True
            if(action == '1'):
                if value_if_allowed.isdigit() and int(value_if_allowed) <= 500:
                    return True
                return False
            return True
        def remove_placeholder(event):
            if self.entry_iteration.get() == self.entryplaceholder:
                self.entry_iteration.delete("0", "end")
                self.entry_iteration.configure(text_color="black")
        def add_placeholder(event):
            if(not self.entry_iteration.get()):
                self.entry_iteration.delete(0,tk.END)
                self.entry_iteration.insert("0",self.entryplaceholder)
            
        validate_input = (self.register(validate_iteration), '%d','%P')
        # Label
        self.label_iteration = tk.CTkLabel(self, text="Input Points", font=self.font, text_color=self.default_text_color, anchor="w")
        

        self.label_iteration.pack()
        self.label_iteration.pack_configure(padx=(50,50), pady=(40,30))
        # Entry
        self.entry_iteration = tk.CTkEntry(self, width=172,height=44, border_width=1, border_color="#5B5B5B",corner_radius=2, font=("georgia",20),text_color="#AEAEAE",validate="key", validatecommand=validate_input)

        self.entry_iteration.insert("0",self.entryplaceholder)
        self.entry_iteration.configure(fg_color="#D9D9D9")

        self.entry_iteration.bind("<FocusIn>",remove_placeholder)
        self.entry_iteration.bind("<FocusOut>",add_placeholder)

        self.entry_iteration.configure(justify="center")
        self.entry_iteration.pack()
        self.entry_iteration.pack_configure(padx=(50,50), pady=(0,40),anchor="center")
    # Setup the Point input field components
    def setupPointsField(self):
        self.inputField = InputFieldDots(self)
    
    # Setup the main functioning button
    def setupButton(self):
        self.data_x = self.inputField.entry_x
        self.data_y = self.inputField.entry_y
        # Check is the Data for iteration is Empty or not
        def isIterationValid():
            current_text = self.entry_iteration.get()
            return (current_text == "" or current_text == self.entryplaceholder or (not current_text.isdigit()))
        def isBlankOnData():

            length_entry = len(self.data_x)
            for i in range(length_entry):
                if(self.data_x[i].get() == "X" or self.data_y[i].get() == "Y" or (not self.data_x[i].get().isdigit())):
                    return True
            return False
        def DataSave():
            self.data_path = os.path.join(os.path.dirname(__file__),"data.txt")
            if(isIterationValid()):
                messagebox.showwarning("Iteration InValid","Please fill the Iteration Field or Re-input the valid data for the iteration")
                return
            if(isBlankOnData()):
                messagebox.showwarning("Field Data Invalid","Please Fill all the Input Dots or Re-input the valid data for the data field")
                return               
            data_iteration = self.entry_iteration.get()
            if(self.data_path):
                with open(self.data_path, "w") as f:
                    f.write(f'{data_iteration}\n')
                with open(self.data_path, "a") as f:
                    for x_entry, y_entry in zip(self.data_x,self.data_y):
                        x_value = x_entry.get()
                        y_value = y_entry.get()
                        if x_value and y_value:
                            f.write(f'{x_value} {y_value}\n')
                messagebox.showinfo("Data Saved","Data Saved Successfully")
        def BruteForceCallout():
            DataSave()
            #TODO: Implement Bruteforce funcion on Bezier Curve

        def DecreaseAndConquerCallout():
            DataSave()
            #TODO: Implement Decrease and Conquer funcion on Bezier Curve        

        self.brute_force_button = tk.CTkButton(self, text="Brute Force", fg_color="#F8DFDF", text_color='black', hover_color='#FF93A6', width=172, height=54, font=('georgia',20),command=BruteForceCallout)

        self.brute_force_button.pack()
        self.brute_force_button.pack_configure(pady=20)

        self.decrease_conquer_button =  tk.CTkButton(self, text="Decrease and \nConquer",fg_color="#EAFFE3", text_color='black', hover_color="#B6FF89", width=172, height=54, font=('georgia',20),command=DecreaseAndConquerCallout)

        self.decrease_conquer_button.pack()
        self.decrease_conquer_button.pack_configure(pady=20)
class InputFieldDots:
    def __init__(self,parent):
        self.parent = parent

        self.entry_x = []
        self.entry_y = []

        self.buttonPhoto_x = 40
        self.buttonPhoto_y = 35

        self.buttonHeight = 30
        self.buttonWidth = 25
        self.buttonColor = "#384764"

        self.max_value = 20
        self.validate_points_cmd = (self.parent.register(self.validate_num_points), '%d','%P')

        self.ButtonPreparation()
        self.SetupDataInput()
        self.SetupListDataField()
    # Prepate Button Images
    def ButtonPreparation(self):
        button_image_path = os.path.join(os.path.dirname(__file__), "Assets","triangle.png")
        button_image = Image.open(button_image_path)

        self.left_button_image = button_image.rotate(90)
        self.right_button_image = button_image.rotate(-90)
        
        self.left_button_image = tk.CTkImage(self.left_button_image,size=(self.buttonPhoto_x,self.buttonPhoto_y))

        self.right_button_image = tk.CTkImage(self.right_button_image,size=(self.buttonPhoto_x,self.buttonPhoto_y))

    # Point Validation for Data Field
    def validate_num_points(self,action,value_if_allowed):
            if not value_if_allowed:  # Allow if the entry is empty
                return True
            if value_if_allowed == 'X' or value_if_allowed == 'Y':
                return True
            if action == '1':  # Insert action
                if value_if_allowed.isdigit():
                    return True   
                elif value_if_allowed == '-' or value_if_allowed[1:].isdigit():
                    return True
                return False
            return True

    # Update all the data fields grid
    def update_entry_fields(self):
        num_of_dots = self.InputLabel.cget("text")
        try:
            num_of_dots = int(num_of_dots)
            
            if num_of_dots >= 3 and num_of_dots <= self.max_value:
                pad_y = 20
                tab_height = 35
                tab_width = 62
                text_size = 20
                for i in range(num_of_dots):
                    if i < len(self.entry_x):
                        self.entry_x[i].grid()
                        self.entry_y[i].grid()
                        self.entry_x[i].configure(height=tab_height, width=tab_width,font=("Helvatica",text_size))
                        self.entry_y[i].configure(height=tab_height, width=tab_width,font=("Helvatica",text_size))
                        self.entry_x[i].grid_configure(pady = pad_y)
                    else:
                        new_entry_x = tk.CTkEntry(self.frame_point, height=tab_height, width=tab_width, text_color="black", corner_radius=2, placeholder_text="X",placeholder_text_color="#AEAEAE",font=('Helvatica',text_size),fg_color="#D9D9D9", validate="key",validatecommand=self.validate_points_cmd)

                        new_entry_x.grid(column=0, row=i, padx=20, pady=pad_y)
                        
                        self.entry_x.append(new_entry_x)
                        new_entry_y = tk.CTkEntry(self.frame_point, height=tab_height, width=tab_width, text_color="black", corner_radius=2, placeholder_text="Y",placeholder_text_color="#AEAEAE", font=('Helvatica',text_size), fg_color="#D9D9D9", validate="key",validatecommand=self.validate_points_cmd)
                        new_entry_y.grid(column=1, row=i, padx=20)
                        
                        self.entry_y.append(new_entry_y)

                for i in range(num_of_dots, len(self.entry_x)):
                    self.entry_x[i].grid_remove()
                    self.entry_y[i].grid_remove()
        except ValueError:
            pass

    # Setup the data input components 
    def SetupDataInput(self):
        def LeftButtonClick():
            current_value = int(self.InputLabel.cget("text"))
            if current_value > 3:
                self.InputLabel.configure(text=str(current_value - 1))
                if current_value - 1 == 3:
                    self.leftbutton.configure(state="disabled")
                self.rightButton.configure(state="enabled")
                self.update_entry_fields()
        def RightButtonClick():
            current_value = int(self.InputLabel.cget("text"))
            if current_value < self.max_value:
                self.InputLabel.configure(text=str(current_value + 1))
                if current_value + 1 == self.max_value:
                    self.rightButton.configure(state="disabled")

                self.leftbutton.configure(state="enabled")
                self.update_entry_fields()


        # Label for the Data Input
        self.LabelData = tk.CTkLabel(self.parent, text="Input Dots",font=self.parent.font, text_color="white",anchor="w")
        self.LabelData.pack()
        self.LabelData.pack_configure(pady=(0,30))

        # Frame for Input Data
        self.DataInputFrame = tk.CTkFrame(self.parent,fg_color=self.buttonColor)
        self.DataInputFrame.pack()
        
        # Left button 
        self.leftbutton = tk.CTkButton(self.DataInputFrame,image=self.left_button_image,command=LeftButtonClick, border_width=0, text="", height= self.buttonHeight,width=self.buttonWidth,fg_color=self.buttonColor,corner_radius=0,hover=False)
        self.leftbutton.grid()
        self.leftbutton.grid_configure(column=0, row=0)

        # Label inside the Frame 
        self.InputLabel = tk.CTkLabel(self.DataInputFrame, text="5", fg_color=self.buttonColor, text_color="white", font=self.parent.font)

        self.InputLabel.grid()
        self.InputLabel.grid_configure(column=1, row=0, padx=40)

        # Right Button inside the Frame
        self.rightButton = tk.CTkButton(self.DataInputFrame, image=self.right_button_image, command= RightButtonClick, border_width=0, text='', height=self.buttonHeight, width=self.buttonWidth, fg_color= self.buttonColor, corner_radius=0, hover=False)

        self.rightButton.grid()
        self.rightButton.grid_configure(column=2,row=0)
   
    # Setup the data field list 
    def SetupListDataField(self):
        self.frame_point = tk.CTkFrame(self.parent, fg_color="#384764")

        self.frame_point.pack()
        self.frame_point.pack_configure(pady=(20,50), anchor="center")

        self.update_entry_fields()
class OutputFrame(tk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent, width=1, fg_color="#191E23")
        self.pack()        
        self.pack_configure(side="right",
        fill="both",expand=True, anchor="n")

        self.fontTime = tk.CTkFont(family="Courier New",size=20, weight="bold")
        self.fontTitle = tk.CTkFont(family="Courier New", weight="bold", underline=True, size=48, slant="italic")
        self.setupOutputTitle()
        self.setupOutputCanvas()
        self.setupTime()

    def setupOutputTitle(self):
        self.OutputTitle = tk.CTkLabel(self,text="BEZIER CURVE SIMULATION", text_color="white",font = self.fontTitle)
        self.OutputTitle.pack()
        self.OutputTitle.pack_configure(anchor='n', padx=15)

    def setupOutputCanvas(self):
        self.canvas = tk.CTkCanvas(self, height=800)
        self.canvas.pack()
        self.canvas.pack_configure(padx=10, pady=20, fill="both",expand=True, side="top")
    
    def setupTime(self):
        self.timeLabel = tk.CTkLabel(self,text="Time Execution: ",font=self.fontTime, text_color="white")
        self.timeLabel.pack()
        self.timeLabel.pack_configure(pady=(10,20),anchor='w', padx=15)

class BezierCurveDrawing(tk.CTkCanvas):
    def __init__(self):
        super().__init__()
        self.setupCanvas()
    def setupCanvas(self):
        self.canvas = tk.CTkCanvas(self,height = 800)
        self.canvas.pack()
        self.canvas.pack_configure(padx=10, pady=20, fill="both",expand=True, side="top")

        

def main():
    app = App()
    app.mainloop()



'''
import tkinter as tk
import numpy as np
import time

class BezierAnimation(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=800, height=600, bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        self.point_curve = [(200, 300.11), (150, 100), (650, 100), (700, 500)]
        self.step = 0
        self.steps = 20
        self.draw_points()
        self.lines_container = self.point_curve.copy()
        self.prev_lines = []
        
    def draw_points(self):
        points_container = None
        for i in range(len(self.point_curve)):
            x0, y0 = self.point_curve[i]
            self.create_oval(x0, y0, x0 + 10, y0 + 10, fill="blue")
            if(points_container):
                self.create_line(points_container[0] + 5,points_container[1] + 5,x0 + 5,y0 + 5,fill='blue')
            points_container = (x0,y0)

    def interpolate_line(self,p1,p2,t):
        x1= p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        return x, y        

    def bezier_curve(self, points):

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

def main():
    root = tk.Tk()
    root.title("Bezier Animation")

    canvas = BezierAnimation(root)
    canvas.bezier_curve(canvas.point_curve)
    root.mainloop()

if __name__ == "__main__":
    main()

'''