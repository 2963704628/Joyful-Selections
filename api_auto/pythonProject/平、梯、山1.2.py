from simanneal import Annealer
import random
import pandas as pd


class CropPlanning(Annealer):
    def __init__(self, state, djk_data, wj_data, Sk_data, bk_data, Pk_data, Ck_data):
        self.djk_data = djk_data  # 亩产量数据
        self.wj_data = wj_data  # 地块权重或面积
        self.Sk_data = Sk_data
        self.bk_data = bk_data
        self.Pk_data = Pk_data
        self.Ck_data = Ck_data
        super().__init__(state)  # 调用父类构造函数

    def energy(self):
        # 计算能量（目标函数）
        total_profit = 0
        penalty = 0

        # 计算 y_ik
        y_ik = [[0 for _ in K_values] for _ in I_values]  # 初始化 y_ik
        r_ik = [0 for _ in K_values]  # 初始化 r_ik

        for i in I_values:  # 遍历每一年
            for j in J_values:  # 遍历每块地
                for k in K_values:  # 遍历每种作物
                    if self.state[i][j][k] == 1:
                        # 计算 y_ik
                        y_ik[i][k] += self.djk_data.get((j + 1, k + 1), 0) * self.wj_data[j]  # d_jk * W_j

                        # 计算 r_ik
                        r_ik[k] += self.state[i][j][k] * self.wj_data[j]  # X_ijk * W_j

                        # 第一部分利润
                        normal_revenue = min(y_ik[i][k], self.Sk_data[k]) * self.bk_data[k]  # 正常收益
                        planting_cost = r_ik[k] * self.Pk_data[k]  # 种植成本
                        profit_part1 = normal_revenue - planting_cost  # 第一部分利润

                        # 第二部分利润
                        second_profit = min(y_ik[i][k] - self.Sk_data[k], 0) * (0.5 * self.bk_data[k])  # 第二部分利润

                        total_profit += profit_part1 + second_profit  # 总利润

                # 重置 r_ik 为 0，以便下一年使用
                r_ik = [0 for _ in K_values]

            # 约束3: 每一块土地在每一年只能种植一种作物
            for j in J_values:
                if sum(self.state[i][j]) != 1:  # 如果该地块没有种植任何作物或种植多于一种作物
                    penalty += 10000  # 增加惩罚

        # 约束1: 不连作约束
        for i in I_values[:-1]:
            for j in J_values:
                for k in K_values:
                    if self.state[i][j][k] == 1 and self.state[i + 1][j][k] == 1:
                        penalty += 10000

        # 约束2: 每一块土地三年内至少种植一次豆类作物
        for j in J_values:
            for start_year in I_values:
                end_year = min(start_year + 2, len(I_values) - 1)
                legume_grown = any(
                    self.state[i][j][k] == 1 for i in range(start_year, end_year + 1) for k in K_values if
                    self.Ck_data[k] == 1)
                if not legume_grown:
                    penalty += 5000

        return -(total_profit - penalty)  # 取负值因为模拟退火是最小化问题

# 定义集合
I_values = range(7)  # 年份范围
J_values = range(26)  # 地块编号
K_values = range(15)  # 作物编号

# 读取亩产量数据
file_path = r"C:\Users\86159\Desktop\亩产量.xlsx"
data = pd.read_excel(file_path, index_col=0, engine='openpyxl')

# 将亩产量数据转换为字典
djk_data = data.to_dict('index')

# 初始化其他模型参数
wj_data = [80, 55, 35, 72, 68, 55, 60, 46, 40, 28, 25, 86, 55, 44, 50, 25, 60, 45, 35, 20, 15, 13, 15, 18, 27, 20]
Sk_data = [57000, 21850, 22400, 33040, 9875, 170840, 132750, 71400, 30000, 12500, 1500, 35100, 36000, 14000, 10000]
bk_data = [5.25, 7.5, 8.25, 7, 6.75, 3.5, 3, 6.75, 6, 7.5, 40, 1.5, 3.25, 5.5, 3.5]
Pk_data = [400, 400, 350, 350, 350, 450, 500, 360, 400, 360, 350, 1000, 2000, 400, 350]
Ck_data = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 for legume, 0 for non-legume

# 初始化状态
state = [[[0 for _ in K_values] for _ in J_values] for _ in I_values]

# 随机选择一种作物种植
for i in I_values:
    for j in J_values:
        k = random.choice(K_values)  # 随机选择一种作物
        state[i][j][k] = 1  # 只在这块地上种植一种作物

# 创建问题实例
crop_planning = CropPlanning(state, djk_data, wj_data, Sk_data, bk_data, Pk_data, Ck_data)

# 运行模拟退火算法
best_state, best_energy = crop_planning.anneal()

# 输出结果
for i in range(len(I_values)):  # 遍历年份
    for j in range(len(J_values)):  # 遍历地块
        planted = False  # 标记是否有作物种植
        for k in range(len(K_values)):  # 遍历作物
            if best_state[i][j][k] == 1:
                print(f"Year {i + 2024}, Plant {k} on plot {j} with decision variable value {best_state[i][j][k]}")
                planted = True
        if not planted:
            print(f"Year {i + 2024}, No crop on plot {j} (should not happen due to constraints)")