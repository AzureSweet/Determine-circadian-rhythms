# Nhập các thư viện cần thiết
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Đọc dữ liệu đã làm sạch
df = pd.read_csv('Cleaned_Data.csv')

# Biểu đồ 1: Dòng thời gian nhiệt độ
plt.figure(figsize=(12, 6))
plt.plot(df['Time'], df['Temperature'], label='Nhiệt độ cơ thể')
for day in range(1, 8):
    plt.axvspan((day-1)*24+6, (day-1)*24+18, alpha=0.2, color='yellow', label='Ngày' if day == 1 else '')
    plt.axvspan((day-1)*24+18, day*24+6, alpha=0.2, color='blue', label='Đêm' if day == 1 else '')
plt.xlabel('Thời gian (giờ)')
plt.ylabel('Nhiệt độ (°C)')
plt.title('Dòng thời gian nhiệt độ cơ thể qua 7 ngày')
plt.legend()
plt.savefig('Temperature_Timeseries.png')
plt.close()

# Biểu đồ 2: Phổ tần số
temperature = df['Temperature'].values
n = len(temperature)
sample_rate = 6
fft_vals = fft(temperature)
fft_freq = fftfreq(n, 1/sample_rate)
positive_freqs = fft_freq[:n//2]
amplitudes = np.abs(fft_vals)[:n//2] * 2 / n
periods = 1 / positive_freqs[positive_freqs > 0]
amplitudes = amplitudes[positive_freqs > 0]

plt.figure(figsize=(12, 6))
plt.plot(periods, amplitudes, label='Biên độ')
plt.axvline(24, color='red', linestyle='--', label='Chu kỳ 24 giờ')
plt.xlabel('Chu kỳ (giờ)')
plt.ylabel('Biên độ')
plt.title('Phổ tần số của nhiệt độ cơ thể')
plt.legend()
plt.xlim(0, 48)  # Giới hạn để tập trung vào các chu kỳ ngắn
plt.savefig('Frequency_Spectrum.png')
plt.close()

# Biểu đồ 3: So sánh ngày/đêm
df['Hour'] = (df['Time'] % 24)
df['Day_Night'] = np.where((df['Hour'] >= 6) & (df['Hour'] < 18), 'Day', 'Night')
df['Day'] = (df['Time'] // 24).astype(int)
day_night_means = df.groupby(['Day', 'Day_Night'])['Temperature'].mean().unstack()

plt.figure(figsize=(8, 6))
day_night_means.mean().plot(kind='bar', color=['yellow', 'blue'])
plt.ylabel('Nhiệt độ trung bình (°C)')
plt.title('So sánh nhiệt độ trung bình ngày và đêm')
plt.savefig('Day_Night_Comparison.png')
plt.close()

# Highlight thú vị: Tìm chu kỳ ultradian mạnh nhất
ultradian_periods = periods[periods < 24]
ultradian_amplitudes = amplitudes[periods < 24]
strongest_ultradian = ultradian_periods[np.argmax(ultradian_amplitudes)]
print(f"Chu kỳ ultradian mạnh nhất là {strongest_ultradian:.2f} giờ với biên độ {max(ultradian_amplitudes):.2f}")