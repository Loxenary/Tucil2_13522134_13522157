# File to save data related to passing between Frame in the GUI.py
from typing import List, Tuple, Union

class Database:
    max_control_points = 20
    control_points: List[Tuple[float, float]] = []
    iterations: int = 0
    selected_points: int = 0

    apps_height: float = None
    apps_width: float = None
    animation_speed: float = None

    is_Button_clicked: bool = False

    data_algorithm: str = None
    time_Execution: float = 0

    max_x: float = None
    max_y: float = None
    min_x: float = None
    min_y: float = None

    origin_points: List[Tuple[float, float]] = []

    is_animated: bool = False # Used to handle button if the animation is still running

    @staticmethod 
    def set_minmax():
        Database.max_x = max(Database.control_points, key=lambda point: point[0])[0]
        Database.max_y = max(Database.control_points, key=lambda point: point[1])[1]
        Database.min_x = min(Database.control_points, key=lambda point: point[0])[0]
        Database.min_y = min(Database.control_points, key=lambda point: point[1])[1]
        

    @staticmethod
    def handle_negatives_data():
        # Handle negative X values
        temp = Database.control_points.copy()
        Database.origin_points = temp

        additional_x = Database.apps_width - Database.max_x
        additional_y = Database.apps_height - Database.max_y

        if(additional_x > Database.apps_width or additional_y > Database.apps_height):
            Database.control_points.clear()
            print("test:", additional_x,"y: ", additional_y)
        
        # Handle any negative x values
        if(additional_x > Database.apps_width and additional_y > Database.apps_height):
            for i in range(len(temp)):
                Database.control_points.append((temp[i][0] + additional_x, temp[i][1] + additional_y))
        elif(additional_x > Database.apps_width):
            for i in range(len(temp)):
                Database.control_points.append((temp[i][0] + additional_x, temp[i][1]))
        elif(additional_y > Database.apps_height):
            for i in range(len(temp)):
                Database.control_points.append((temp[i][0], temp[i][1] + additional_y))    
    


    def handle_points_scaling():

        max_y = max(Database.origin_points, key=lambda point: point[1])[1]
        min_y = min(Database.origin_points, key=lambda point: point[1])[1]

        temp_normalize_y = [(y - min_y) / (max_y - min_y) for _, y in Database.origin_points]

        min_x = min(Database.control_points, key=lambda point: point[0])[0]
        max_x = max(Database.control_points, key=lambda point: point[0])[0]

        temp_normalize_x = [(x - min_x) / (max_x - min_x)  for x, _ in Database.control_points]

        
        print("Temp y: ",temp_normalize_y)
    
        print("Temp x: ",temp_normalize_x)

        # set padding for max values
        print("Height:",Database.apps_height)
        print("Width:",Database.apps_width)
        
        offset_x_left = 200
        offset_y_bottom = 200
        offset_x_rigth = Database.apps_width - (offset_x_left * 2)
        offset_y_top = Database.apps_height - (offset_y_bottom * 2)
        print("Ofset: ",offset_x_rigth)
        
        for i in temp_normalize_y:
            print("Data: ", (Database.apps_height - ((i* offset_y_top) +offset_y_bottom)))


        temp_scaled_up = [((x * offset_x_rigth) + offset_x_left , (Database.apps_height - ((y * offset_y_top) +offset_y_bottom))) for x, y in zip(temp_normalize_x, temp_normalize_y)]

        Database.print_control_points()
        Database.control_points = temp_scaled_up
        Database.set_minmax()
        Database.handle_negatives_data()

        # scale_factor = 0.5
        # width = Database.apps_width
        # height = Database.apps_height

        # x_range = abs(Database.max_x - Database.min_x)
        # y_range = abs(Database.max_y - Database.min_y)

        # print("width: " + str(width) + " height: " + str(height))
        # x_scale = width / x_range
        # y_scale = height / y_range
        
        # scale = min(x_scale,y_scale) * scale_factor

        # x_add = 0; y_add = 0
        # if(x_scale <= y_scale):
        #     x_add = 100
        # else:
        #     y_add = 100
        # Database.control_points = [((scale * (x - Database.min_x) )+ x_add, (scale * (y - Database.min_y)) + y_add) for x,y in Database.control_points]

    def handle_points_flipped(canvas_height):
        temp = [(x,canvas_height - y) for x,y in Database.control_points]
        print("height: ",canvas_height)
        Database.control_points = temp

    @staticmethod
    def handle_control_points(canvas_height, canvas_width):
        print("Previously: ")
        Database.print_control_points()
        
        Database.handle_negatives_data()
        Database.set_apps_height(canvas_height)
        Database.set_minmax()
        Database.handle_points_flipped(Database.apps_height)

        Database.set_apps_width(canvas_width)
        
        Database.set_minmax()
        print("================================================================")
        print("Handle scaling: ")
        Database.handle_points_scaling()
        return Database.control_points

    @staticmethod 
    def set_control_points(control_points):
        for i in range(len(control_points)):
            Database.control_points[i] = float(control_points[i])

    @staticmethod
    def set_apps_height(apps_height):
        Database.apps_height = float(apps_height)

    @staticmethod
    def set_apps_width(apps_width):
        Database.apps_width = float(apps_width)

    @staticmethod
    def set_control_points_from_idx(control_points):
        x, y = control_points
        Database.control_points.append((float(x), float(y)))

    @staticmethod
    def set_selected_points(selected_points):
        Database.selected_points = int(selected_points)

    @staticmethod    
    def get_selected_control_points():
        control_points = []
        for i in range(Database.selected_points):
            control_points.append(Database.control_points[i])
        return control_points

    @staticmethod
    def get_iteration():
        return int(Database.iterations)

    @staticmethod
    def set_animation_speed(animation_speed):
        Database.animation_speed = float(animation_speed)

    @staticmethod
    def set_iterations(iteration):
        Database.iterations = int(iteration)

    @staticmethod 
    def print_control_points():
        print("Point Control : ")
        for i in range(len(Database.control_points)):
            print(f'{i+1}: x: {Database.control_points[i][0]} y: {Database.control_points[i][1]}')

    @staticmethod
    def clear_all_function_data():
        Database.is_Button_clicked = False
        Database.data_algorithm = None
    
    @staticmethod
    def clear_all_data():
        Database.control_points = []
        Database.iterations = 0
        Database.selected_points = 0
        Database.is_Button_clicked = False
        Database.data_algorithm = None
        Database.time_Execution = 0

    @staticmethod
    def get_time_execution():
        return "{:.3f}".format(Database.time_Execution)
    
    @staticmethod
    def set_time_execution(time_execution):
        Database.time_Execution = time_execution