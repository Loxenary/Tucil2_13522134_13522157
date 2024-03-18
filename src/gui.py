import customtkinter as tk
from tkinter import messagebox
import os
from PIL import Image
from GlobalData import Database as db
import BezierAlgorithm as bz

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x850")
        self.setupFrame()
        db.clear_all_data()

    def setupFrame(self):
        self.InputFrame = InputFrame(self,self.setupOutputCanvas)
        self.OutputFrame = OutputFrame(self)
        
    # called only when a funciton button is pressed
    def setupOutputCanvas(self):
        db.is_Button_clicked = True
        if(not db.is_animated):
            self.OutputFrame.destroy()
            self.OutputFrame = OutputFrame(self)
            self.OutputFrame.setupTimeExecution()
class InputFrame(tk.CTkFrame):
    def __init__(self, parent, callbackFunction):
        super().__init__(master=parent,corner_radius=0)
        self.pack()
        self.parent = parent
        self.pack_configure(side="left",fill="both")
        self.setupScrollableContainer()
        self.container = InputContainer(self.scrollable_frame,callbackFunction)
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
    def __init__(self,parent,callbackFunction):
        super().__init__(master=parent, corner_radius=0, border_width=0, border_color="#D9D9D9", fg_color="#384764")
        self.pack()
        self.pack_configure(fill="x",expand=True)
        self.font = tk.CTkFont(family="Courier New",size =20)
        self.entryplaceholder = "Max 500"
        self.default_text_color = "white"

        self.callbackFunction = callbackFunction

        self.algorithm = None

        # Call Setup Field
        self.setupIterationField()
        self.setupPointsField()
        self.setupAnimationSpeedEntry()
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
        self.label_iteration = tk.CTkLabel(self, text="Input Iterations", font=self.font, text_color=self.default_text_color, anchor="w")
        

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
    def setupAnimationSpeedEntry(self):
        def validate_iteration(action, value_if_allowed):
            if not value_if_allowed: 
                return True
            if(action == '1'):
                if value_if_allowed.isdigit() and int(value_if_allowed) <= 500:
                    return True
                return False
            return True
        validate_input = (self.register(validate_iteration), '%d','%P')
        # Label
        self.label_speed = tk.CTkLabel(self, text="Animation Duration", font=self.font, text_color=self.default_text_color, anchor="w")
    
        self.label_speed.pack()
        self.label_speed.pack_configure(padx=(50,50), pady=(40,30))
        # Entry

        self.entry_speed = tk.CTkEntry(self, width=172,height=44, border_width=1, border_color="#5B5B5B",corner_radius=2, font=("georgia",20),text_color="#AEAEAE",validate="key", validatecommand=validate_input)

        self.entry_speed.insert(0, "40")
        self.entry_speed.configure(fg_color="#D9D9D9",text_color="black")

        self.entry_speed.configure(justify="center")
        self.entry_speed.pack()
        self.entry_speed.pack_configure(padx=(50,50), pady=(0,40),anchor="center")
    # Setup the Point input field components
    def setupPointsField(self):
        self.inputField = InputFieldDots(self)
    
    def save_animation_Data(self):
        db.set_animation_speed(self.entry_speed.get())

    # Setup the main functioning button
    def setupButton(self):
        self.data_x = self.inputField.entry_x
        self.data_y = self.inputField.entry_y
        
        # Check is the Data for iteration is Empty or not
        def isIterationValid():
            current_text = self.entry_iteration.get()
            return (current_text == "" or current_text == self.entryplaceholder or (not current_text.isdigit()))
        def isBlankOnData():
            length_entry = int(self.inputField.InputLabel.cget("text"))
            for i in range(length_entry):
                data_x = self.data_x[i].get()
                data_y = self.data_y[i].get()
                if(data_x[0] == '-' and data_x[1:].isdigit()):
                    continue
                if(data_y[0] == '-' and data_y[1:].isdigit()):
                    continue
                if(data_x == "X" or data_y == "Y" or (not data_x.isdigit()) or (not data_y.isdigit())):
                    return True
                
                
            return False
    
        
        def DataSave(algorithm):
            db.clear_all_data()
            # self.data_path = os.path.join(os.path.dirname(__file__),"data.txt")
            if(isIterationValid()):
                messagebox.showwarning("Iteration InValid","Please fill the Iteration Field or Re-input the valid data for the iteration")
                return
            if(isBlankOnData()):
                messagebox.showwarning("Field Data Invalid","Please Fill all the Input Dots or Re-input the valid data for the data field")
                return
            
            data_length = int(self.inputField.InputLabel.cget("text"))
            for i in range(data_length):               
                db.set_control_points_from_idx((self.data_x[i].get(),self.data_y[i].get()))
            db.set_selected_points(data_length)

            db.set_iterations(self.entry_iteration.get())
            db.data_algorithm = algorithm
            db.animation_speed = int(self.entry_speed.get())
            self.callbackFunction()
            

        def BruteForceCallout():
            data_length = int(self.inputField.InputLabel.cget("text"))
            if(data_length == 3):
                DataSave("BruteForce")
            else:
                messagebox.showwarning("Cannot Use Bruteforce","Sorry, We didn't implement bruteforce for more than 3 control points")
            #TODO: Implement Bruteforce funcion on Bezier Curve

        def DecreaseAndConquerCallout():
            DataSave("DNC")            
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
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
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
                # Update any data new or not into database

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
        self.LabelData = tk.CTkLabel(self.parent, text="Control Points",font=self.parent.font, text_color="white",anchor="w")
        self.LabelData.pack()
        self.LabelData.pack_configure(pady=(0,30))

        # Frame for Input Data
        self.DataInputFrame = tk.CTkFrame(self.parent,fg_color=self.buttonColor)
        self.DataInputFrame.pack()
        
        # Left button 
        self.leftbutton = tk.CTkButton(self.DataInputFrame,image=self.left_button_image,command=LeftButtonClick, border_width=0, text="", height= self.buttonHeight,width=self.buttonWidth,fg_color=self.buttonColor,corner_radius=0,hover=False,state="disabled")
        self.leftbutton.grid()
        self.leftbutton.grid_configure(column=0, row=0)

        # Label inside the Frame 
        self.InputLabel = tk.CTkLabel(self.DataInputFrame, text="3", fg_color=self.buttonColor, text_color="white", font=self.parent.font)

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

        self.canvas = None
        self.setupOutputTitle()
        self.setupOutputCanvas()
        self.setupTime()

    def setupOutputTitle(self):
        self.OutputTitle = tk.CTkLabel(self,text="BEZIER CURVE SIMULATION", text_color="white",font = self.fontTitle)
        self.OutputTitle.pack()
        self.OutputTitle.pack_configure(anchor='n', padx=15)

    def setupTimeExecution(self):
        self.timeLabel.configure(text= f'Time Execution: {db.get_time_execution()}')

    def on_canvas_scroll(self,event):
    # Perform scroll operation
        self.canvas.yview_scroll(-1 * event.delta, "units")
    def on_canvas_scale(self,event):
    # Perform scale operation
        if event.delta > 0:
            scale_factor = 1.1  # Zoom in
        else:
            scale_factor = 0.9  # Zoom out
        self.canvas.scale("all", event.x, event.y, scale_factor, scale_factor)

    def on_canvas_drag_Start(self,event):
        self.canvas.scan_mark(event.x, event.y)
    
    def on_canvas_drag_motion(self,event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def setupOutputCanvas(self):
        def setup_grid_coordinate():
            def get_normalized_numeration(bin_x, bin_y):
                ranges_x = db.max_x - db.min_x
                ranges_y = db.max_y - db.min_y

                iteration_x = ranges_x / bin_x
                iteration_y = ranges_y / bin_y
                
                return iteration_x, iteration_y
            def setup_border():
                x1= 100
                y1= 100
                x2 = self.canvas.winfo_width() - 100
                y2 = self.canvas.winfo_height() - 100
                self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", width=2)
                self.rectangle_height = y2-y1
                self.rectangle_width = x2-x1

            def setup_coordinate_text(bin_x, bin_y):
                iterate_x = (self.canvas.winfo_width() - 300) / bin_x
                iterate_y = (self.canvas.winfo_height() - 300) / bin_y

                iterate_val_x, iterate_val_y = get_normalized_numeration(bin_x,bin_y)
                x1 = 100
                y1 = 150 
                x2 = x1 - 8
                y2 = y1
                

                # Y coordinates
                for i in range(bin_y, -1,-1):
                    y1 = (self.canvas.winfo_height() -  (iterate_y * i+ y2))
                    if(not db.is_Button_clicked):
                        test = "" 
                        text_padding = 6
                    else:
                        if(i == bin_y):
                            test = "{:.2f}".format(db.max_y)

                        elif(i == 0):
                            test = "{:.2f}".format(db.min_y)
    
                        else:
                            test = "{:.2f}".format(db.min_y + (iterate_val_y * i))
                            
                        text_padding = 6 * len(test)
                    font_text= tk.CTkFont("Courier New",30 - (len(str(test) * 2) ),weight="bold")
                    self.canvas.create_line(x1, y1, x2, y1, width=2)
                    self.canvas.create_text(x2 - text_padding, y1, text=test,font= font_text)
                # X coordinates
                y1 = self.canvas.winfo_height() - 100
                x1 = 0
                x2 = 150
                y2 = y1 + 8
                for j in range(0, bin_x+1):
                    text_padding = 25
                    x1 = (iterate_x * j) + x2
                    test= 10 * (bin_x - j)
                
                    if(not db.is_Button_clicked):
                        test = ""
                    else:
                        if(j == 0):
                            test = "{:.2f}".format(db.min_x)
                        elif(j == bin_x):
                            test= "{:.2f}".format(db.max_x)
                        else:
                            test = "{:.2f}".format(db.min_x + (iterate_val_x * j))
                    font_text= tk.CTkFont("Courier New",22 - len(str(test)),weight="bold")
                    self.canvas.create_line(x1,y1, x1,y2, width=2)
                    self.canvas.create_text(x1, y1+ text_padding, text=test,font= font_text)
            # Setup Border Around the output
            setup_border()
            if(db.is_Button_clicked):
                setup_coordinate_text(5,8)


        scrollbar = tk.CTkScrollbar(self, orientation=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def call_bezier():
            setup_grid_coordinate()
            # height are applied inside the change_control_points function
            self.canvas.change_control_points(self.canvas.winfo_height(),self.canvas.winfo_width())
            self.canvas.setup_bezier_animation()
            self.canvas.bezier_curve()

        if db.is_Button_clicked:
            
            db.is_animated = True
            
            control_points = db.get_selected_control_points()
            iteration = db.get_iteration()

            min_x = min(control_points, key=lambda point: point[0])[0]
            max_x = max(control_points, key=lambda point: point[0])[0]
            min_y = min(control_points, key=lambda point: point[1])[1]
            max_y = max(control_points, key=lambda point: point[1])[1]

            canvas_width = max(max_x - min_x, 0) + 100
            canvas_height = max(max_y - min_y, 0) + 100


            algorithm = bz.algorithm_decider(db.data_algorithm)

            # Setup for handling negative number 
            db.set_apps_height(canvas_height - 100)
            db.set_apps_width(canvas_width - 100)
            db.set_minmax()


            if self.canvas:
                self.canvas.destroy()
            if algorithm == "DNC":
                self.canvas = bz.DNC_Algorthm(self, control_points, iteration, db.animation_speed, weight_line = 3, weight_circle=6, weight_curve=2, interpolated_weight=3)
            else:
                self.canvas = bz.BruteForce_Algorithm(self, control_points, iteration, db.animation_speed,weight_line = 3, weight_circle=6, weight_curve=2, interpolated_weihgt=3)

            self.canvas.pack_configure(padx=10, pady=20, side="top",fill='x')
            self.canvas.pack()

            self.after(100, call_bezier)
            db.is_animated = False
        else:
            self.canvas = tk.CTkCanvas(self,height=1100,width = 2000)
            self.canvas.pack()
            self.canvas.pack_configure(padx=10, pady=20, side="top")
            self.after(100,setup_grid_coordinate)
        
        self.canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.canvas.yview)
    def setupTime(self):
        self.timeLabel = tk.CTkLabel(self,text="Time Execution: ",font=self.fontTime, text_color="white")
        self.timeLabel.pack()
        self.timeLabel.pack_configure(pady=(10,20),anchor='w', padx=15)


def main():
    app = App()
    app.mainloop()