import random

# 2023年销售量
sales_2023 = [
    57000, 21850, 22400, 33040, 9875, 170840, 132750, 71400, 30000, 12500,
    1500, 35100, 36000, 14000, 10000, 21000, 36240, 26880, 6240, 30000,
    36210, 3432, 900, 2610, 3600, 4050, 4500, 35480, 13050, 2850, 1200,
    3600, 1800, 1800, 150000, 60000, 36000, 9000, 7200, 18000, 4200
]

# 存储未来七年的销售量和增长率
future_sales = []
growth_rates = []

# 计算2024到2030年的预期销售量
for year in range(8):  # 未来七年
    year_sales = []
    year_growth_rates = []
    for i in range(len(sales_2023)):
        if i == 5 or i == 6:  # 作物6和作物7
            growth_rate = random.uniform(0.05, 0.10)  # 5%到10%
        else:
            growth_rate = random.uniform(-0.05, 0.05)  # -5%到5%

        # 计算预期销售量
        if year == 0:
            new_sales = sales_2023[i]  # 第一年销售量为2023年的销售量
        else:
            new_sales = future_sales[year - 1][i] * (1 + growth_rate)  # 计算未来销售量

        year_sales.append(new_sales)
        year_growth_rates.append(growth_rate)

    future_sales.append(year_sales)
    growth_rates.append(year_growth_rates)

# 输出结果
for year in range(8):
    print(f"Year {2023 + year}:")
    for i in range(len(future_sales[year])):
        print(f"  Crop {i + 1}: Sales = {future_sales[year][i]:.2f}, Growth Rate = {growth_rates[year][i] * 100:.2f}%")