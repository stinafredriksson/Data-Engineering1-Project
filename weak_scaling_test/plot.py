import matplotlib.pyplot as plt
import numpy as np

load_time = [75.1, 150, 103.44, 130.8, 131.76, 123.62, 155.32]
cores = [16, 2, 14, 10, 4, 8, 6]
analyse_time = [473.9, 2538.4, 467.45, 540.76, 1357, 651.23, 1174.25]

load_time_coefficients = np.polyfit(cores, load_time, 1)
load_time_polynomial = np.poly1d(load_time_coefficients)

analyse_time_coefficients = np.polyfit(cores, analyse_time, 2)
analyse_time_polynomial = np.poly1d(analyse_time_coefficients)

x_values = np.linspace(min(cores), max(cores), 100)
load_time_y_values = load_time_polynomial(x_values)
analyse_time_y_values = analyse_time_polynomial(x_values)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
plt.scatter(cores, load_time, label='Load Time Data')
plt.plot(x_values, load_time_y_values, color='red', label='Fitted Line')
plt.xlabel('Cores')
plt.ylabel('Load Time')
plt.title('Load Time vs. Cores')
plt.legend()

plt.subplot(1, 2, 2) 
plt.scatter(cores, analyse_time, label='Analyse Time Data')
plt.plot(x_values, analyse_time_y_values, color='red', label='Fitted Quadratic Curve')
plt.xlabel('Cores')
plt.ylabel('Analyse Time')
plt.title('Analyse Time vs. Cores (Non-Linear Fit)')
plt.legend()

plt.tight_layout()
plt.show()

