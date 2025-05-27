# Nhập các thư viện cần thiết
import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq

# Đọc dữ liệu đã làm sạch
df = pd.read_csv('Cleaned_Data.csv')

# Lấy dữ liệu nhiệt độ và thời gian
temperature = df['Temperature'].values
n = len(temperature)
sample_rate = 6  # 6 mẫu mỗi giờ (10 phút/mẫu)

# Thực hiện FFT
fft_vals = fft(temperature)
fft_freq = fftfreq(n, 1/sample_rate)

# Lấy tần số dương và biên độ tương ứng
positive_freqs = fft_freq[:n//2]
amplitudes = np.abs(fft_vals)[:n//2] * 2 / n

# Chuyển tần số thành chu kỳ (giờ)
periods = 1 / positive_freqs[positive_freqs > 0]  # Chỉ lấy tần số dương
amplitudes = amplitudes[positive_freqs > 0]

# Tìm chu kỳ chính (~24 giờ) và ultradian (<24 giờ)
circadian_idx = np.argmin(np.abs(periods - 24))  # Tìm chu kỳ gần 24 giờ
ultradian_periods = periods[periods < 24]
ultradian_amplitudes = amplitudes[periods < 24]

# In kết quả
print(f"Chu kỳ circadian (~24 giờ): {periods[circadian_idx]:.2f} giờ, Biên độ: {amplitudes[circadian_idx]:.2f}")
print("Các chu kỳ ultradian nổi bật (<24 giờ):")
for period, amp in zip(ultradian_periods[:5], ultradian_amplitudes[:5]):  # In 5 chu kỳ đầu
    print(f"Chu kỳ: {period:.2f} giờ, Biên độ: {amp:.2f}")

# Lưu phổ tần số vào file CSV
fft_df = pd.DataFrame({'Period': periods, 'Amplitude': amplitudes})
fft_df.to_csv('FFT_Results.csv', index=False)