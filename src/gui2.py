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
        self.pack_configure(side="left",fill="both")
        self.setupScrollableContainer()
        self.container = InputContainer(self.scrollable_frame)
    def setupScrollableContainer(self):
        def on_canvas_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def on_mousewheel(event):
            self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

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

        self.canvas.bind_all("<MouseWheel>",on_mousewheel)
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
        self.label_iteration = tk.CTkLabel(self, text="Input Dots", font=self.font, text_color=self.default_text_color, anchor="w")
        

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
    def setupPointsField(self):
        self.inputField = InputFieldDots(self)
    def setupButton(self):
        self.data_x = self.inputField.entry_x
        self.data_y = self.inputField.entry_y
        def isIterationEmpty():
            current_text = self.entry_iteration.get()
            return current_text == "" or current_text == self.entryplaceholder
        def isBlankOnData():

            length_entry = len(self.data_x)
            for i in range(length_entry):
                if(self.data_x[i].get() == "X" or self.data_y[i].get() == "Y"):
                    return True
            return False
        def DataSave():
            self.data_path = os.path.join(os.path.dirname(__file__),"data.txt")
            if(isIterationEmpty()):
                messagebox.showwarning("Iteration Blank","Please fill the Input Iteration Field")
                return
            if(isBlankOnData()):
                messagebox.showwarning("Field Blank","Please Fill all the Input Dots")
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

    def ButtonPreparation(self):
        button_image_path = os.path.join(os.path.dirname(__file__), "Assets","triangle.png")
        button_image = Image.open(button_image_path)

        self.left_button_image = button_image.rotate(90)
        self.right_button_image = button_image.rotate(-90)
        
        self.left_button_image = tk.CTkImage(self.left_button_image,size=(self.buttonPhoto_x,self.buttonPhoto_y))

        self.right_button_image = tk.CTkImage(self.right_button_image,size=(self.buttonPhoto_x,self.buttonPhoto_y))

    def validate_num_points(self,action,value_if_allowed):
            if not value_if_allowed:  # Allow if the entry is empty
                return True
            if value_if_allowed == 'X' or value_if_allowed == 'Y':
                return True
            if action == '1':  # Insert action
                if value_if_allowed.isdigit():
                    return True   
                elif value_if_allowed.startswith('-') and value_if_allowed[1:].isdigit():
                    return True
                return False
            return True

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
    def SetupListDataField(self):
        self.frame_point = tk.CTkFrame(self.parent, fg_color="#384764")

        self.frame_point.pack()
        self.frame_point.pack_configure(pady=(20,50), anchor="center")

        self.update_entry_fields()

class OutputFrame(tk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent, width=1, fg_color="#191E23")
        self.pack()
        self.pack_configure(side="right",fill="both",expand=True)
        self.setupOutputTitle()

    def setupOutputTitle(self):
        self.OutputTitle = tk.CTkLabel(self,text="BEZIER CURVE SIMULATION", text_color="white",font=("Helvaica",48))
        self.OutputTitle.pack()


def main():
    app = App()
    app.mainloop()