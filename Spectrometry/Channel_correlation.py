import numpy

import numpy as np
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
from matplotlib import ticker

spectrum_df = pd.read_csv(r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Data\Spectrum'
                          r'\20220210_Calibration_isotope\U1-2-3-4(timeshift -2)_coord_clear_unite.txt',
                          delimiter='\t')
out_df = spectrum_df[['LON', 'LAT', 'ALT', 'DATETIME']]
correlation_df = pd.DataFrame()

raster_dataset_tot = rasterio.open(r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Aerogeo\WGS84\tot.tif')
raster_dataset_U = rasterio.open(r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Aerogeo\WGS84\U.tif')
raster_dataset_Th = rasterio.open(r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Aerogeo\WGS84\Th.tif')
raster_dataset_K = rasterio.open(r'F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Aerogeo\WGS84\K.tif')
raster_tot = raster_dataset_tot.read(1)
raster_U = raster_dataset_U.read(1)
raster_Th = raster_dataset_Th.read(1)
raster_K = raster_dataset_K.read(1)

spectrum_matr = np.zeros((len(spectrum_df), 1023), dtype=numpy.int32)

tot_list = []
U_list = []
Th_list = []
K_list = []

for row in spectrum_df.iterrows():
    tot_list.append(raster_tot[raster_dataset_tot.index(row[1]['LON'], row[1]['LAT'])])
    U_list.append(raster_U[raster_dataset_U.index(row[1]['LON'], row[1]['LAT'])])
    Th_list.append(raster_Th[raster_dataset_Th.index(row[1]['LON'], row[1]['LAT'])])
    K_list.append(raster_K[raster_dataset_K.index(row[1]['LON'], row[1]['LAT'])])
    spectre = row[1]['spectre'].split(';')
    for i in range(0, 1023):
        spectrum_matr[row[0]][i] = int(spectre[i])

out_df.insert(4, 'aero_tot', tot_list)
out_df.insert(5, 'aero_U', U_list)
out_df.insert(6, 'aero_Th', Th_list)
out_df.insert(7, 'aero_K', K_list)

out_df.to_csv('aero_data.txt', sep='\t')
spectrum_matr_df = pd.DataFrame(spectrum_matr)

tot_corr = np.zeros(1023)
U_corr = np.zeros(1023)
Th_corr = np.zeros(1023)
K_corr = np.zeros(1023)

for i in range(1023):
    tot_corr[i] = out_df['aero_tot'].corr(spectrum_matr_df[i])
    U_corr[i] = out_df['aero_U'].corr(spectrum_matr_df[i])
    Th_corr[i] = out_df['aero_Th'].corr(spectrum_matr_df[i])
    K_corr[i] = out_df['aero_K'].corr(spectrum_matr_df[i])

correlation_df.insert(0, 'tot', tot_corr)
correlation_df.insert(1, 'U', U_corr)
correlation_df.insert(2, 'Th', Th_corr)
correlation_df.insert(3, 'K', K_corr)

correlation_df.to_csv('correlation.txt', sep='\t')

x = correlation_df.index.values
y = correlation_df['tot']
fig, ax = plt.subplots()
ax.plot(x, y, color = 'r', linewidth = 1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
fig.set_figwidth(60)
fig.set_figheight(8)
ax.grid()
plt.savefig('corr_tot.png')
plt.show()

x = correlation_df.index.values
y = correlation_df['U']
fig, ax = plt.subplots()
ax.plot(x, y, color = 'r', linewidth = 1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
fig.set_figwidth(60)
fig.set_figheight(8)
ax.grid()
plt.savefig('corr_U.png')
plt.show()

x = correlation_df.index.values
y = correlation_df['Th']
fig, ax = plt.subplots()
ax.plot(x, y, color = 'r', linewidth = 1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
fig.set_figwidth(60)
fig.set_figheight(8)
ax.grid()
plt.savefig('corr_Th.png')
plt.show()

x = correlation_df.index.values
y = correlation_df['K']
fig, ax = plt.subplots()
ax.plot(x, y, color = 'r', linewidth = 1)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
fig.set_figwidth(60)
fig.set_figheight(8)
ax.grid()
plt.savefig('corr_K.png')
plt.show()

x = correlation_df.index.values
fig, ax = plt.subplots()
ax.plot(x, correlation_df[['tot', 'U', 'Th', 'K']], linewidth = 1)
ax.legend(['tot', 'U', 'Th', 'K'])
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
fig.set_figwidth(60)
fig.set_figheight(8)
ax.grid()
plt.savefig('all.png')
plt.show()

x = correlation_df.index.values
fig, ax = plt.subplots()
ax.plot(x, correlation_df[['U', 'Th']], linewidth = 1)
ax.legend(['U', 'Th'])
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
fig.set_figwidth(60)
fig.set_figheight(8)
ax.grid()
plt.savefig('U_Th.png')
plt.show()