import math
import random
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import folium
import numpy as np
import pandas as pd
import datetime
from math import sqrt
from numpy import concatenate
from sklearn.preprocessing import LabelEncoder
import sys



output_content = ""


# 计算未被覆盖的面积（蒙特卡洛）
def is_inside_circle(point, circle_center, radius):
    x, y = point
    cx, cy = circle_center
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


def monte_carlo_net_area(main_R, main_coord, other_Rs, other_coords, num_samples=100000):
    # 确定边界
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
output_content += "Net Influence Area: {area}" + "\n"


# 查看具体区域的权重（只与其他公司影响力范围相关）
# 主题：假设每被一个公司覆盖-10权重，列出本公司影响范围内所有1*1空间的目前权重

def is_inside_circle(point, circle_center, radius):
    x, y = point
    cx, cy = circle_center
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


def calculate_weights(main_R, main_coord, other_Rs, other_coords, m, n):
    # 计算所有圆的最左、最右、最上和最下的边界，形成一个矩形
    max_x = max(main_coord[0] + main_R, max(coord[0] + R for coord, R in zip(other_coords, other_Rs)))
    min_x = min(main_coord[0] - main_R, min(coord[0] - R for coord, R in zip(other_coords, other_Rs)))
    max_y = max(main_coord[1] + main_R, max(coord[1] + R for coord, R in zip(other_coords, other_Rs)))
    min_y = min(main_coord[1] - main_R, min(coord[1] - R for coord, R in zip(other_coords, other_Rs)))

    # 计算每个方块的大小
    dx = (max_x - min_x) / m
    dy = (max_y - min_y) / n

    zero_weight_points = {}
    negative_weight_points = {}

    # 遍历每个方块
    for i in range(m):
        for j in range(n):
            x = int(min_x + i * dx + 0.5)  # 方块的中心x坐标
            y = int(min_y + j * dy + 0.5)  # 方块的中心y坐标
            point = (x, y)

            if is_inside_circle(point, main_coord, main_R):  # 只考虑在主圆内的点
                weight = 0

                # 对于在主圆内的每个点，检查是否在其他圆内
                for coord, R in zip(other_coords, other_Rs):
                    if is_inside_circle(point, coord, R):
                        weight -= 10

                if weight == 0:
                    zero_weight_points[point] = weight
                else:
                    negative_weight_points[point] = weight

    return zero_weight_points, negative_weight_points


# 使用之前的参数进行测试
main_R = 5
main_coord = (0, 0)
other_Rs = [4, 3, 2, 3]
other_coords = [(6, 0), (0, 2), (2, 0), (-1, -1)]

zero_weight, negative_weight = calculate_weights(main_R, main_coord, other_Rs, other_coords, 100, 100)
print("Length of Zero weight: ", len(zero_weight))
output_content += "Length of Zero weight: " + str(len(zero_weight)) + "\n"
print("Zero weight points:", zero_weight)
output_content += "Zero weight points:" + str(zero_weight) + "\n"
print("Negative weight points:", negative_weight)
output_content += "Negative weight points:" + str(negative_weight) + "\n"


#主题：可视化本公司（0,0）和其他公司的影响范围

# 主要公司的位置和半径
main_company = (0, 0, 5)  # (x, y, R)

# 其他公司的位置和半径
other_companies = [
    (6, 0, 5),   # (x, y, R)
    (0, 2, 3),
    (2, 0, 2),
    (-1,-1,1)
]

fig, ax = plt.subplots(figsize=(10, 10))

# 绘制主要公司的圆
circle = patches.Circle((main_company[0], main_company[1]), main_company[2], fc='blue', alpha=0.5)
ax.add_patch(circle)

# 绘制其他公司的圆
for company in other_companies:
    circle = patches.Circle((company[0], company[1]), company[2], fc='red', alpha=0.5)
    ax.add_patch(circle)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# 设置网格线，并且每个单位长度为1
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_xticks(range(-10, 11, 1))
ax.set_yticks(range(-10, 11, 1))

plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('result.png')
# plt.savefig('./frontend/public/result.png')
# plt.show()


# 根据房产实例计算权重（房价，距离）
# 完全独立于上一组模拟
# 载入数据
df = pd.read_excel('data.xlsx', sheet_name=4)
df0 = pd.read_excel('data.xlsx', sheet_name=0)
df1 = pd.read_excel('data.xlsx', sheet_name=1)
df2 = pd.read_excel('data.xlsx', sheet_name=2)
df3 = pd.read_excel('data.xlsx', sheet_name=3)
# 数据合并
dff = pd.concat([df0, df1, df2, df3])
# 数据预处理
dff["tube_name"] = dff["city"] + dff["tube_name"]
dff.drop(labels=['city'], axis=1, inplace=True)
# 数据合并
data = pd.merge(df, dff, on="tube_name")

data.rename(
    columns={'租金中位数（元/月）': 'area_price_level', '居住便利度': 'convenience', 'tube_distance（m）': 'tube_distance'},
    inplace=True)

data['city_cn']=data['city']
data.city[data.city=='上海'] = 'shanghai'
data.city[data.city=='广州'] = 'guangzhou'
data.city[data.city=='北京'] = 'beijing'
data.city[data.city=='深圳'] = 'shenzhen'
lb=LabelEncoder()
data['city_encode'] = lb.fit_transform(data['city'].values)
data['floor_encode'] = lb.fit_transform(data['floor'].values)
data['towards_encode'] = lb.fit_transform(data['towards'].values)

data.head(3)

print(data.head(3))
output_content += str(data.head(3)) + "\n"

# 主要公司的位置和半径
main_company = (31.19602, 121.433985, 350)  # (纬度, 经度, 半径)

#根据数据对北上广部分地区建立可视化模型

# 创建Folium地图
sh_map = folium.Map(
    location=[main_company[0], main_company[1]],  # 地图初始位置设为主要公司位置
    zoom_start=12,
    tiles="cartodbpositron"
)

# 绘制主要公司的圆，透明填充，黑色虚线边框
folium.Circle(
    location=(main_company[0], main_company[1]),
    radius=main_company[2],  # 半径单位为米
    color='red',
    fill=False,
    weight=2,  # 边框宽度
    dash_array='5, 5'  # 虚线样式
).add_to(sh_map)

folium.Circle(
    location=(main_company[0], main_company[1]),
    radius=10,  # 半径单位为米
    color='red',
    fill=True,
    weight=2,  # 边框宽度
    dash_array='5, 5'  # 虚线样式
).add_to(sh_map)

for i in range(1500):
    lat = data['latitude'].iloc[i]
    long = data['longitude'].iloc[i]
    radius = data['rent_room'].iloc[i]/550 #550

    if data['rent_room'].iloc[i] > 4500:
        color = "#008080"  # 蓝色为高价房
    elif data['rent_room'].iloc[i] < 3000:
        color = "#9BCD9B"  # 灰色为低价房
    else:
        color = "#9C9C9C"  #绿色为平价房

    popup_text = """城市 : {}<br>
                楼层 : {}<br>
                租金 : {}<br>
                朝向 : {}<br>
                面积 : {}<br>
                房间数量 : {}<br>
                纬度 : {}<br>
                经度 : {}<br>"""
    popup_text = popup_text.format(data['city_cn'].iloc[i] ,
                               data['floor'].iloc[i] ,
                               data['rent_room'].iloc[i] ,
                               data['towards'].iloc[i] ,
                               data['price_area'].iloc[i] ,
                               data['room_no'].iloc[i],
                               data['latitude'].iloc[i],
                               data['longitude'].iloc[i]
                               )
    folium.CircleMarker(location = [lat, long], popup= popup_text,radius = radius, color = color, fill = True).add_to(sh_map)

# 定义矩形的四个顶点坐标 (纬度, 经度)
coords = [
    (31.20138055, 121.4361536),
    (31.195382, 121.439823),
    (31.191512, 121.432394),
    (31.19873115, 121.4246766),
    (31.20138055, 121.4361536)
]

# 绘制矩形，闭合线段
folium.PolyLine(
    coords,
    color="black",
    weight=2,
    opacity=1,
    dash_array='5, 5'  # 虚线样式
).add_to(sh_map)

sh_map
sh_map.save('map.html')
# sh_map.save('./frontend/public/map.html')


# 黑色虚线代表数据有效范围
# 红色虚线与中点代指本公司

# 创建字典以存储在圆内的房子数据
houses_in_circle = {}

# 遍历DataFrame中的房子
for i in range(1500):
    house_coord = (data['latitude'].iloc[i], data['longitude'].iloc[i])
    house_price = data['rent_room'].iloc[i]
    # 检查房子是否在主要公司的圆内
    if is_inside_circle(house_coord, (main_company[0], main_company[1]), main_company[2]):
        # 计算房子到圆心的距离
        distance = math.sqrt((house_coord[0] - main_company[0]) ** 2 + (house_coord[1] - main_company[1]) ** 2)
        # 存储房子的数据
        houses_in_circle[house_coord] = house_price / distance  # function = 房价/距离
        # 解释：这个等式是临时的。房价越高说明用户消费力越高，与权重成正比。距离越远影响力越小，成反比。

# 计算总和
total_value = sum(houses_in_circle.values())

print("Total:", total_value / 1000000)
output_content += f"Total: {total_value / 1000000}\n"
