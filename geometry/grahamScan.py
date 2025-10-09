from functools import cmp_to_key
from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

Point = Tuple[float, float]

# ---------------- Helper Functions ----------------
def cross(o: Point, a: Point, b: Point) -> float:
    """2D cross product (OA x OB)."""
    #return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    #return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    return  (b[0]-a[0])*(o[1]-a[1]) - (b[1]-a[1])*(o[0]-a[0])


def graham_scan_steps(points: List[Point]):
    """Generator yielding steps of Graham Scan."""
    pts = sorted(set(points)) #remove duplicates and lexicographic sort 
    if len(pts) <= 1:
        yield (pts, None, None, None, [])
        return

    # Pivot: lowest y then x
    pivot = min(pts, key=lambda p: (p[1], p[0]))
    

    # # Sort by polar angle and distance
    # def polar_key(p):
    #     from math import atan2
    #     return (atan2(p[1]-pivot[1], p[0]-pivot[0]), (p[0]-pivot[0])**2 + (p[1]-pivot[1])**2)

    # sorted_pts = sorted(pts, key=polar_key)
    
     # Comparator function using cross product
    def polar_cmp(a: Point, b: Point) -> int:
        cp = cross(pivot, a, b)
        if cp > 0:
            return -1  # a comes before b (counter-clockwise)
        elif cp < 0:
            return 1   # b comes before a (clockwise)
        else:
            # Collinear: closer point comes first
            da = (a[0]-pivot[0])**2 + (a[1]-pivot[1])**2
            db = (b[0]-pivot[0])**2 + (b[1]-pivot[1])**2
            return -1 if da < db else (1 if da > db else 0)

    # Sort points by polar angle using comparator
    sorted_pts = sorted(pts, key=cmp_to_key(polar_cmp))

    stack: List[Point] = []
    for p in sorted_pts:
        while len(stack) >= 2 and cross(stack[-2], stack[-1], p) <= 0:
            yield (stack.copy(), stack[-1], p, None)
            stack.pop()
        stack.append(p)
        yield (stack.copy(), p, None, None)

    # final step: close hull
    yield (stack.copy(), None, None, "final")

# ---------------- Animation ----------------
def animate_graham(points: List[Point]):
    fig, ax = plt.subplots()
    xs, ys = zip(*points)
    ax.scatter(xs, ys, c='blue', label='Points')

    hull_line, = ax.plot([], [], 'r-', lw=2)
    hull_pts = ax.scatter([], [], c='red', s=80)

    # Text indicators for p, q, r
    text_p = ax.text(1.05, 0.9, "", transform=ax.transAxes, fontsize=10, color="green")
    text_q = ax.text(1.05, 0.85, "", transform=ax.transAxes, fontsize=10, color="orange")
    text_r = ax.text(1.05, 0.80, "", transform=ax.transAxes, fontsize=10, color="purple")

    ax.set_aspect('equal')
    ax.set_title("Graham Scan Simulation")

    steps = list(graham_scan_steps(points))

    def update(frame):
        stack, p, q, status = steps[frame]

        # Hull line and points
        if stack:
            hx, hy = zip(*stack)
            if status == "final":
                # close polygon
                hull_line.set_data(list(hx) + [hx[0]], list(hy) + [hy[0]])
            else:
                hull_line.set_data(hx, hy)
            hull_pts.set_offsets(np.array(stack))
        else:
            hull_pts.set_offsets(np.empty((0, 2)))

        # Update indicators on side
        text_p.set_text(f"p: {p}" if p else "p: -")
        text_q.set_text(f"q: {q}" if q else "q: -")
        text_r.set_text(f"status: {status}" if status else "r: -")

        return hull_line, hull_pts, text_p, text_q, text_r

    ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=800, blit=False, repeat=False)
    plt.show()

    # Print final hull points (CCW order)
    final_hull = steps[-1][0]
    print("Convex Hull points in CCW order:")
    for pt in final_hull:
        print(pt)

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    points = [
        (0, 7), (2, 8), (4, 9), (5, 6), (4, 4),
        (2, 3), (4, 2), (3, 0)
    ]
    animate_graham(points)
