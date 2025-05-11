
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as hp
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

def draw_plots(df):

    # Szukamy nazw zawierających "EMG" i "PPG"
    emg_channels = [col for col in df.columns if "EMG" in col]
    ppg_channels = [col for col in df.columns if "PPG" in col]
    res_channels = [col for col in df.columns if "Respiration" in col]

    #print(emg_channels)

    for emg in emg_channels:
    # Rysujemy EMG
        plt.figure(figsize=(12, 4))
        plt.plot(df.index, df[emg], label=emg)
        plt.title("Sygnały EMG")
        plt.xlabel("Czas [s]")
        plt.ylabel("mV")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show(block=False)

    for ppg in ppg_channels:
    # Rysujemy PPG
        plt.figure(figsize=(12, 4))
        plt.plot(df.index, df[ppg], label=ppg, color='r')
        plt.title("Sygnał PPG")
        plt.xlabel("Czas [s]")
        plt.ylabel("mV")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show(block=False)


    for res in res_channels:
    # Rysujemy EMG
        plt.figure(figsize=(12, 4))
        plt.plot(df.index, df[res], label=res, color='g')
        plt.title("Sygnały respiracji")
        plt.xlabel("Czas [s]")
        plt.ylabel("mV")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()
        
        
def heartrate_analisis(data, fs, basic_plot=True, poincare_plot=True):
    # Analiza
    wd, m = hp.process(data['PPG (Pulse)'].values, sample_rate=fs, calc_freq=True)

    if basic_plot:
        # Wyświetlenie wyników
        hp.plotter(wd, m)
    if poincare_plot:
        hp.plot_poincare(wd, m)
    # Wydrukuj wyniki
    for k, v in m.items():
        print(f"{k}: {v:.2f}")
    return wd, m
        
def plot_respiratory_with_peaks(data, peaks):
    plt.figure(figsize=(12, 4))
    plt.plot(data.index, data['Respiration'], label='Sygnał oddechowy')
    plt.plot(data.index[peaks], data['Respiration'].iloc[peaks], 'rx', label='Szczyty')
    plt.xlabel('Czas [s]')
    plt.ylabel('Amplituda')
    plt.title('Sygnał oddechowy z wykrytymi szczytami')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_respiratory_intervals(intervals):
    plt.figure(figsize=(10, 3))
    plt.plot(intervals, marker='o')
    plt.title("Odstępy między szczytami oddechowymi")
    plt.xlabel("Nr oddechu")
    plt.ylabel("Czas trwania [s]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def respiratory_analysis(data, fs, basic_plot=True, variability_plot=True):
    # Wykrycie szczytów
    peaks, _ = find_peaks(data['Respiration'], distance=fs/2, prominence=0.2)

    if len(peaks) == 0:
        print("Nie wykryto szczytów w sygnale oddechowym.")
        return None

    # Wykres sygnału z oznaczonymi szczytami
    if basic_plot:
        plot_respiratory_with_peaks(data, peaks)

    # Obliczenia
    czas_trwania_s = len(data['Respiration']) / fs
    czestosc_oddechow = len(peaks) / (czas_trwania_s / 60)
    print(f"Średnia częstość oddechu: {czestosc_oddechow:.2f} oddechów/min")

    # Zmienność oddechowa
    time_peaks = data.index[peaks]
    intervals = np.diff(time_peaks)

    mean_interval = np.mean(intervals)
    sd_interval = np.std(intervals)
    cv_interval = (sd_interval / mean_interval) * 100  # %

    print(f"Średni odstęp między oddechami: {mean_interval:.2f} s")
    print(f"Odchylenie standardowe odstępów: {sd_interval:.2f} s")
    print(f"Współczynnik zmienności: {cv_interval:.2f} %")

    if variability_plot:
        plot_respiratory_intervals(intervals)

    return {
        "czestosc_oddechow": czestosc_oddechow,
        "mean_interval": mean_interval,
        "sd_interval": sd_interval,
        "cv_interval": cv_interval,
        "peaks": peaks,
        "intervals": intervals
    }
        
def bandpass_emg(data, fs):
    lowcut = 20.0
    highcut = 450.0
    nyq = 0.5 * fs
    b, a = butter(4, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, data)

def bandpass_resp(data, fs):
    lowcut = 0.05
    highcut = 1.0
    nyq = 0.5 * fs
    b, a = butter(2, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, data)

def bandpass_ppg(data, fs):
    lowcut = 0.5
    highcut = 5.0
    nyq = 0.5 * fs
    b, a = butter(2, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, data)