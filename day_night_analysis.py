# Nhập các thư viện cần thiết
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Đọc dữ liệu đã làm sạch
df = pd.read_csv('Cleaned_Data.csv')

# Tạo cột chỉ thị ngày/đêm dựa trên thời gian
df['Hour'] = (df['Time'] % 24)  # Lấy giờ trong ngày
df['Day_Night'] = np.where((df['Hour'] >= 6) & (df['Hour'] < 18), 'Day', 'Night')

# Nhóm theo ngày và ngày/đêm để tính nhiệt độ trung bình
df['Day'] = (df['Time'] // 24).astype(int)  # Ngày thứ mấy
day_night_means = df.groupby(['Day', 'Day_Night'])['Temperature'].mean().unstack()

# Tính trung bình ngày/đêm qua 7 ngày
day_mean = day_night_means['Day'].mean()
night_mean = day_night_means['Night'].mean()

# Thực hiện t-test để so sánh ngày và đêm
day_data = df[df['Day_Night'] == 'Day']['Temperature']
night_data = df[df['Day_Night'] == 'Night']['Temperature']
t_stat, p_value = ttest_ind(day_data, night_data)

# In kết quả
print(f"Nhiệt độ trung bình ban ngày: {day_mean:.2f} °C")
print(f"Nhiệt độ trung bình ban đêm: {night_mean:.2f} °C")
print(f"Kiểm tra t-test: t = {t_stat:.2f}, p-value = {p_value:.4f}")

# Lưu kết quả vào file CSV
day_night_means.to_csv('Day_Night_Means.csv')