import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv('Data.csv')

# Làm sạch cột Temperature: chuyển sang số, loại bỏ giá trị không hợp lệ
df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
df = df.dropna(subset=['Temperature'])  # Loại bỏ các hàng có Temperature là NaN

# Tạo mảng thời gian giả định (mỗi điểm cách 10 phút = 1/6 giờ)
df['Time'] = np.arange(0, len(df) * 10/60, 10/60)  # Thời gian tính bằng giờ

# Lưu dữ liệu đã làm sạch vào file CSV mới
df.to_csv('Cleaned_Data.csv', index=False)

# In thông tin dữ liệu đã làm sạch
print(f"Số lượng điểm dữ liệu sau khi làm sạch: {len(df)}")
print(df.head())