from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

Point = Tuple[float, float]

# ---------------- Convex Hull Algorithm ----------------
def orientation(a: Point, b: Point, c: Point) -> int:
    cross = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    if abs(cross) < 1e-12:
        return 0
    return 1 if cross > 0 else 2 #1 and 2 swap korsi

def dist_sq(a: Point, b: Point) -> float:
    dx, dy = a[0]-b[0], a[1]-b[1]
    return dx*dx + dy*dy

def jarvis_march_clockwise_steps(points: List[Point]):
    """Generator yielding steps for CW Jarvis March."""
    unique = list(dict.fromkeys(points))
    if len(unique) <= 1:
        yield (unique, None, None, None, [])
        return

    start = min(unique, key=lambda p: (p[0], p[1]))
    hull = []
    p = start
    added_collinear = []

    while True:
        hull.append(p)
        q = unique[0] if unique[0]!=p else unique[1]
        collinear_points = []

        for r in unique:
            if r == p or r == q:
                continue
            yield (hull.copy(), p, q, r, added_collinear.copy())
            orient = orientation(p, q, r)
            # CW selection
            if orient == 1:
                q = r
                collinear_points = []
                added_collinear.clear()
            elif orient == 0:
                if dist_sq(p, r) > dist_sq(p, q):
                    collinear_points.append(q)
                    q = r
                else:
                    collinear_points.append(r)

        collinear_points.sort(key=lambda pt: dist_sq(p, pt))
        hull.extend(collinear_points)
        added_collinear = collinear_points.copy()

        p = q
        if p == start:
            yield (hull.copy(), None, None, None, added_collinear.copy())
            break
        yield (hull.copy(), p, None, None, added_collinear.copy())

# ---------------- Animation ----------------
def animate_hull(points: List[Point]):
    fig, ax = plt.subplots()
    xs, ys = zip(*points)
    ax.scatter(xs, ys, c='blue', label='Points')

    hull_line, = ax.plot([], [], 'r-', lw=2)
    hull_pts = ax.scatter([], [], c='red', s=80)
    p_dot, = ax.plot([], [], 'go', markersize=12, label='p')
    q_dot, = ax.plot([], [], 'yo', markersize=12, label='q')
    r_dot, = ax.plot([], [], 'mo', markersize=8, label='r')
    arrow = ax.annotate("", xy=(0,0), xytext=(0,0),
                        arrowprops=dict(facecolor='black', shrink=0.05))

    ax.set_aspect('equal')
    ax.legend()
    ax.set_title("Jarvis March (Clockwise) Simulation with CW arrows")

    steps = list(jarvis_march_clockwise_steps(points))

    def update(frame):
        hull_so_far, p, q, r, _ = steps[frame]

        # Hull line and points
        if hull_so_far:
            hx, hy = zip(*hull_so_far)
            hull_line.set_data(list(hx)+[hx[0]], list(hy)+[hy[0]])
            hull_pts.set_offsets(np.array(hull_so_far))
        else:
            hull_pts.set_offsets(np.empty((0,2)))

        # p, q, r points
        p_dot.set_data([p[0]], [p[1]] if p else [])
        q_dot.set_data([q[0]], [q[1]] if q else [])
        r_dot.set_data([r[0]], [r[1]] if r else [])

        # Arrow from p -> q
        if p and q:
            arrow.set_position((p[0], p[1]))
            arrow.xy = (q[0], q[1])
        else:
            arrow.set_position((0,0))
            arrow.xy = (0,0)

        return hull_line, hull_pts, p_dot, q_dot, r_dot, arrow

    ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=800, blit=True, repeat=False)
    plt.show()

    # Print final hull points in clockwise order
    final_hull = steps[-1][0]
    print("Convex Hull points in clockwise order:")
    for pt in final_hull:
        print(pt)

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    points = [
        (0,3), (2,2), (1,1), (2,1),
        (3,0), (0,0), (3,3), (2,2), (3,1),
        (1,2), (2,3), (1,3)
        #   (0, 7), (2, 8), (5, 6), (4, 4),
        # (2, 3), (4, 2), (3, 0)
    ]
    animate_hull(points)
