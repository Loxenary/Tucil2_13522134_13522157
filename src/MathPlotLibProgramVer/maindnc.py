from beziercurve import BezierCurve
import time

def input_control_points():
    # Meminta input dari pengguna untuk titik kontrol
    control_points = []
    while True:
        n = int(input("Masukkan banyak titik control points: "))
        if n < 3:
            print("Error: Minimum 3 control points required.")
        else:
            break
    for i in range(n):
        x = float(input(f"Masukkan koordinat x untuk control point {i+1}: "))
        y = float(input(f"Masukkan koordinat y untuk control point {i+1}: "))
        control_points.append((x, y))
    return control_points

def main():
    bezier = BezierCurve()
    
    # Meminta input titik kontrol dan jumlah iterasi
    control_points = input_control_points()
    iterations = int(input("Masukkan jumlah iterasi: "))
    
    start_time = time.time()
    # Menghasilkan kurva Bezier
    bezier.make_bezier(*control_points, iterations=iterations)
    end_time = time.time()
    print("Curve Points : ",bezier.curve_points)
    
    # Menghitung dan mencetak waktu yang dibutuhkan untuk pembuatan kurva
    print("Time execution:", end_time - start_time, "seconds")
    
    # Menampilkan kurva Bezier
    bezier.plot_curve()

if __name__ == "__main__":
    main()
