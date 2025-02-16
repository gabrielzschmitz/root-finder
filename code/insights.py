import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("results.csv")

# Calculate average computation time and iterations for each method
avg_comp_time = data.groupby("method")["comp_time"].mean()
avg_iterations = data.groupby("method")["iterations"].mean()

# Calculate the accuracy of the roots (assuming the true root is pi)
true_root = 3.141592653589793
data["relative_error"] = abs(data["root"] - true_root) / abs(true_root)
avg_relative_error = data.groupby("method")["relative_error"].mean()

# Print the results with method names
print("Average Computation Time:")
for method, time in avg_comp_time.items():
    print(f"{method}: {time:.6f} seconds")
print("\nAverage Iterations:")
for method, iterations in avg_iterations.items():
    print(f"{method}: {iterations:.0f} iterations")
print("\nAverage Relative Error:")
for method, error in avg_relative_error.items():
    print(f"{method}: {error:.6e}")

# Reset the index to remove the "method" label
avg_comp_time = avg_comp_time.reset_index(drop=True)
avg_iterations = avg_iterations.reset_index(drop=True)
avg_relative_error = avg_relative_error.reset_index(drop=True)

# Plotting the results
plt.figure(figsize=(14, 6))

# Plot average computation time
plt.subplot(1, 3, 1)
avg_comp_time.plot(kind="bar", color="skyblue")
plt.title("Tempo de Computação Médio")
plt.ylabel("Tempo (s)")
plt.xticks(
    range(len(avg_comp_time)),
    ["Bisection", "False Position", "Fixed Point", "Newton Raphson", "Secant"],
    rotation=45,
)

# Plot iterations
plt.subplot(1, 3, 2)
avg_iterations.plot(kind="bar", color="lightgreen")
plt.title("Número de Iterações")
plt.ylabel("Iterações")
plt.xticks(
    range(len(avg_iterations)),
    ["Bisection", "False Position", "Fixed Point", "Newton Raphson", "Secant"],
    rotation=45,
)

# Plot average relative error with a logarithmic y-axis
plt.subplot(1, 3, 3)
avg_relative_error.plot(kind="bar", color="salmon", logy=True)
plt.title("Erro Relativo")
plt.ylabel("Erro Relativo")
plt.xticks(
    range(len(avg_relative_error)),
    ["Bisection", "False Position", "Fixed Point", "Newton Raphson", "Secant"],
    rotation=45,
)

plt.tight_layout()
plt.show()
