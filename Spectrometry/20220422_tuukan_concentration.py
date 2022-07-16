import numpy as np
import pandas as pd
import geopandas as gpd
#import rasterio
import matplotlib.pyplot as plt
from matplotlib import ticker
import datetime
import os

current_folder = r"F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Data\Spectrum\20220210_Calibration_isotope\Calibration_points\Regression_lines"
calibration_points = gpd.read_file(r"F:\YandexDisk\Work\SibGIS\QGisPRJ\20210731_Tuykan\Data\Spectrum\20220210_Calibration_isotope\Calibration_points\Spectrum_Calibration_points_cut.gpkg", layer='Spectrum_Calibration_points_cut')

polynom_U1 = np.polyfit(calibration_points["U1"], calibration_points["u_aero"], 1)
print("U1 channel regression :{}, pearson: {}.".format(polynom_U1, calibration_points["U1"].corr(calibration_points["u_aero"])))

polynom_U2 = np.polyfit(calibration_points["U2"], calibration_points["u_aero"], 1)
print("U2 channel regression :{}, pearson: {}.".format(polynom_U2, calibration_points["U2"].corr(calibration_points["u_aero"])))

polynom_U3 = np.polyfit(calibration_points["U3"], calibration_points["u_aero"], 1)
print("U3 channel regression :{}, pearson: {}.".format(polynom_U3, calibration_points["U3"].corr(calibration_points["u_aero"])))

polynom_U4 = np.polyfit(calibration_points["U4"], calibration_points["u_aero"], 1)
print("U4 channel regression :{}, pearson: {}.".format(polynom_U4, calibration_points["U4"].corr(calibration_points["u_aero"])))

integral = np.polyfit(calibration_points["int"], calibration_points["tot_ra_con"], 1)
print("int_UAV channel regression :{}, pearson: {}.".format(integral, calibration_points["int"].corr(calibration_points["tot_ra_con"])))

K = np.polyfit(calibration_points["K"], calibration_points["K_aero"], 1)
print("K_UAV channel regression :{}, pearson: {}.".format(K, calibration_points["K"].corr(calibration_points["K_aero"])))

Th = np.polyfit(calibration_points["Th"], calibration_points["th_aero"], 1)
print("Th channel regression :{}, pearson: {}.".format(Th, calibration_points["Th"].corr(calibration_points["th_aero"])))

# th2_2620KEv = np.polyfit(calibration_points["th2_2620KEv"], calibration_points["Th_GND"], 1)
# print("u3_1760KEv channel regression :{}, pearson: {}.".format(th2_2620KEv, calibration_points["th2_2620KEv"].corr(calibration_points["Th_GND"])))
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

#U1 channel plot
x = calibration_points["U1"]
y = calibration_points["u_aero"]
x_line = np.linspace(calibration_points["U1"].min(), calibration_points["U1"].max())
y_line = x_line * polynom_U1[0] + polynom_U1[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("U1 channel regression :{}, pearson: {}.".format(polynom_U1, calibration_points["U1"].corr(calibration_points["u_aero"])))
plt.xlabel("U1")
plt.ylabel("u_aero")
ax.grid()
plt.savefig(new_folder + '\\' + 'U1.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#u1_2205KEv channel plot
x = calibration_points["U2"]
y = calibration_points["u_aero"]
x_line = np.linspace(calibration_points["U2"].min(), calibration_points["U2"].max())
y_line = x_line*polynom_U2[0] + polynom_U2[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("U2 channel regression :{}, pearson: {}.".format(polynom_U2, calibration_points["U2"].corr(calibration_points["u_aero"])))
plt.xlabel("U2")
plt.ylabel("u_aero")
ax.grid()
plt.savefig(new_folder + '\\' + 'U2.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#u2_1120KEv channel plot
x = calibration_points["U3"]
y = calibration_points["u_aero"]
x_line = np.linspace(calibration_points["U3"].min(), calibration_points["U3"].max())
y_line = x_line*polynom_U3[0] + polynom_U3[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("U3 channel regression :{}, pearson: {}.".format(polynom_U3, calibration_points["U3"].corr(calibration_points["u_aero"])))
plt.xlabel("U3")
plt.ylabel("u_aero")
ax.grid()
plt.savefig(new_folder + '\\' + 'U3.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#U4 channel plot
x = calibration_points["U4"]
y = calibration_points["u_aero"]
x_line = np.linspace(calibration_points["U4"].min(), calibration_points["U4"].max())
y_line = x_line*polynom_U4[0] + polynom_U4[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("U4 channel regression :{}, pearson: {}.".format(polynom_U4, calibration_points["U4"].corr(calibration_points["u_aero"])))
plt.xlabel("U4")
plt.ylabel("u_aero")
ax.grid()
plt.savefig(new_folder + '\\' + 'U4.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#K channel plot
x = calibration_points["K"]
y = calibration_points["K_aero"]
x_line = np.linspace(calibration_points["K"].min(), calibration_points["K"].max())
y_line = x_line*K[0] + K[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("K channel regression :{}, pearson: {}.".format(K, calibration_points["K"].corr(calibration_points["K_aero"])))
plt.xlabel("K")
plt.ylabel("K_aero")
ax.grid()
plt.savefig(new_folder + '\\' + 'K.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

#Th channel plot
x = calibration_points["Th"]
y = calibration_points["th_aero"]
x_line = np.linspace(calibration_points["Th"].min(), calibration_points["Th"].max())
y_line = x_line * Th[0] + Th[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("Th channel regression :{}, pearson: {}.".format(Th, calibration_points["Th"].corr(calibration_points["th_aero"])))
plt.xlabel("Th")
plt.ylabel("th_aero")
ax.grid()
plt.savefig(new_folder + '\\' + 'Th.png', dpi=800)
plt.figure(figsize=(10,6))
plt.show()

# #th2_2620KEv channel plot
# x = calibration_points["th2_2620KEv"]
# y = calibration_points["Th_GND"]
# x_line = np.linspace(calibration_points["th2_2620KEv"].min(), calibration_points["th2_2620KEv"].max())
# y_line = x_line*th2_2620KEv[0] + th2_2620KEv[1]
# fig, ax = plt.subplots()
# fig.set_size_inches(12,6)
# ax.scatter(x, y, s=1, color = 'r')
# ax.plot(x_line, y_line)
# ax.title.set_text("th2_2620KEv channel regression :{}, pearson: {}.".format(th2_2620KEv, calibration_points["th2_2620KEv"].corr(calibration_points["Th_GND"])))
# plt.xlabel("th2_2620KEv")
# plt.ylabel("Th_GND")
# ax.grid()
# plt.savefig(new_folder + '\\' + 'th2_2620KEv.png', dpi=800)
# plt.figure(figsize=(10,6))
# plt.show()

#int_UAV channel plot
x = calibration_points["int"]
y = calibration_points["tot_ra_con"]
x_line = np.linspace(calibration_points["int"].min(), calibration_points["int"].max())
y_line = x_line*integral[0] + integral[1]
fig, ax = plt.subplots()
fig.set_size_inches(12,6)
ax.scatter(x, y, s=1, color = 'r')
ax.plot(x_line, y_line)
ax.title.set_text("int channel regression :{}, pearson: {}.".format(integral, calibration_points["int"].corr(calibration_points["tot_ra_con"])))
plt.xlabel("int")
plt.ylabel("tot_ra_con")
ax.grid()
plt.savefig(new_folder + '\\' + 'int.png', dpi=800)
plt.show()

# k = 2.73958333
# b = 25.66666667

# u0_1_2_609KEv = (int(k * 609 + b), int(k * 650 + b)) #609 1/2 пика
# u1_2205KEv = (int(k * 2035 + b), int(k * 2280 + b)) #корректировка по графику 2.2
# u2_1120KEv = (int(k*1055+b), int(k*1300+b)) #1120/ 2пика 7 и 8
# u3_1760KEv = (int(k*1670+b), int(k*1830+b)) #1,76
# th1_910KEv = (int(k*875+b), int(k*1010+b)) #935
# th2_2620KEv = (int(k*2356+b), int(k*2480+b)) #2.4
# K = (int(k*1340+b), int(k*1535+b)) #1459 K40
# integral = (int(k*400+b), int(k*2810+b))
# u0_1_2_609KEv = (int(k * 607 + b), int(k * 664 + b))  # 609 1/2 пика
# u1_2205KEv = (int(k * 2025 + b), int(k * 2300 + b))  # корректировка по графику 2.2
# u2_1120KEv = (int(k * 1050 + b), int(k * 1305 + b))  # 1120/ 2пика 7 и 8
# u3_1760KEv = (int(k * 1670 + b), int(k * 1835 + b))  # 1,76
# Th = (int(k * 870 + b), int(k * 1010 + b))  # 910
# th2_2620KEv = (int(k * 2510 + b), int(k * 2670 + b))  # 2.4 переделать 2.62
# K = (int(k * 1340 + b), int(k * 1535 + b))  # 1459 K40
# integral = (int(k * 400 + b), int(k * 2810 + b))
#
#
# calibration_df = pd.read_csv(r"F:\YandexDisk\Work\SibGIS\QGisPRJ\20211021_Krasnokamensk_metod\Data\Spectrum\Spectrum\KrasnokamSpectr\Spectr40m\calibration_spectre.txt", sep= '\t')
# fig, ax = plt.subplots()
# fig.set_size_inches(20,8)
# ax.set_yscale('log')
#
# #plot int boarders
# plt.axvline(integral[0], c = 'r', label = 'int')
# plt.axvline(integral[1], c = 'r')
#
# #plot u0_1_2_609KEv boarders
# plt.axvline(u0_1_2_609KEv[0], c = 'y', label = 'u0_1_2_609KEv')
# plt.axvline(u0_1_2_609KEv[1], c = 'y')
#
# #plot u1_2205KEv boarders
# plt.axvline(u1_2205KEv[0], c = 'c', label = 'u1_2205KEv')
# plt.axvline(u1_2205KEv[1], c = 'c')
#
# #plot u2_1120KEv boarders
# plt.axvline(u2_1120KEv[0], c = 'c', label = 'u2_1120KEv + 1240KEv')
# plt.axvline(u2_1120KEv[1], c = 'c')
#
# #plot u3_1760KEv boarders
# plt.axvline(u3_1760KEv[0], c = 'm', label = 'u3_1760KEv')
# plt.axvline(u3_1760KEv[1], c = 'm')
#
# #plot th1_910KEv boarders
# plt.axvline(Th[0], c ='tab:olive', label ='th1_910KEv')
# plt.axvline(Th[1], c ='tab:olive')
#
# #plot th2_2620KEv boarders
# plt.axvline(th2_2620KEv[0], c = 'tab:purple', label = 'th2_2620KEv')
# plt.axvline(th2_2620KEv[1], c = 'tab:purple')
#
# #plot K boarders
# plt.axvline(K[0], c = 'tab:orange', label = 'K')
# plt.axvline(K[1], c = 'tab:orange')
#
# ax.legend()
# ax.plot(calibration_df["channel"], calibration_df["value"])
# ax.plot(calibration_df["channel"], calibration_df["average_window"])
# plt.savefig(new_folder + '\\' + 'spectrum_calibration.png', dpi=1200)
# plt.show()