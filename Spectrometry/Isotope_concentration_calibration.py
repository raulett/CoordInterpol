import numpy as np
import pandas as pd
import geopandas as gpd
#import rasterio
import matplotlib.pyplot as plt
from matplotlib import ticker
import datetime
import os

current_folder = r"F:\YandexDisk\Work\SibGIS\QGisPRJ\20211021_Krasnokamensk_metod\Яхин_данные\radio_40_GK"
calibration_points = gpd.read_file(r"F:\YandexDisk\Work\SibGIS\QGisPRJ\20211021_Krasnokamensk_metod\Яхин_данные\radio_40_GK\radio_40_GK.gpkg", layer='calibration_full')

polynom_U0 = np.polyfit(calibration_points["u0_1_2_609KEv"], calibration_points["Ra_GND"], 1)
print("U_1_2_609 channel regression :{}, pearson: {}.".format(polynom_U0, calibration_points["u0_1_2_609KEv"].corr(calibration_points["Ra_GND"])))

polynom_U1 = np.polyfit(calibration_points["u1_2205KEv"], calibration_points["Ra_GND"], 1)
print("u1_2205KEv channel regression :{}, pearson: {}.".format(polynom_U1, calibration_points["u1_2205KEv"].corr(calibration_points["Ra_GND"])))

polynom_U2 = np.polyfit(calibration_points["u2_1120KEv"], calibration_points["Ra_GND"], 1)
print("u2_1120KEv channel regression :{}, pearson: {}.".format(polynom_U2, calibration_points["u2_1120KEv"].corr(calibration_points["Ra_GND"])))

polynom_U3 = np.polyfit(calibration_points["u3_1760KEv"], calibration_points["Ra_GND"], 1)
print("u3_1760KEv channel regression :{}, pearson: {}.".format(polynom_U3, calibration_points["u3_1760KEv"].corr(calibration_points["Ra_GND"])))

integral = np.polyfit(calibration_points["int_UAV"], calibration_points["MED_GND"], 1)
print("int_UAV channel regression :{}, pearson: {}.".format(integral, calibration_points["int_UAV"].corr(calibration_points["MED_GND"])))

K = np.polyfit(calibration_points["K_UAV"], calibration_points["K_GND"], 1)
print("K_UAV channel regression :{}, pearson: {}.".format(K, calibration_points["K_UAV"].corr(calibration_points["K_GND"])))

th1_910KEv = np.polyfit(calibration_points["th1_910KEv"], calibration_points["Th_GND"], 1)
print("th1_910KEv channel regression :{}, pearson: {}.".format(th1_910KEv, calibration_points["th1_910KEv"].corr(calibration_points["Th_GND"])))

th2_2620KEv = np.polyfit(calibration_points["th2_2620KEv"], calibration_points["Th_GND"], 1)
print("u3_1760KEv channel regression :{}, pearson: {}.".format(th2_2620KEv, calibration_points["th2_2620KEv"].corr(calibration_points["Th_GND"])))
#
# polynom_tot = np.polyfit(calibration_points["int_UAV"], calibration_points["MED_GND"], 1)
# print("total channel regression :{}".format(polynom_tot))
#
# polynom_U = np.polyfit(calibration_points["U_UAV"], calibration_points["Ra_GND"], 1)
# print("U channel regression :{}".format(polynom_U))
#
# polynom_Th = np.polyfit(calibration_points["Th_UAV"], calibration_points["Th_GND"], 1)
# print("Th channel regression :{}".format(polynom_Th))
#
# polynom_K = np.polyfit(calibration_points["K_UAV"], calibration_points["K_GND"], 1)
# print("K channel regression :{}".format(polynom_K))

date_time = datetime.datetime.now()
datetime_str = date_time.strftime('%Y%m%d%H%M%S')
new_folder = current_folder + '\\' + 'regression_channel' + '\\' + datetime_str
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

#u0_1_2_609KEv channel plot
x = calibration_points["u0_1_2_609KEv"]
y = calibration_points["Ra_GND"]
x_line = np.linspace(calibration_points["u0_1_2_609KEv"].min(), calibration_points["u0_1_2_609KEv"].max())
y_line = x_line*polynom_U0[0] + polynom_U0[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("U_1_2_609 channel regression :{}, pearson: {}.".format(polynom_U0, calibration_points["u0_1_2_609KEv"].corr(calibration_points["Ra_GND"])))
plt.xlabel("u0_1_2_609KEv")
plt.ylabel("Ra_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'u0_1_2_609KEv.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#u1_2205KEv channel plot
x = calibration_points["u1_2205KEv"]
y = calibration_points["Ra_GND"]
x_line = np.linspace(calibration_points["u1_2205KEv"].min(), calibration_points["u1_2205KEv"].max())
y_line = x_line*polynom_U1[0] + polynom_U1[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("u1_2205KEv channel regression :{}, pearson: {}.".format(polynom_U1, calibration_points["u1_2205KEv"].corr(calibration_points["Ra_GND"])))
plt.xlabel("u1_2205KEv")
plt.ylabel("Ra_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'u1_2205KEv.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#u2_1120KEv channel plot
x = calibration_points["u2_1120KEv"]
y = calibration_points["Ra_GND"]
x_line = np.linspace(calibration_points["u2_1120KEv"].min(), calibration_points["u2_1120KEv"].max())
y_line = x_line*polynom_U2[0] + polynom_U2[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("u2_1120KEv channel regression :{}, pearson: {}.".format(polynom_U2, calibration_points["u2_1120KEv"].corr(calibration_points["Ra_GND"])))
plt.xlabel("u2_1120KEv")
plt.ylabel("Ra_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'u2_1120KEv.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#U3_1760KEv channel plot
x = calibration_points["u3_1760KEv"]
y = calibration_points["Ra_GND"]
x_line = np.linspace(calibration_points["u3_1760KEv"].min(), calibration_points["u3_1760KEv"].max())
y_line = x_line*polynom_U3[0] + polynom_U3[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("u3_1760KEv channel regression :{}, pearson: {}.".format(polynom_U3, calibration_points["u3_1760KEv"].corr(calibration_points["Ra_GND"])))
plt.xlabel("U3_1760KEv")
plt.ylabel("Ra_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'U3_1760KEv.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#K_UAV channel plot
x = calibration_points["K_UAV"]
y = calibration_points["K_GND"]
x_line = np.linspace(calibration_points["K_UAV"].min(), calibration_points["K_UAV"].max())
y_line = x_line*K[0] + K[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("K_UAV channel regression :{}, pearson: {}.".format(K, calibration_points["K_UAV"].corr(calibration_points["K_GND"])))
plt.xlabel("K_UAV")
plt.ylabel("K_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'K_UAV.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#th1_910KEv channel plot
x = calibration_points["th1_910KEv"]
y = calibration_points["Th_GND"]
x_line = np.linspace(calibration_points["th1_910KEv"].min(), calibration_points["th1_910KEv"].max())
y_line = x_line*th1_910KEv[0] + th1_910KEv[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("th1_910KEv channel regression :{}, pearson: {}.".format(th1_910KEv, calibration_points["th1_910KEv"].corr(calibration_points["Th_GND"])))
plt.xlabel("th1_910KEv")
plt.ylabel("Th_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'th1_910KEv.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#th2_2620KEv channel plot
x = calibration_points["th2_2620KEv"]
y = calibration_points["Th_GND"]
x_line = np.linspace(calibration_points["th2_2620KEv"].min(), calibration_points["th2_2620KEv"].max())
y_line = x_line*th2_2620KEv[0] + th2_2620KEv[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("th2_2620KEv channel regression :{}, pearson: {}.".format(th2_2620KEv, calibration_points["th2_2620KEv"].corr(calibration_points["Th_GND"])))
plt.xlabel("th2_2620KEv")
plt.ylabel("Th_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'th2_2620KEv.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#int_UAV channel plot
x = calibration_points["int_UAV"]
y = calibration_points["MED_GND"]
x_line = np.linspace(calibration_points["int_UAV"].min(), calibration_points["int_UAV"].max())
y_line = x_line*integral[0] + integral[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("int_UAV channel regression :{}, pearson: {}.".format(integral, calibration_points["int_UAV"].corr(calibration_points["MED_GND"])))
plt.xlabel("int_UAV")
plt.ylabel("MED_GND")
ax.grid()
plt.savefig(new_folder + '\\' + 'int_UAV.png', dpi=800)
plt.show()

k = 2.73958333
b = 25.66666667

# u0_1_2_609KEv = (int(k * 609 + b), int(k * 650 + b)) #609 1/2 пика
# u1_2205KEv = (int(k * 2035 + b), int(k * 2280 + b)) #корректировка по графику 2.2
# u2_1120KEv = (int(k*1055+b), int(k*1300+b)) #1120/ 2пика 7 и 8
# u3_1760KEv = (int(k*1670+b), int(k*1830+b)) #1,76
# th1_910KEv = (int(k*875+b), int(k*1010+b)) #935
# th2_2620KEv = (int(k*2356+b), int(k*2480+b)) #2.4
# K = (int(k*1340+b), int(k*1535+b)) #1459 K40
# integral = (int(k*400+b), int(k*2810+b))
u0_1_2_609KEv = (int(k * 607 + b), int(k * 664 + b))  # 609 1/2 пика
u1_2205KEv = (int(k * 2025 + b), int(k * 2300 + b))  # корректировка по графику 2.2
u2_1120KEv = (int(k * 1050 + b), int(k * 1305 + b))  # 1120/ 2пика 7 и 8
u3_1760KEv = (int(k * 1670 + b), int(k * 1835 + b))  # 1,76
th1_910KEv = (int(k * 870 + b), int(k * 1010 + b))  # 910
th2_2620KEv = (int(k * 2510 + b), int(k * 2670 + b))  # 2.4 переделать 2.62
K = (int(k * 1340 + b), int(k * 1535 + b))  # 1459 K40
integral = (int(k * 400 + b), int(k * 2810 + b))


calibration_df = pd.read_csv(r"F:\YandexDisk\Work\SibGIS\QGisPRJ\20211021_Krasnokamensk_metod\Data\Spectrum\Spectrum\KrasnokamSpectr\Spectr40m\calibration_spectre.txt", sep= '\t')
fig, ax = plt.subplots()
fig.set_size_inches(20,8)
ax.set_yscale('log')

#plot int boarders
plt.axvline(integral[0], c = 'r', label = 'int')
plt.axvline(integral[1], c = 'r')

#plot u0_1_2_609KEv boarders
plt.axvline(u0_1_2_609KEv[0], c = 'y', label = 'u0_1_2_609KEv')
plt.axvline(u0_1_2_609KEv[1], c = 'y')

#plot u1_2205KEv boarders
plt.axvline(u1_2205KEv[0], c = 'c', label = 'u1_2205KEv')
plt.axvline(u1_2205KEv[1], c = 'c')

#plot u2_1120KEv boarders
plt.axvline(u2_1120KEv[0], c = 'c', label = 'u2_1120KEv + 1240KEv')
plt.axvline(u2_1120KEv[1], c = 'c')

#plot u3_1760KEv boarders
plt.axvline(u3_1760KEv[0], c = 'm', label = 'u3_1760KEv')
plt.axvline(u3_1760KEv[1], c = 'm')

#plot th1_910KEv boarders
plt.axvline(th1_910KEv[0], c = 'tab:olive', label = 'th1_910KEv')
plt.axvline(th1_910KEv[1], c = 'tab:olive')

#plot th2_2620KEv boarders
plt.axvline(th2_2620KEv[0], c = 'tab:purple', label = 'th2_2620KEv')
plt.axvline(th2_2620KEv[1], c = 'tab:purple')

#plot K boarders
plt.axvline(K[0], c = 'tab:orange', label = 'K')
plt.axvline(K[1], c = 'tab:orange')

ax.legend()
ax.plot(calibration_df["channel"], calibration_df["value"])
ax.plot(calibration_df["channel"], calibration_df["average_window"])
plt.savefig(new_folder + '\\' + 'spectrum_calibration.png', dpi=1200)
plt.show()