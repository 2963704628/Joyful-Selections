import pandas as pd
from scipy.optimize import linprog

# 1. 读取数据
data_path = "C:\\Users\\86159\\Desktop\\data.xlsx"
supplier_data_path = "C:\\Users\\86159\\Desktop\\最少数量供应商.xlsx"
data = pd.read_excel(data_path, index_col=[0, 1])  # 假设索引是周和转运商ID
supplier_data = pd.read_excel(supplier_data_path, index_col=[0, 1])  # 假设索引是周和供应商ID

# 2. 准备目标函数系数
# 目标是最小化损耗率乘以供货量
c = -data['loss_rate'].values  # 假设'loss_rate'是数据中的列名

# 3. 准备约束条件
# 每一家转运商的运货能力之和 <= 6000 立方米
transport_capacity_constraints = []
for transporter_id in data.index.get_level_values('transporter_id').unique():
    capacity_constraint = data.loc[transporter_id]['supply_volume'].sum() <= 6000
    transport_capacity_constraints.append(capacity_constraint)

# 损耗量应该小于供货量
loss_less_than_supply_constraints = data['loss_rate'] * data['supply_volume'] < 1  # 损耗率小于1意味着损耗量小于供货量

# 4. 将约束条件转换为linprog所需的格式
# 由于linprog要求每个约束条件都是一个等式，我们需要将不等式转换为等式
A_ub = []
b_ub = []
for constraint in transport_capacity_constraints:
    A_ub.append(pd.Series(1, index=data.index.get_level_values('transporter_id').unique()))
    b_ub.append(6000)

# 5. 求解线性规划问题
res = linprog(c, A_ub=A_ub, b_ub=b_ub, method='highs')

# 6. 结果分析
print("Optimization result:", res)