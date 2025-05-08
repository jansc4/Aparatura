
import pandas as pd
import matplotlib.pyplot as plt

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