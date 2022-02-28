import matplotlib.pyplot as plt
import numpy as np
import util

def histogram_snr(SNR, city):
    signal = SNR[np.nonzero(SNR)]
    plt.hist(signal)
    plt.xlabel('SNR (dB)')
    plt.ylabel('Number of users')
    plt.title(f'SNR distribution in {city}')
    plt.show()
    print(f'SNR:{np.min(signal)}-{np.max(signal)} dB, average is {util.average(signal)} dB')

def degree_bs(links, city):
    degrees = sum(links)
    plt.hist(degrees)
    plt.xlabel('Number of connections per BS')
    plt.ylabel('Number of BSs')
    plt.title(f'BS degree in {city}')
    plt.show()
    print(f'Number of connections per BS:{np.min(degrees)}-{np.max(degrees)}, average is {util.average(degrees)}')

def degree_user(links, city):
    degrees = sum(np.transpose(links))
    plt.hist(degrees)
    plt.xlabel('Number of connections per user')
    plt.ylabel('Number of users')
    plt.title(f'User degree in {city}')
    plt.show()