import re
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def clean_equation(text):
    """Convert common school-style equation input into SymPy-friendly syntax."""
    text = text.strip().lower()
   
    text = text.replace("^", "**")
    text = text.replace(" ", "")

    # 2x -> 2*x, -x -> -1*x, 3(x+1) -> 3*(x+1)
    text = re.sub(r'(?<=\d)(?=x|y)', '*', text)
    text = re.sub(r'(?<=\d)(?=\()', '*', text)
    text = re.sub(r'(?<=[xy])(?=\()', '*', text)

    # x -> 1*x and y -> 1*y where needed
    text = re.sub(r'(?<![A-Za-z0-9_*])x', '1*x', text)
    text = re.sub(r'(?<![A-Za-z0-9_*])y', '1*y', text)
    text = re.sub(r'(?<![A-Za-z0-9_*])\-x', '-1*x', text)
    text = re.sub(r'(?<![A-Za-z0-9_*])\-y', '-1*y', text)

    return text


def parse_equation(text):
    """Return a SymPy expression equal to zero."""
    cleaned = clean_equation(text)

    if "=" in cleaned:
        left, right = cleaned.split("=", 1)
        expression = sp.sympify(left) - sp.sympify(right)
    else:
        expression = sp.sympify(cleaned)

    return sp.expand(expression)


def get_coefficients(expr):
    """For ax + by + c = 0, return a, b, c."""
    x, y = sp.symbols("x y")
    poly = sp.Poly(expr, x, y)

    a = poly.coeff_monomial(x)
    b = poly.coeff_monomial(y)
    c = poly.coeff_monomial(1)

    # Reject non-linear equations.
    if sp.Poly(expr, x, y).total_degree() > 1:
        raise ValueError("Only linear equations in x and y are supported.")

    if a == 0 and b == 0:
        raise ValueError("This is not a valid linear equation in x and y.")

    return float(a), float(b), float(c)


def equation_name(a, b, c):
    return f"{a:g}x + {b:g}y + {c:g} = 0"


def intercepts(a, b, c):
    x_int = None
    y_int = None

    # y = 0 -> ax + c = 0
    if a != 0:
        x_int = -c / a

    # x = 0 -> by + c = 0
    if b != 0:
        y_int = -c / b

    return x_int, y_int


def classify_pair(a1, b1, c1, a2, b2, c2):
    """
    For:
        a1*x + b1*y + c1 = 0
        a2*x + b2*y + c2 = 0

    Returns:
        unique -> one solution
        none   -> no solution
        infinite -> infinitely many solutions
    """
    determinant = a1 * b2 - a2 * b1

    if abs(determinant) > 1e-10:
        return "unique"

    # Parallel/coincident test.
    if abs(a1 * b2 - a2 * b1) < 1e-10:
        if abs(a1 * c2 - a2 * c1) < 1e-10 and abs(b1 * c2 - b2 * c1) < 1e-10:
            return "infinite"
        return "none"

    return "none"


def solve_intersection(a1, b1, c1, a2, b2, c2):
    det = a1 * b2 - a2 * b1

    if abs(det) < 1e-10:
        return None

    # Cramer's rule for ax + by + c = 0
    x_val = (b1 * c2 - b2 * c1) / det
    y_val = (c1 * a2 - c2 * a1) / det

    return x_val, y_val


def choose_range(intersection, all_intercepts):
    """Choose a useful graph range automatically."""
    values = [abs(v) for v in all_intercepts if v is not None]

    if intersection:
        values.extend([abs(intersection[0]), abs(intersection[1])])

    largest = max(values, default=5)
    limit = max(5, np.ceil(largest * 1.35))

    # Keep the graph readable for normal Class 10 examples.
    limit = min(max(limit, 5), 50)
    return float(limit)


def plot_graph(eq1_text, eq2_text):
    x, y = sp.symbols("x y")

    expr1 = parse_equation(eq1_text)
    expr2 = parse_equation(eq2_text)

    a1, b1, c1 = get_coefficients(expr1)
    a2, b2, c2 = get_coefficients(expr2)

    result = classify_pair(a1, b1, c1, a2, b2, c2)
    intersection = solve_intersection(a1, b1, c1, a2, b2, c2)

    xint1, yint1 = intercepts(a1, b1, c1)
    xint2, yint2 = intercepts(a2, b2, c2)

    all_intercepts = [xint1, yint1, xint2, yint2]
    limit = choose_range(intersection, all_intercepts)

    xs = np.linspace(-limit, limit, 1000)

    def y_values(a, b, c):
        if abs(b) < 1e-12:
            return None
        return -(a * xs + c) / b

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot equation 1
    if abs(b1) < 1e-12:
        x_const = -c1 / a1
        ax.axvline(x_const, linewidth=2.5, label=eq1_text)
    else:
        ax.plot(xs, y_values(a1, b1, c1), linewidth=2.5, label=eq1_text)

    # Plot equation 2
    if abs(b2) < 1e-12:
        x_const = -c2 / a2
        ax.axvline(x_const, linewidth=2.5, label=eq2_text)
    else:
        ax.plot(xs, y_values(a2, b2, c2), linewidth=2.5, label=eq2_text)

    # Mark intercepts
    if xint1 is not None and abs(xint1) <= limit:
        ax.scatter(xint1, 0, s=55, zorder=5)
        ax.annotate(f"({xint1:.2f}, 0)", (xint1, 0), xytext=(6, 8),
                    textcoords="offset points")

    if yint1 is not None and abs(yint1) <= limit:
        ax.scatter(0, yint1, s=55, zorder=5)
        ax.annotate(f"(0, {yint1:.2f})", (0, yint1), xytext=(6, 8),
                    textcoords="offset points")

    if xint2 is not None and abs(xint2) <= limit:
        ax.scatter(xint2, 0, s=55, zorder=5)
        ax.annotate(f"({xint2:.2f}, 0)", (xint2, 0), xytext=(6, -18),
                    textcoords="offset points")

    if yint2 is not None and abs(yint2) <= limit:
        ax.scatter(0, yint2, s=55, zorder=5)
        ax.annotate(f"(0, {yint2:.2f})", (0, yint2), xytext=(6, -18),
                    textcoords="offset points")

    # Mark solution/intersection
    if result == "unique" and intersection:
        ix, iy = intersection
        ax.scatter(ix, iy, s=130, marker="o", zorder=10, label=f"Solution ({ix:.2f}, {iy:.2f})")
        ax.annotate(
            f"  Solution = ({ix:.2f}, {iy:.2f})",
            (ix, iy),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=11,
            fontweight="bold"
        )

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, linestyle="--", alpha=0.45)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")

    if result == "unique":
        title = "Pair of Linear Equations — One Solution (Intersecting Lines)"
    elif result == "none":
        title = "Pair of Linear Equations — No Solution (Parallel Lines)"
    else:
        title = "Pair of Linear Equations — Infinitely Many Solutions (Coincident Lines)"

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.show()

    # Terminal result
    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Equation 1: {equation_name(a1, b1, c1)}")
    print(f"Equation 2: {equation_name(a2, b2, c2)}")

    print("\nIntercepts:")
    print(f"  Eq 1: x-intercept = {xint1}, y-intercept = {yint1}")
    print(f"  Eq 2: x-intercept = {xint2}, y-intercept = {yint2}")

    if result == "unique":
        print(f"\n✓ One solution: ({intersection[0]:.4f}, {intersection[1]:.4f})")
        print("  Graph meaning: the two lines intersect at one point.")
    elif result == "none":
        print("\n✗ No solution.")
        print("  Graph meaning: the two lines are parallel and never meet.")
    else:
        print("\n∞ Infinitely many solutions.")
        print("  Graph meaning: both equations represent the same line.")

    print("=" * 60)


def main():
    print("\n" + "=" * 60)
    print("  CLASS 10 MATHS — LINEAR EQUATION GRAPH PLOTTER")
    print("=" * 60)
    print("Example input:")
    print("  2x + 3y = 6")
    print("  x - y = 2")
    print("  3x + 4y - 12 = 0")
    print("\nTip: Use x and y as variables.\n")

    while True:
        try:
            eq1 = input("Enter Equation 1: ")
            eq2 = input("Enter Equation 2: ")

            plot_graph(eq1, eq2)

        except Exception as error:
            print(f"\nERROR: {error}")
            print("Please enter a valid linear equation, for example: 2x + 3y = 6")

        again = input("\nDo you want to try another pair? (y/n): ").strip().lower()
        if again != "y":
            print("\nGood luck with your Maths exam! 💪")
            break


if __name__ == "__main__":
    main()