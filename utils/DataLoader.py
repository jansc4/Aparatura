import bioread
import pandas as pd


"""
Loads data from .acq files using bioread and save them to pandas DataFrame
"""

def load_data(file_path):
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
    return df