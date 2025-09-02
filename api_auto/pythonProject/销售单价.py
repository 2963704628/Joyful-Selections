import random

# 2023年销售单价
price_2023 = [
    3.24, 7.5, 8.25, 7, 6.75, 3.5, 3, 6.75, 6, 7.5,
    40, 1.5, 3.25, 5.5, 3.5, 7, 8, 6.75, 6.5, 3.75,
    6.25, 5.5, 5.75, 5.25, 5.5, 6.25, 5, 5.75, 7, 5.25,
    7.25, 4.5, 4.5, 4, 2.5, 2.5, 3.25, 57.5, 19,
    16, 100, 9.6, 8.1, 7.8, 4.5, 7.5, 6.6, 6.9, 6.8,
    6.6, 7.8, 6, 6.9, 8.4, 6.3, 8.7, 5.4, 5.4, 4.8
]

# 存储未来八年的销售单价
future_prices = []

# 计算2024到2031年的预期销售单价
for year in range(8):  # 未来八年
    year_prices = []
    for i in range(len(price_2023)):
        if i < 16:  # 第1到第16个销售单价
            new_price = price_2023[i]  # 保持不变
        elif 16 <= i <= 36 or 41 <= i <= 58:  # 第17到第37个和第42到第59个销售单价
            growth_rate = random.uniform(0.029, 0.031)  # 3%左右的随机增长率
            if year == 0:
                new_price = price_2023[i]  # 第一年销售单价为2023年的销售单价
            else:
                new_price = future_prices[year - 1][i] * (1 + growth_rate)  # 计算未来销售单价
        elif i == 38 or i == 39 or i == 40:  # 第38、39、40个销售单价
            growth_rate = random.uniform(-0.05, -0.01)  # -5%到-1%之间的随机增长率
            if year == 0:
                new_price = price_2023[i]  # 第一年销售单价为2023年的销售单价
            else:
                new_price = future_prices[year - 1][i] * (1 + growth_rate)  # 计算未来销售单价
        elif i == 41:  # 第41个销售单价
            growth_rate = -0.04  # 固定为-4%
            if year == 0:
                new_price = price_2023[i]  # 第一年销售单价为2023年的销售单价
            else:
                new_price = future_prices[year - 1][i] * (1 + growth_rate)  # 计算未来销售单价

        year_prices.append(new_price)

    future_prices.append(year_prices)

# 输出结果
for year in range(8):
    print(f"Year {2023 + year}:")
    for i in range(len(future_prices[year])):
        print(f"  Crop {i + 1}: Price = {future_prices[year][i]:.2f}")