import contextlib
import numpy as np
import matplotlib.pyplot as plt
import struct
import wave


# funkcja do czytania próbek z pliku wav
def read_samples(wave_file, nb_frames):
    frame_data = wave_file.readframes(nb_frames)
    if frame_data:
        sample_width = wave_file.getsampwidth()
        nb_samples = len(frame_data) // sample_width
        format = {1: "%dB", 2: "<%dh", 4: "<%dl"}[sample_width] % nb_samples
        return struct.unpack(format, frame_data)
    else:
        return ()


def FFT(dane, rozmiar, fs, Fsd):
    # transformata fouriera na próbkach
    wyniki_fft = np.fft.fft(dane, rozmiar)

    # zapisanie wyników transformaty do pliku wynikiFFT.txt
    with open("wynikiFFT.txt", "w") as f:
        for wynik in wyniki_fft:
            f.write(str(wynik) + "\n")

    # obliczamy moduł zespolonej wartości co daje widmo amplitudowe
    widmo_amp = np.abs(wyniki_fft)

    f = np.fft.fftfreq(rozmiar, 1 / fs)

    # rysujemy wykres widma
    plt.plot(f, widmo_amp)
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Amplituda widma')
    plt.title('Widmo')
    plt.xlim((0, Fsd/2))
    plt.yscale("log")
    plt.show()


def zbadaj(plik, fftN, D):

    # obliczenie danych sygnału wejściowego
    with contextlib.closing(wave.open(plik, "r")) as s:
        oryginalna_liczba_probek = s.getnframes()
        fs = s.getframerate()

    liczba_probek = int(oryginalna_liczba_probek / D)

    if fftN == -1:
        fftN = liczba_probek

    df = fs / fftN

    Fsd = fs / D

    print("FFT N: " + str(fftN))
    print("df: " + str(df))
    print("D: " + str(D))
    print("Fsd: " + str(Fsd))

    # odczytanie próbek z pliku wav
    probki = read_samples(wave.open(plik, "rb"), oryginalna_liczba_probek)

    poDecymacji = []

    for i, probka in enumerate(probki):
        if i % D == 0:
            poDecymacji.append(probka)

    print("Liczba probek po decymacji: " + str(len(poDecymacji)))

    FFT(poDecymacji, fftN, fs, Fsd)


if __name__ == "__main__":
    N1 = 1024
    N2 = 2048
    N3 = 4096
    NMAX = -1

    zbadaj("signal.wav", NMAX, 1)
