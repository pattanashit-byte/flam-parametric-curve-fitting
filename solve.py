import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution


# ============================================================
# 1. Load the dataset
# ============================================================

data = pd.read_csv("xy_data.csv")

x_actual = data["x"].to_numpy()
y_actual = data["y"].to_numpy()

# Number of points in the dataset
n = len(data)

# The assignment gives the range 6 < t < 60.
# We assume the CSV points are uniformly sampled over this range.
t = np.linspace(6, 60, n)


# ============================================================
# 2. Define the parametric curve
# ============================================================

def generate_curve(params):
    """
    Generate x(t) and y(t) for a given set of parameters.

    params:
        theta -> angle in degrees
        M     -> exponential parameter
        X     -> horizontal translation
    """

    theta, M, X = params

    # Convert theta from degrees to radians
    theta_rad = np.radians(theta)

    # Exponential oscillation term
    exponential = np.exp(M * np.abs(t))
    oscillation = np.sin(0.3 * t)

    # Parametric equations
    x_pred = (
        t * np.cos(theta_rad)
        - exponential * oscillation * np.sin(theta_rad)
        + X
    )

    y_pred = (
        42
        + t * np.sin(theta_rad)
        + exponential * oscillation * np.cos(theta_rad)
    )

    return x_pred, y_pred


# ============================================================
# 3. Define the L1 objective function
# ============================================================

def objective(params):
    """
    Calculate the total L1 distance between
    actual and predicted points.
    """

    x_pred, y_pred = generate_curve(params)

    # L1 distance:
    # |x_actual - x_pred| + |y_actual - y_pred|
    l1_error = np.sum(
        np.abs(x_actual - x_pred)
        + np.abs(y_actual - y_pred)
    )

    return l1_error


# ============================================================
# 4. Define parameter bounds
# ============================================================

bounds = [
    (0.000001, 49.999999),    # theta: 0 < theta < 50 degrees
    (-0.049999, 0.049999),    # M: -0.05 < M < 0.05
    (0.000001, 99.999999)     # X: 0 < X < 100
]


# ============================================================
# 5. Optimize theta, M and X
# ============================================================

print("Starting optimization...")
print("Number of data points:", n)
print()

result = differential_evolution(
    objective,
    bounds,
    strategy="best1bin",
    maxiter=2000,
    popsize=20,
    tol=1e-10,
    mutation=(0.5, 1.0),
    recombination=0.7,
    seed=42,
    polish=True,
    workers=1
)


# ============================================================
# 6. Extract optimized parameters
# ============================================================

theta, M, X = result.x

final_l1 = result.fun

theta_rad = np.radians(theta)


# ============================================================
# 7. Generate final fitted curve
# ============================================================

x_pred, y_pred = generate_curve(result.x)


# ============================================================
# 8. Calculate additional error measurements
# ============================================================

point_l1 = (
    np.abs(x_actual - x_pred)
    + np.abs(y_actual - y_pred)
)

mean_l1 = np.mean(point_l1)
max_l1 = np.max(point_l1)


# ============================================================
# 9. Print results
# ============================================================

print("=" * 60)
print("OPTIMIZATION RESULT")
print("=" * 60)

print(f"Theta      : {theta:.10f} degrees")
print(f"Theta      : {theta_rad:.10f} radians")
print(f"M          : {M:.10f}")
print(f"X          : {X:.10f}")
print()

print(f"Total L1   : {final_l1:.10f}")
print(f"Mean L1    : {mean_l1:.10f}")
print(f"Maximum L1 : {max_l1:.10f}")

print()
print("Optimizer success:", result.success)
print("Optimizer message:", result.message)


# ============================================================
# 10. Create Desmos / LaTeX submission equation
# ============================================================

desmos_string = (
    f"\\left("
    f"t*\\cos({theta_rad:.6f})"
    f"-e^{{{M:.6f}\\left|t\\right|}}"
    f"\\cdot\\sin(0.3t)"
    f"\\sin({theta_rad:.6f})"
    f"+{X:.6f},"
    f"42+t*\\sin({theta_rad:.6f})"
    f"+e^{{{M:.6f}\\left|t\\right|}}"
    f"\\cdot\\sin(0.3t)"
    f"\\cos({theta_rad:.6f})"
    f"\\right)"
)

print()
print("=" * 60)
print("DESMOS / LATEX SUBMISSION")
print("=" * 60)
print(desmos_string)


# ============================================================
# 11. Save the results
# ============================================================

with open("submission.txt", "w") as file:

    file.write("FLAM SDE/R&D Internship - Parametric Curve Fitting\n")
    file.write("=" * 60 + "\n\n")

    file.write(f"Theta (degrees) : {theta:.10f}\n")
    file.write(f"Theta (radians) : {theta_rad:.10f}\n")
    file.write(f"M               : {M:.10f}\n")
    file.write(f"X               : {X:.10f}\n\n")

    file.write(f"Total L1        : {final_l1:.10f}\n")
    file.write(f"Mean L1         : {mean_l1:.10f}\n")
    file.write(f"Maximum L1      : {max_l1:.10f}\n\n")

    file.write("Desmos / LaTeX equation:\n")
    file.write(desmos_string + "\n")


# ============================================================
# 12. Plot actual data vs fitted curve
# ============================================================

plt.figure(figsize=(10, 7))

plt.scatter(
    x_actual,
    y_actual,
    s=15,
    label="Actual data"
)

plt.plot(
    x_pred,
    y_pred,
    linewidth=2,
    label="Fitted curve"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("FLAM Parametric Curve Fitting")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "fit_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print()
print("Results saved to:")
print("  submission.txt")
print("  fit_plot.png")