import pulp
import pandas as pd

# 假设的参数值
material_consumption = {'A': 0.6, 'B': 0.66, 'C': 0.72}
weekly_production_capacity = 28200  # 每周产能为 2.82 万立方米
inventory_requirement = 2 * weekly_production_capacity  # 两周生产需求的原材料库存量

# 读取Excel文件
file_path = r"C:\Users\86159\Desktop\供应商的供货量.xlsx"
sheet_name = 'Sheet1'
data = pd.read_excel(file_path, sheet_name=sheet_name)

# 初始化supplier_capacity字典
supplier_capacity = {}

# 遍历DataFrame中的每一行，填充supplier_capacity字典
for index, row in data.iterrows():
    supplier_id = f"S{index+1:03d}"  # 格式化供应商ID为S001, S002, ...
    material_type = row['材料分类']
    for week in range(1, 241):  # 遍历W001到W240
        week_column = f'W{week}'
        supply_volume = row.get(week_column, 0)  # 使用get方法避免缺失列的问题
        # 假设材料分类直接对应材料类型A, B, C
        if material_type in material_consumption:
            material_key = material_type
        else:
            # 如果材料分类不是A, B, C，可以选择跳过或者映射到相应的材料类型
            continue
        supplier_capacity[(supplier_id, material_key)] = supply_volume

# 创建决策变量，这里需要使用与supplier_capacity字典中一致的键结构
x = pulp.LpVariable.dicts("x", [(supplier_id, material) for supplier_id, material in supplier_capacity.keys()], lowBound=0, cat='Binary')

# 创建问题实例
model = pulp.LpProblem("Supplier_Selection", pulp.LpMaximize)

# 目标函数：最大化供应商总数
# 这里的循环需要遍历x字典中的所有键
model += -pulp.lpSum(x[supplier_id, material] for supplier_id, material in x)

# 约束条件
# (1) 每周产能约束
for material, consumption in material_consumption.items():
    # 这里需要遍历所有的供应商和材料组合
    model += pulp.lpSum([
        supplier_capacity[supplier_id, material] * x[supplier_id, material]
        for supplier_id, material in supplier_capacity.keys() if material == material
    ]) >= weekly_production_capacity

# (2) 库存约束
# 这里需要遍历所有的供应商和材料组合
model += pulp.lpSum([
    supplier_capacity[supplier_id, material] * x[supplier_id, material]
    for supplier_id, material in supplier_capacity.keys()
]) >= inventory_requirement

# 求解问题
model.solve()

# 输出结果
print("Status:", pulp.LpStatus[model.status])

total_suppliers = sum(x[supplier_id].value() == 1 for supplier_id in x)
selected_suppliers = [supplier_id for supplier_id in x if x[supplier_id].value() == 1]

print(f"至少需要选择 {total_suppliers} 家供应商来满足生产需求。")
print("这些供应商及其材料分类如下：")
for supplier_id in selected_suppliers:
    material_type = next((mate for mate in material_consumption if (supplier_id[0], mate) in supplier_capacity), None)
    print(f"供应商ID: {supplier_id[0]}, 材料分类: {material_type}")