import utils.DataLoader as dl
import utils.BiopackAnalisis as ba


path = "C:/Users/jan/Documents/Aparatura - Projekt/legia/jhony/ai.acq"

badanie = dl.load_data(path)
ba.draw_plots(badanie)
