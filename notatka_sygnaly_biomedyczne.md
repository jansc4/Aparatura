
# 📊 Praktyczne użycie Pandas, Matplotlib, SciPy, NumPy, Seaborn i HRV w analizie sygnałów biomedycznych

## 🐼 Pandas – analiza danych tabelarycznych

### Importowanie i podstawy:
```python
import pandas as pd

df = pd.read_csv("dane.csv")
print(df.head())
print(df.info())
print(df.describe())
```

### Filtrowanie i manipulacja:
```python
df_filtr = df[df["kanał"] == "EMG"]
df["znormalizowane"] = (df["sygnał"] - df["sygnał"].mean()) / df["sygnał"].std()
df.groupby("pacjent")["sygnał"].mean()
```

---

## 📈 Matplotlib – wykresy i wizualizacja

### Podstawowy wykres:
```python
import matplotlib.pyplot as plt

plt.plot(df["czas"], df["sygnał"])
plt.title("Sygnał EMG")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda [mV]")
plt.grid(True)
plt.show()
```

### Wiele sygnałów:
```python
plt.figure(figsize=(10, 4))
plt.plot(df["czas"], df["emg"], label="EMG")
plt.plot(df["czas"], df["resp"], label="Respiration", alpha=0.7)
plt.legend()
plt.show()
```

---

## 🔬 SciPy – analiza i filtracja sygnału

### Filtrowanie pasmowoprzepustowe:
```python
from scipy.signal import butter, filtfilt

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

fs = 1000  # Hz
filtered_signal = bandpass_filter(df["emg"], 20, 450, fs)
```

### Detekcja szczytów:
```python
from scipy.signal import find_peaks

peaks, _ = find_peaks(df["ppg"], distance=fs*0.6)
plt.plot(df["czas"], df["ppg"])
plt.plot(df["czas"].iloc[peaks], df["ppg"].iloc[peaks], "rx")
plt.title("Detekcja tętna z PPG")
plt.show()
```

---

## 🔢 NumPy – operacje macierzowe i wektorowe

```python
import numpy as np

sygnał = df["emg"].values
rms = np.sqrt(np.mean(sygnał**2))
norm = (sygnał - np.min(sygnał)) / (np.max(sygnał) - np.min(sygnał))
```

---

## 🎨 Seaborn – wizualizacja statystyk

```python
import seaborn as sns

sns.histplot(df["sygnał"], kde=True)
sns.boxplot(data=df, x="kanał", y="sygnał")
```

---

## ❤️ HRV – analiza zmienności rytmu serca

### Z użyciem NeuroKit2:
```python
import neurokit2 as nk

ppg = df["ppg"].values
signals, info = nk.ppg_process(ppg, sampling_rate=fs)
nk.ppg_plot(signals)

# Analiza HRV
hrv = nk.hrv(signals, sampling_rate=fs, show=True)
```

---

## 🔗 Przydatne linki
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [SciPy Signal](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [NumPy Docs](https://numpy.org/doc/)
- [Seaborn Docs](https://seaborn.pydata.org/)
- [NeuroKit2](https://neuropsychology.github.io/NeuroKit/)
