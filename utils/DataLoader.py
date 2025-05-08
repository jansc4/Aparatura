import bioread
import pandas as pd
import os

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
    print(file.name)
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
    print(df.head())
    return df


def mass_load(dir_path):
    extension = ['.acq']
    examinations = []
    files = []

    # Zbieranie plików .acq
    for file_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file_name)
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(file_name)
            if ext.lower() in extension:
                files.append(full_path)

    # Czytelny wydruk znalezionych plików
    if files:
        print("Znalezione pliki .acq:")
        for idx, path in enumerate(files, 1):
            print(f"  {idx}. {path}")
    else:
        print("Nie znaleziono plików .acq w podanym folderze.")

    # Wczytywanie danych z plików
    for path in files:
        print(f"\nWczytywanie danych z pliku: {path}")
        exam = load_data(path)
        examinations.append(exam)

    return examinations
