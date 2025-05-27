# Nhập các thư viện cần thiết
import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq

# Đọc dữ liệu đã làm sạch
df = pd.read_csv('Cleaned_Data.csv')

# Kiểm tra biên độ chu kỳ 24 giờ
temperature = df['Temperature'].values
n = len(temperature)
sample_rate = 6  # 6 mẫu mỗi giờ
fft_vals = fft(temperature)
fft_freq = fftfreq(n, 1/sample_rate)
positive_freqs = fft_freq[:n//2]
amplitudes = np.abs(fft_vals)[:n//2] * 2 / n
periods = 1 / positive_freqs[positive_freqs > 0]
amplitudes = amplitudes[positive_freqs > 0]
circadian_idx = np.argmin(np.abs(periods - 24))
circadian_amplitude = amplitudes[circadian_idx]

# Tạo cột Day và tính độ lệch chuẩn mỗi ngày
df['Day'] = (df['Time'] // 24).astype(int)
daily_std = df.groupby('Day')['Temperature'].std()

# Xác định số ngày thực tế
num_days = df['Day'].max() + 1
print(f"Số ngày trong dữ liệu: {num_days}")

# Phân tích biên độ chu kỳ 24 giờ cho từng ngày
daily_peaks = []
for day in range(num_days):
    day_data = df[df['Day'] == day]['Temperature']
    if len(day_data) < 24 * sample_rate:  # Kiểm tra nếu ngày không đủ 24 giờ
        print(f"Ngày {day} không đủ dữ liệu ({len(day_data)} mẫu), bỏ qua FFT.")
        daily_peaks.append(np.nan)  # Thêm giá trị NaN nếu không đủ dữ liệu
        continue
    fft_vals_day = fft(day_data)
    fft_freq_day = fftfreq(len(day_data), 1/sample_rate)
    positive_freqs_day = fft_freq_day[:len(day_data)//2]
    amplitudes_day = np.abs(fft_vals_day)[:len(day_data)//2] * 2 / len(day_data)
    periods_day = 1 / positive_freqs_day[positive_freqs_day > 0]
    circadian_idx_day = np.argmin(np.abs(periods_day - 24))
    daily_peaks.append(amplitudes_day[circadian_idx_day])

# Kiểm tra rối loạn
if circadian_amplitude < 0.5:  # Ngưỡng giả định
    print("Cảnh báo: Biên độ chu kỳ 24 giờ thấp, có thể có rối loạn nhịp sinh học.")
if daily_std.max() > 2 * daily_std.mean():  # Ngày bất thường nếu std gấp đôi trung bình
    print(f"Ngày bất thường (độ lệch chuẩn cao): {daily_std.idxmax()}")
if len(daily_peaks) > 1 and np.nanstd(daily_peaks) > 0.3:  # Ngưỡng giả định cho sự không đồng đều
    print("Cảnh báo: Chu kỳ 24 giờ không lặp lại đồng đều qua các ngày.")

# Tạo DataFrame với độ dài phù hợp
results = pd.DataFrame({
    'Day': range(num_days),
    'Circadian_Amplitude': daily_peaks,
    'Daily_Std': daily_std.values[:num_days]  # Cắt bớt nếu daily_std dài hơn
})
results.to_csv('Circadian_Analysis.csv', index=False)

# In thông tin để kiểm tra
print(f"Độ dài daily_peaks: {len(daily_peaks)}")
print(f"Độ dài daily_std: {len(daily_std)}")
print(results)