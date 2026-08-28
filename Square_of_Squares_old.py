import math

def is_perfect_square(n):
    if n < 0: return False
    sqrt_n = int(math.isqrt(n))
    return sqrt_n**2 == n

def find_near_magic_square(n_min, n_max, r_limit):
    for n in range(n_min, n_max):
        # Center cell is n^2
        center = n**2
        
        # We look for lattice points on the circle (k1+n)^2 + (k2-n)^2 = R^2
        # Let X = k1+n and Y = k2-n. Then X^2 + Y^2 = R^2.
        for r_sq in range(100, r_limit):
            s = r_sq + center # The Magic Constant
            
            # Find all integer pairs (X, Y) such that X^2 + Y^2 = R^2
            points = []
            for x in range(1, int(math.sqrt(r_sq)) + 1):
                y_sq = r_sq - x**2
                y = math.isqrt(y_sq)
                if y**2 == y_sq:
                    # Calculate k1 and k2 from lattice points
                    k1 = x - n
                    k2 = y + n
                    points.append((k1, k2))
            
            if len(points) < 3:
                continue

            # Try combinations of 3 points for the top row
            # Top row: (n+k1_a)^2 + (n+k1_b)^2 + (n+k1_c)^2 = S
            for i in range(len(points)):
                for j in range(len(points)):
                    for l in range(len(points)):
                        if i == j or j == l or i == l: continue
                        
                        ka, kb, kc = points[i], points[j], points[l]
                        
                        top_row_sum = (n + ka[0])**2 + (n + kb[0])**2 + (n + kc[0])**2
                        
                        if top_row_sum == s:
                            # We found a square that is magic in:
                            # 1. All 4 center lines (by Gap Algorithm construction)
                            # 2. The Top Row
                            
                            # Construct the full grid to check "Magic 8"
                            grid = [
                                (n+ka[0])**2, (n+kb[0])**2, (n+kc[0])**2,
                                (n+70)**2,    center,       (n-70)**2, # Placeholder Mid-Row
                                (n-ka[1])**2, (n-kb[1])**2, (n-kc[1])**2
                            ]
                            
                            squares_count = sum(1 for x in grid if is_perfect_square(x))
                            
                            if squares_count >= 7:
                                print(f"--- Found Near-Miss (Squares: {squares_count}) ---")
                                print(f"n={n}, S={s}")
                                print(f"Row 1: {grid[0:3]}")
                                print(f"Row 2: {grid[3:6]}")
                                print(f"Row 3: {grid[6:9]}")
                                return

# Run search
find_near_magic_square(10, 50, 5000)