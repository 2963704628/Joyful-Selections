import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 假设 best_state 是模拟退火算法的输出
# 生成一些示例数据
years = list(range(1, 15))  # 1到14年
plots = list(range(16))  # 16块地
crops = list(range(22))  # 22种作物

# 计算每个地块每年的作物种植面积
heatmap_data = np.zeros((len(years), len(plots), len(crops)))

for i in range(len(years)):
    for j in range(len(plots)):
        for k in range(len(crops)):
            heatmap_data[i][j][k] = best_state[i][j][k]

# 绘制热图
plt.figure(figsize=(12, 8))
for year in range(len(years)):
    plt.subplot(4, 4, year + 1)
    sns.heatmap(heatmap_data[year], annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Area'})
    plt.title(f'Year {years[year]}')
    plt.xlabel('Plots')
    plt.ylabel('Crops')

plt.tight_layout()
plt.show()

# 计算收益和成本
total_revenue = []
total_cost = []

for i in range(len(years)):
    revenue = 0
    cost = 0
    for j in range(len(plots)):
        for k in range(len(crops)):
            if best_state[i][j][k] > 0:
                revenue += min(yield_amount[k], Sk_data[k]) * best_state[i][j][k] * bk_data[k]
                cost += best_state[i][j][k] * Pk_data[k]
    total_revenue.append(revenue)
    total_cost.append(cost)

# 绘制收益和成本柱状图
plt.figure(figsize=(10, 6))
plt.bar(years, total_revenue, label='Total Revenue', alpha=0.6)
plt.bar(years, total_cost, label='Total Cost', alpha=0.6)
plt.xlabel('Year')
plt.ylabel('Amount')
plt.title('Total Revenue and Cost Over Years')
plt.legend()
plt.show()