import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 假设这是你的数据集
data = pd.read_excel(r"数据表单1.xlsx")

# 分割数据集为训练集和测试集
X = data[['纹饰', '类型', '颜色']]
y = data['表面风化']  # 确保列名正确
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 创建一个ColumnTransformer，用于对分类变量进行编码
preprocessor = ColumnTransformer(
    transformers=[
        ('ohe', OneHotEncoder(), ['纹饰', '类型', '颜色'])
    ]
)

# 创建一个逻辑回归模型
logreg = LogisticRegression(max_iter=1000)  # 可能需要增加迭代次数以确保收敛

# 创建一个Pipeline，先进行数据编码，然后进行逻辑回归训练
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', logreg)])

# 训练模型
pipeline.fit(X_train, y_train)

# 测试模型
score = pipeline.score(X_test, y_test)
print(f'Model accuracy: {score:.2f}')

# 获取OneHot编码后的列名
encoded_feature_names = preprocessor.named_transformers_['ohe'].get_feature_names_out(input_features=['纹饰', '类型', '颜色'])

# 获取模型系数
coefficients = pipeline.named_steps["classifier"].coef_

# 打印每个特征类别的系数大小
for orig_feature in ['纹饰', '类型', '颜色']:
    # 找到每个特征类别对应的系数索引
    feature_indices = [i for i, name in enumerate(encoded_feature_names) if name.startswith(orig_feature)]
    # 获取对应特征类别的系数
    feature_coefficients = coefficients[0, feature_indices]
    # 找到系数绝对值最大的索引
    max_index = np.argmax(np.abs(feature_coefficients))
    # 获取最大系数的值和对应的OneHot编码特征名
    max_coefficient = feature_coefficients[max_index]
    max_feature_name = encoded_feature_names[feature_indices[max_index]]

    print(f"The coefficient for '{orig_feature}' is { feature_coefficients} for feature '{encoded_feature_names}'")
    print(f"The largest coefficient for '{orig_feature}' is {max_coefficient} for feature '{max_feature_name}'")