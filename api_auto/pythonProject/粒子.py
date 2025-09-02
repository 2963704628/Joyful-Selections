import numpy as np

# 定义问题参数
num_particles = 50  # 粒子数量
num_dimensions = 8  # 维度数量，即转运商的数量
max_iter = 240  # 最大迭代次数

# 假设损耗率已知，这里使用随机数模拟
loss_rates = np.random.rand(num_dimensions) * 0.05  # 0到5%的损耗率

# 假设采购成本已知，这里使用随机数模拟
costs = np.array([1.0, 1.2, 1.1])  # A, B, C三类材料的采购成本

# 粒子群初始化
positions = np.random.rand(num_particles, num_dimensions)
velocities = np.zeros((num_particles, num_dimensions))


# 适应度函数
def fitness(particle):
    # 计算成本
    cost = np.dot(particle, costs)
    # 计算损耗率
    loss_rate = np.dot(particle, loss_rates)
    # 转换为负值，因为我们希望最小化这两个目标
    return -cost, -loss_rate


# 粒子群算法主循环
for iter in range(max_iter):
    # 评估当前粒子群的适应度
    for i in range(num_particles):
        positions[i], velocities[i] = update_particle(positions[i], velocities[i], iter)


# 更新粒子位置和速度的函数
def update_particle(position, velocity, iter):
    # 这里使用简单的线性递减惯性权重和随机加速系数
    inertia_weight = 0.9 - iter * (0.9 / max_iter)
    c1, c2 = 2.0, 2.0  # 加速系数
    r1, r2 = np.random.rand(), np.random.rand()

    # 个体最优位置
    pbest_position = position
    # 全局最优位置
    gbest_position = positions[np.argmin(fitness(positions)[0])]

    # 更新速度
    velocity = inertia_weight * velocity + c1 * r1 * (pbest_position - position) + c2 * r2 * (gbest_position - position)

    # 更新位置
    position += velocity

    # 确保位置在合理范围内
    position = np.clip(position, 0, 6000)

    return position, velocity


# 运行算法并打印结果
print("最优解位置:", positions[np.argmin(fitness(positions)[0])])
print("最优解适应度:", fitness(positions[np.argmin(fitness(positions)[0])]))