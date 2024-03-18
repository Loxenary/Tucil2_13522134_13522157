import matplotlib.pyplot as plt
import numpy as np
import time

from bruteforce import BezierCurve

bezier = BezierCurve()

# Masukkan banyaknya titik kontrol
while True:
    n = int(input("Masukkan banyak titik kontrol: "))
    if n != 3:
        print("Error: Minimum 3 control points required.")
    else:
        break

# Masukkan titik kontrol sesuai dengan jumlah yang dimasukkan sebelumnya
control_points = []
for i in range(n):
    x = float(input(f"Masukkan koordinat x titik kontrol ke-{i+1}: "))
    y = float(input(f"Masukkan koordinat y titik kontrol ke-{i+1}: "))
    control_points.append((x, y))

while True:
    iterations = int(input("Masukkan jumlah iterasi: "))
    if iterations < 1:
        print("Error: Minimum 3 control points required.")
    else:
        break

start_time = time.time()
bezier.make_bezier(*control_points, iterations=iterations)
end_time = time.time()

print("Waktu eksekusi:", end_time - start_time, "detik")
bezier.plot_curve()
