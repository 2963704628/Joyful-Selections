import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
# 假设Excel文件的第一行为周标识，第一列为转运商ID
file_path = "C:\\Users\\86159\\Desktop\\data.xlsx"
data = pd.read_excel(file_path, header=0, index_col=0)


# 假设 data 是包含时间序列数据的 DataFrame
# 选择一个转运商的数据，例如 'T1'
column_name = 'T8'
time_series_data = data[column_name].dropna()

# 如果索引不是日期时间格式，您可以重置索引
time_series_data_reset = time_series_data.reset_index(drop=True)

# 拟合ARMA模型，这里使用(1,0,1)作为示例
model = ARIMA(time_series_data_reset, order=(1, 0, 1))
fitted_model = model.fit()

# 使用模型进行预测
forecast_steps = 24
forecast = fitted_model.get_forecast(steps=forecast_steps)
forecast_values = forecast.predicted_mean
confidence_intervals = forecast.conf_int()

# 为预测结果设置索引（例如，使用整数索引）
forecast_index = pd.RangeIndex(start=len(time_series_data_reset), stop=len(time_series_data_reset) + forecast_steps)
# 绘制历史数据和预测结果
plt.figure(figsize=(12, 6))
plt.plot(time_series_data_reset.index, time_series_data_reset, label='Historical Loss Rate')
plt.plot(forecast_values.index, forecast_values, label='Forecasted Loss Rate', linestyle='--')
plt.fill_between(forecast_values.index, confidence_intervals.iloc[:, 0], confidence_intervals.iloc[:, 1], color='grey', alpha=0.2)
plt.legend()
plt.title('ARMA Model Forecast for Transporter T8')
plt.xlabel('Week')
plt.ylabel('Loss Rate')
plt.show()