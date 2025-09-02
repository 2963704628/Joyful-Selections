from simanneal import Annealer
import random
import pandas as pd

# 定义你的问题类
class CropPlanning(Annealer):
    def __init__(self, state, djk_data, wj_data, Sk_data, bk_data, Pk_data, Ck_data):
        self.djk_data = djk_data
        self.wj_data = wj_data
        self.Sk_data = Sk_data
        self.bk_data = bk_data
        self.Pk_data = Pk_data
        self.Ck_data = Ck_data
        super().__init__(state)  # 调用父类构造函数

    def move(self):
        # 随机选择一个时间段和地块
        i, j = random.choice(I_values), random.choice(J_values)
        # 随机选择一个作物进行翻转
        if i % 2 == 0:
            k = random.choice(range(1, 19))  # 偶数时间段只能选择作物1至18
        else:
            k = random.choice(range(19, 22))  # 奇数时间段只能选择作物19至21

        # 确保每块土地在每个时间段只种植一个作物
        self.state[i][j] = [0] * len(K_values)
        self.state[i][j][k] = 1

    def energy(self):
        # 计算能量（目标函数）
        total_profit = 0
        penalty = 0

        # 计算 y_ik 和 r_ik
        y_ik = [[0 for _ in K_values] for _ in I_values]  # 初始化 y_ik
        r_ik = [[0 for _ in K_values] for _ in I_values]  # 初始化 r_ik

        for i in I_values:  # 遍历每一个时间段
            for j in J_values:  # 遍历每块地
                for k in K_values:  # 遍历每种作物
                    if self.state[i][j][k] == 1:
                        # 计算 y_ik
                        y_ik[i][k] += self.djk_data[k] * self.wj_data[j]  # d_jk * W_j
                        # 计算 r_ik
                        r_ik[i][k] += self.wj_data[j]  # W_j

                # 计算每种作物的收益和成本
                for k in K_values:
                    # 收益
                    revenue = min(y_ik[i][k], self.Sk_data[k]) * self.bk_data[k]  # 收益
                    # 成本
                    planting_cost = r_ik[i][k] * self.Pk_data[k]  # 种植成本
                    # 利润
                    profit = revenue - planting_cost  # 利润

                    # 第二部分利润
                    additional_profit = max(y_ik[i][k] - self.Sk_data[k], 0) * 0.5 * self.bk_data[k]

                    total_profit += profit + additional_profit  # 累加总利润

            # 约束3: 在j块土地上的种植面积累加和等于该地的耕地面积
            for j in J_values:
                if sum(self.state[i][j]) != 1:  # 如果该地块没有种植任何作物或种植多于一种作物
                    penalty += 10000  # 增加惩罚

        # 约束1: 每块土地六个时间段内至少种植一次豆类作物
        for j in J_values:
            for start_time in range(0, len(I_values), 6):
                end_time = min(start_time + 5, len(I_values) - 1)
                legume_grown = any(
                    self.state[i][j][k] == 1 for i in range(start_time, end_time + 1) for k in K_values if
                    self.Ck_data[k] == 1)
                if not legume_grown:
                    penalty += 5000

        # 约束2: 同一块土地不能连续两个时间段种植同一作物，作物0除外
        for i in range(len(I_values) - 1):
            for j in J_values:
                for k in K_values:
                    if k == 0:  # 作物0的特殊约束
                        if i % 2 == 0 and self.state[i][j][k] == 1:
                            if i + 1 < len(I_values) and self.state[i + 1][j][k] != 1:
                                penalty += 10000
                            if i + 2 < len(I_values) and self.state[i + 2][j][k] == 1:
                                penalty += 10000
                    elif 1 <= k <= 18:  # 作物1到作物18只能在偶数时间段种植
                        if i % 2 == 1 and self.state[i][j][k] == 1:
                            penalty += 10000
                    else:  # 作物19到作物21只能在奇数时间段种植
                        if i % 2 == 0 and self.state[i][j][k] == 1:
                            penalty += 10000

        return -(total_profit - penalty)  # 取负值因为模拟退火是最小化问题

# 定义集合
I_values = range(14)  # 时间范围
J_values = range(8)  # 地块编号
K_values = range(22)  # 作物编号

# 亩产量
djk_data = [500, 3000, 2000, 3000, 2000, 2400, 6400, 2700, 2400, 3300, 3700, 4100, 3200, 12000, 4100, 1600, 10000, 5000, 5500, 5000, 4000, 3000]

# 初始化其他模型参数
wj_data = [15, 10, 14, 6, 10, 12, 22, 20]
Sk_data = [21000, 30000, 24000, 0, 30000, 33600, 38400, 0, 0, 0, 0, 0, 32000, 0, 0, 0, 0, 0, 0, 150000, 100000, 36000]
bk_data = [7, 8, 6.75, 6.5, 3.75, 6.25, 5.5, 5.75, 5.25, 5.5, 6.5, 5, 5.75, 7, 5.25, 7.25, 4.5, 4.5, 4, 2.5, 2.5, 3.25]
Pk_data = [680, 2000, 1000, 2000, 2000, 2000, 2000, 2300, 1600, 2400, 2900, 1600, 1600, 2900, 1600, 1000, 4100, 2000, 900, 2000, 500, 500]
Ck_data = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 for legume, 0 for non-legume

# 初始化状态
state = [[[0 for _ in K_values] for j in J_values] for i in I_values]  # 初始化状态为不种植任何作物

# 确保每块土地都有作物种植
for i in I_values:
    for j in J_values:
        if i % 2 == 0:
            k = (i * len(J_values) + j) % 18 + 1  # 偶数时间段均匀分配作物1至18
        else:
            k = (i * len(J_values) + j) % 3 + 19  # 奇数时间段均匀分配作物19至21
        state[i][j] = [0] * len(K_values)
        state[i][j][k] = 1

# 创建问题实例
crop_planning = CropPlanning(state, djk_data, wj_data, Sk_data, bk_data, Pk_data, Ck_data)

# 运行模拟退火算法
best_state, best_energy = crop_planning.anneal()

# 输出结果
for i in range(len(I_values)):  # 遍历时间段
    for j in range(len(J_values)):  # 遍历地块
        for k in range(len(K_values)):  # 遍历作物
            if best_state[i][j][k] == 1:
                print(f"Time {i + 1}, Plant {k} on plot {j} with decision variable value {best_state[i][j][k]}")