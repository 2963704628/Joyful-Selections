from simanneal import Annealer
import random

# 定义你的问题类
class CropPlanning(Annealer):
    def __init__(self, state, wj_data, Sk_data, Pk_data, Ck_data, bk_data):
        self.wj_data = wj_data  # 地块权重或面积
        self.Sk_data = Sk_data
        self.Pk_data = Pk_data
        self.Ck_data = Ck_data
        self.bk_data = bk_data  # 销售单价
        super().__init__(state)  # 调用父类构造函数

    def move(self):
        # 随机选择一个年份、地块和作物
        i, j = random.choice(I_values), random.choice(J_values)
        k = random.choice(K_values)

        # 深复制状态
        new_state = [row[:] for row in self.state]

        # 随机改变种植面积
        change = random.uniform(-0.1, 0.1)  # 随机变化的幅度
        new_state[i][j][k] = max(0.3, min(new_state[i][j][k] + change, 0.6))  # 确保面积在0.3到0.6之间

        # 确保同一地块上最多只种植两种作物
        planted_crops = [new_state[i][j][k] for k in K_values if new_state[i][j][k] > 0]
        if len(planted_crops) > 2:
            # 如果种植的作物超过两种，随机选择一种作物将其种植面积设为0
            k_to_remove = random.choice([k for k in K_values if new_state[i][j][k] > 0])
            new_state[i][j][k_to_remove] = 0

        self.state = new_state  # 更新状态

    def energy(self):
        # 计算能量（目标函数）
        total_profit = 0
        penalty = 0

        # 计算 y_ik 和 r_ik
        y_ik = [[0 for _ in K_values] for _ in I_values]  # 初始化 y_ik
        r_ik = [0 for _ in K_values]  # 初始化 r_ik

        for i in I_values:  # 遍历每一年
            for j in J_values:  # 遍历每块地
                for k in K_values:  # 遍历每种作物
                    # 计算亩产量
                    if i % 2 == 0:  # 偶数年份
                        yield_amount = [3600, 2400, 3600, 2400, 3000, 8000, 3300, 3000, 4000, 4500, 5000, 4000, 15000, 5000, 2000, 12000, 6000, 6000][k]
                    else:  # 奇数年份
                        yield_amount = [3200, 2200, 3200, 2200, 2700, 7200, 3000, 2700, 3600, 4100, 4500, 3600, 13500, 4500, 1800, 11000, 5400, 6000][k]

                    # 计算 y_ik
                    y_ik[i][k] += yield_amount * self.state[i][j][k]  # d_jk * X_ijk

                    # 计算 r_ik
                    r_ik[k] += self.state[i][j][k]  # X_ijk

                # 计算每种作物的收益和成本
                for k in K_values:
                    # 销售单价
                    price = self.bk_data[k]

                    # 种植成本
                    cost = self.Pk_data[k]

                    # 收益
                    revenue = min(y_ik[i][k], self.Sk_data[k]) * price
                    # 成本
                    planting_cost = r_ik[k] * cost
                    # 第一部分利润
                    profit1 = revenue - planting_cost

                    # 第二部分成本
                    extra_cost = max(y_ik[i][k] - self.Sk_data[k], 0) * 0.5 * price

                    # 总利润
                    total_profit += profit1 - extra_cost

                # 重置 r_ik 为 0，以便下一年使用
                r_ik = [0 for _ in K_values]

            # 约束条件1: 每块土地三年内至少种植一次豆类作物
            for j in J_values:
                for m in range(1, 7):  # m 从 1 到 6
                    for n in range(1, 4):  # n 从 1 到 3
                        if sum(self.state[i][j][k] * self.Ck_data[k] for k in K_values) > 0:
                            break
                    else:
                        penalty += 5000  # 增加惩罚

            # 约束条件2: 0.3 <= X_ijk <= 0.6 且同一地块最多种植两种作物
            for j in J_values:
                planted_crops = [self.state[i][j][k] for k in K_values if self.state[i][j][k] > 0]
                if len(planted_crops) > 2:
                    penalty += 10000  # 增加惩罚
                for k in K_values:
                    if self.state[i][j][k] < 0.3 or self.state[i][j][k] > 0.6:
                        penalty += 10000  # 增加惩罚

            # 约束条件3: 每块土地的种植面积总和等于该地的耕地面积
            for j in J_values:
                if sum(self.state[i][j]) != self.wj_data[j]:
                    penalty += 10000  # 增加惩罚

            # 约束条件4: 同一块土地不能连续两个时间段种同一作物
            for j in J_values:
                for k in K_values:
                    if i > 0 and self.state[i][j][k] > 0 and self.state[i - 1][j][k] > 0:
                        penalty += 10000  # 增加惩罚

        return -(total_profit - penalty)  # 取负值因为模拟退火是最小化问题

# 定义集合
I_values = range(14)  # 时间范围
J_values = range(4)  # 地块编号
K_values = range(18)  # 作物编号

# 初始化其他模型参数
wj_data = [0.6, 0.6, 0.6, 0.6]  # 每块地的耕地面积
Sk_data = [2160, 0, 2160, 0, 810, 2160, 900, 810, 1200, 1350, 0, 1080, 4050, 1350, 0, 3600, 1800, 1800]

# 假设种植成本
Pk_data = [2400, 1200, 2400, 2400, 2400, 2400, 2700, 2000, 3000, 3500, 2000, 2000, 3500, 2000, 1200, 5000, 2500, 1100]

# 定义豆类作物标识
Ck_data = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 for legume, 0 for non-legume

# 销售单价
bk_data = [8, 6.75, 6.5, 3.75, 6.25, 5.5, 5.75, 5.25, 5.5, 6.25, 5, 5.75, 7, 5.25, 7.25, 4.5, 4.5, 4]

# 初始化状态
state = [[[0 for _ in K_values] for _ in J_values] for _ in I_values]

# 随机选择一种作物种植
for i in I_values:
    for j in J_values:
        # 确保每块地最多种植两种作物
        crops_to_plant = random.sample(K_values, 2)
        for k in crops_to_plant:
            state[i][j][k] = random.uniform(0.3, 0.6)  # 随机选择种植面积

# 创建问题实例
crop_planning = CropPlanning(state, wj_data, Sk_data, Pk_data, Ck_data, bk_data)  # 确保传递所有参数

# 运行模拟退火算法
best_state, best_energy = crop_planning.anneal()

# 输出结果
for i in range(len(I_values)):  # 遍历年份
    for j in range(len(J_values)):  # 遍历地块
        for k in range(len(K_values)):  # 遍历作物
            if best_state[i][j][k] > 0:
                print(f"Time {i + 1}, Plant {k} on plot {j} with area {best_state[i][j][k]:.2f}")