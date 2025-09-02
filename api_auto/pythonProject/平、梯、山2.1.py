from simanneal import Annealer
import random
import pandas as pd

# 从其他 Python 文件中导入数据
from 预期销售量 import expected_sales  # 假设返回一个列表或字典
from 种植成本 import planting_costs  # 假设返回一个列表
from 未来亩产量 import future_yield  # 假设返回一个字典
from 销售单价 import selling_prices  # 假设返回一个列表

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
        # 随机选择一个年份和地块
        i, j = random.choice(I_values), random.choice(J_values)
        # 随机选择一个作物进行翻转
        k = random.choice(K_values)

        # 深复制状态
        new_state = [row[:] for row in self.state]

        # 确保翻转后仍然有一个作物种植
        if new_state[i][j][k] == 1:
            new_state[i][j][k] = 0  # 如果当前种植，翻转为不种植
            # 确保至少有一个作物种植
            if sum(new_state[i][j]) == 0:
                new_state[i][j][random.choice(K_values)] = 1  # 随机选择一个作物种植
        else:
            new_state[i][j][k] = 1  # 如果当前不种植，翻转为种植

        self.state = new_state  # 更新状态

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

                # 计算每种作物的收益和成本
                for k in K_values:
                    # 收益
                    revenue = min(y_ik[i][k], self.Sk_data[k]) * self.bk_data[k]  # 收益
                    # 成本
                    planting_cost = r_ik[k] * self.Pk_data[k]  # 种植成本
                    # 利润
                    profit = revenue - planting_cost  # 利润

                    total_profit += profit  # 累加总利润

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
Sk_data = expected_sales  # 从预期销售量文件中获取
bk_data = selling_prices  # 从销售单价文件中获取
Pk_data = planting_costs  # 从种植成本文件中获取
Ck_data = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 for legume, 0 for non-legume

# 初始化状态
state = [[[1 for _ in K_values] for j in J_values] for i in I_values]  # 确保每块土地都有作物种植

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