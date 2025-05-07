import pandas as pd
from Dataclass import Badanie,Channel


def wczytaj_i_przetworz_dane(sciezka_pliku: str) -> Badanie:
    with open(sciezka_pliku, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    name = lines[0]  # ai.acq
    sample_rate_line = lines[1]  # "1 msec/sample"
    sample_rate = float(sample_rate_line.split()[0]) / 1000  # msec -> sec

    num_channels = int(lines[2].split()[0])  # "4 channels"

    # Teraz odczytujemy nazwy i jednostki kanałów
    channel_names = [lines[3 + i * 2] for i in range(num_channels)]
    channel_units = [lines[4 + i * 2] for i in range(num_channels)]

    # Dane zaczynają się po nagłówku CH1, CH2, itd.
    header_index = 3 + num_channels * 2 + 1
    data_lines = lines[header_index + 1:]

    # Wczytaj dane do DataFrame
    data = pd.read_csv(
        sciezka_pliku,
        sep='\t',
        skiprows=header_index + 1,
        names=["time"] + [f"CH{i+1}" for i in range(num_channels)],
        engine="python"
    )

    # Tworzymy obiekty Channel
    channels = []
    for i in range(num_channels):
        col = f"CH{i+1}"
        ch = Channel(
            name=channel_names[i],
            unit=channel_units[i],
            data=data[col].dropna().tolist()
        )
        channels.append(ch)

    badanie = Badanie(
        name=name,
        sample_rate=sample_rate,
        channels=channels
    )

    return badanie


badanie1 = wczytaj_i_przetworz_dane("C:\\Users\\jan\\Documents\\Aparatura - Projekt\\legia\\jhony\\ai.txt")
print(badanie1.name)