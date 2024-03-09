import random

# 计算未被覆盖的面积（蒙特卡洛）
def is_inside_circle(point, circle_center, radius):
    x, y = point
    cx, cy = circle_center
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2

def monte_carlo_net_area(main_R, main_coord, other_Rs, other_coords, num_samples=100000):
    max_x = max([main_coord[0] + main_R] + [coord[0] + R for coord, R in zip(other_coords, other_Rs)])
    min_x = min([main_coord[0] - main_R] + [coord[0] - R for coord, R in zip(other_coords, other_Rs)])
    max_y = max([main_coord[1] + main_R] + [coord[1] + R for coord, R in zip(other_coords, other_Rs)])
    min_y = min([main_coord[1] - main_R] + [coord[1] - R for coord, R in zip(other_coords, other_Rs)])

    count_inside_main = 0
    count_inside_others = 0
    for _ in range(num_samples):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        if is_inside_circle((x, y), main_coord, main_R):
            count_inside_main += 1
            for coord, R in zip(other_coords, other_Rs):
                if is_inside_circle((x, y), coord, R):
                    count_inside_others += 1
                    break

    main_circle_area = (count_inside_main / num_samples) * (max_x - min_x) * (max_y - min_y)
    overlap_area = (count_inside_others / num_samples) * (max_x - min_x) * (max_y - min_y)

    return main_circle_area - overlap_area

# 示例
main_R = 5
main_coord = (0, 0)
other_Rs = [4, 3, 2, 3]
other_coords = [(6, 0), (0, 2), (2, 0), (-1, -1)]

area = monte_carlo_net_area(main_R, main_coord, other_Rs, other_coords)
print(f"Net Influence Area: {area}")
