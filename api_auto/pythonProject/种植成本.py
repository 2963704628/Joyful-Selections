import random

# 2023年种植成本
cost_2023 = [
    400, 400, 350, 350, 350, 450, 500, 360, 400, 360,
    350, 1000, 2000, 400, 350, 680, 2000, 1000, 2000,
    2000, 2000, 2000, 2300, 1600, 2400, 2900, 1600,
    1600, 2900, 1600, 1000, 4100, 2000, 900, 2400,
    1200, 2400, 2400, 2400, 2400, 2700, 2000, 3000,
    3500, 2000, 2000, 3500, 2000, 1200, 5000, 2500,
    1100, 2000, 500, 500, 3000, 2000, 10000, 10000,
    2640, 1320, 2640, 2640, 2640, 2640, 3000, 2200,
    3300, 3850, 2200, 2200, 3850, 2200, 1300, 5500,
    2750, 1200
]

# 存储未来八年的种植成本
future_costs = []

# 计算2024到2031年的预期种植成本
for year in range(8):  # 未来八年
    year_costs = []
    for i in range(len(cost_2023)):
        # 生成随机增长率在4%到6%之间
        growth_rate = random.uniform(0.04, 0.06)

        # 计算预期种植成本
        if year == 0:
            new_cost = cost_2023[i]  # 第一年种植成本为2023年的种植成本
        else:
            new_cost = future_costs[year - 1][i] * (1 + growth_rate)  # 计算未来种植成本

        year_costs.append(new_cost)

    future_costs.append(year_costs)

# 输出结果
for year in range(8):
    print(f"Year {2023 + year}:")
    for i in range(len(future_costs[year])):
        print(f"  Crop {i + 1}: Cost = {future_costs[year][i]:.2f}")