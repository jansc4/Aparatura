import bioread
import pandas as pd
import matplotlib.pyplot as plt

# Ścieżka do pliku .acq (zmień na własną)
file_path = "C:/Users/jan/Documents/Aparatura - Projekt/legia/jhony/ai.acq"

# Wczytanie pliku .acq
file = bioread.read_file(file_path)

# Inicjalizacja pustych struktur danych
data = {}
duplicats = set()  # Zmieniamy na set, bo sprawdzanie obecności w set jest szybsze
channel_counts = {}  # Słownik do liczenia wystąpień kanałów

# Iteracja przez kanały i zapis danych
for channel in file.channels:
    print(f"Nazwa kanału: {channel.name}, Jednostka: {channel.units}")
    
    if channel.name in duplicats:
        # Jeśli kanał już występuje, licznik go zlicza
        if channel.name not in channel_counts:
            channel_counts[channel.name] = 1
        else:
            channel_counts[channel.name] += 1
        
        # Generujemy nową nazwę kanału z numerem
        new_channel_name = f"{channel.name} {channel_counts[channel.name]}"
        data[new_channel_name] = channel.data  # dane czasowe
    else:
        # Jeśli to pierwszy raz, zapisujemy kanał w słowniku
        data[channel.name] = channel.data  # dane czasowe
        duplicats.add(channel.name)  # Dodajemy nazwę kanału do zestawu

    time = channel.time_index  # Czas (jest identyczny dla wszystkich kanałów)


# Tworzenie DataFrame z danymi i czasem
df = pd.DataFrame(data)
df['Czas [s]'] = time
df = df.set_index('Czas [s]')

# Podgląd pierwszych wierszy
print(df.head())

# --- Rysowanie wykresów ---

# Szukamy nazw zawierających "EMG" i "PPG"
emg_channels = [col for col in df.columns if "EMG" in col]
ppg_channels = [col for col in df.columns if "PPG" in col]
res_channels = [col for col in df.columns if "Respiration" in col]

print(emg_channels)


# Rysujemy EMG
plt.figure(figsize=(12, 4))
for emg in emg_channels:
    plt.plot(df.index, df[emg], label=emg)
plt.title("Sygnały EMG")
plt.xlabel("Czas [s]")
plt.ylabel("mV")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Rysujemy PPG
plt.figure(figsize=(12, 4))
for ppg in ppg_channels:
    plt.plot(df.index, df[ppg], label=ppg, color='r')
plt.title("Sygnał PPG")
plt.xlabel("Czas [s]")
plt.ylabel("mV")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
