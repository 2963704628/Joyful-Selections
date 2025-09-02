import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_excel


# 定义激活函数及其导数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# 定义BPNN类
class BPNN:
    def __init__(self, num_in, num_hidden, num_out):
        self.num_in = num_in  # 输入层节点数
        self.num_hidden = num_hidden  # 隐藏层节点数
        self.num_out = num_out  # 输出层节点数

        # 初始化权重矩阵和偏置，确保权重矩阵的行数与输入特征数量相匹配
        self.weights_input_hidden = np.random.randn(num_in, num_hidden)
        self.weights_hidden_output = np.random.randn(num_hidden, num_out)
        self.bias_hidden = np.zeros((1, num_hidden))
        self.bias_output = np.zeros((1, num_out))



    def backpropagation(self, targets, outputs, learning_rate):
        # 反向传播
        output_errors = targets - outputs
        output_delta = output_errors * sigmoid_derivative(outputs)
        hidden_errors = np.dot(output_delta, self.weights_hidden_output.T)
        hidden_delta = hidden_errors * sigmoid_derivative(self.hidden_layer)

        # 权重和偏置更新
        self.weights_hidden_output += np.dot(self.hidden_layer.T, output_delta) * learning_rate
        self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
        self.weights_input_hidden += np.dot(self.inputs.T, hidden_delta) * learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

        return np.mean(np.abs(output_errors))  # 返回误差

    def train(self, patterns, iterations, learning_rate):
        for i in range(iterations):
            total_error = 0
            for inputs, targets in patterns:
                # 确保inputs是二维数组
                if inputs.ndim == 1:
                    inputs = inputs.reshape(1, -1)

                outputs = self.feedforward(inputs)
                error = self.backpropagation(inputs, targets, learning_rate)
                total_error += error

            if i % 1000 == 0:
                print(f'Iteration {i}, Error: {total_error / len(patterns)}')

    def feedforward(self, inputs):
        # 前向传播
        self.inputs = inputs
        # 添加一行代码以添加偏置项
        inputs_with_bias = np.hstack((np.ones((inputs.shape[0], 1)), inputs))
        self.hidden_layer = sigmoid(np.dot(inputs_with_bias, self.weights_input_hidden) + self.bias_hidden)
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.weights_hidden_output) + self.bias_output)
        return self.output_layer
    def update(self, inputs):
        # 使用当前权重和偏置进行预测
        return self.feedforward(inputs)

# 读取Excel文件并预处理数据
def preprocess_data(excel_data):
    supplier_ids = excel_data.iloc[:, 0].values
    num_suppliers = len(supplier_ids)  # 68家供应商
    num_weeks = excel_data.shape[1] - 1  # 减去供应商ID列
    num_features = num_weeks
    num_output_weeks = 24  # 预测未来24周

    # 将供应量数据转换为numpy数组，并排除供应商ID列
    supply_data = excel_data.iloc[:, 1:].values
    # 重新生成X和y，确保所有供应商的数据都被考虑
    X = supply_data[:, :-num_output_weeks]  # 特征数据，除去最后24周
    y = supply_data[:, -num_output_weeks:]  # 目标数据，仅使用最后24周

    # 归一化特征数据
    X = (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))

    return X, y, num_suppliers, num_features, num_output_weeks

# 调整 create_pattern 函数
def create_pattern(X, y, num_suppliers, num_features, num_output_weeks):
    pattern = []
    for i in range(num_suppliers):
        for j in range(num_output_weeks):
            # 为每个供应商的每个特征创建一个模式
            inputs = X[i, j:num_features]  # 从第j周开始的所有特征
            targets = y[i, j:]  # 从第j周开始的接下来24周的目标供应量
            pattern.append((inputs, targets))
    return pattern


if __name__ == '__main__':
    filename = r"C:/Users/86159/Desktop/最少数量供应商.xlsx"
    excel_data = read_excel(filename)
    X, y, num_suppliers, num_features, num_output_weeks = preprocess_data(excel_data)

    # 调整神经网络的输入层节点数，加上1表示供应商ID或一个额外的偏置项
    n = BPNN(num_features + 1, 20, num_output_weeks)

    # 训练神经网络
    # 注意：create_pattern函数需要返回正确格式的patterns
    patterns = create_pattern(X, y, num_suppliers, num_features, num_output_weeks)
    n.train(patterns, iterations=100000, learning_rate=0.01)

    # 使用最后一周的数据进行预测
    # 注意：这里假设我们使用所有供应商的最后一周数据进行预测
    last_week_data = X[:, -1].reshape(num_suppliers, 1)  # 重塑为二维数组
    predictions = n.update(last_week_data)

    # 可视化预测结果
    # 注意：这里假设predictions是一个二维数组，每行是一个供应商的预测结果
    plt.figure(figsize=(10, 5))
    for i in range(num_output_weeks):  # 预测未来24周
        plt.plot(predictions[:, i], label=f'Week {i + 1}')
    plt.title('Predicted Supply Volume for Next 24 Weeks')
    plt.xlabel('Supplier')
    plt.ylabel('Supply Volume')
    plt.legend()
    plt.show()