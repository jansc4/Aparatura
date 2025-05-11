import utils.DataLoader as dl
import utils.BiopackAnalisis as ba
import heartpy as hp
import matplotlib.pyplot as plt
import numpy as np

path = "C:/Users/jan/Documents/Aparatura - Projekt/legia/jhony/ai.acq"

#badanie = dl.load_data(path)
#ba.draw_plots(badanie)

badania = dl.mass_load("C:/Users/jan/Documents/Aparatura - Projekt/legia/jhony")

ba.draw_plots(badania[3])

data = badania[0]
sample_rate = 1000  # Hz – dostosuj do swojego sygnału

_, _ = ba.heartrate_analisis(data, sample_rate)
badania_filtr = data.copy()
badania_filtr['PPG (Pulse)'] = ba.bandpass_ppg(badania_filtr['PPG (Pulse)'], sample_rate)
badania_filtr['EMG (5 - 500 Hz)'] = ba.bandpass_emg(badania_filtr['EMG (5 - 500 Hz)'], sample_rate)
badania_filtr['EMG (5 - 500 Hz) 1'] = ba.bandpass_emg(badania_filtr['EMG (5 - 500 Hz) 1'], sample_rate)
badania_filtr['Respiration'] = ba.bandpass_resp(badania_filtr['Respiration'], sample_rate)
ba.draw_plots(badania_filtr)
_, _ = ba.heartrate_analisis(badania_filtr, sample_rate)

_ = ba.respiratory_analysis(badania_filtr, sample_rate)

