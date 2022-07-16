import pandas
import scipy
import numpy as np
import fiona
import geopandas as gpd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

calibration_points = gpd.read_file("F:\\YandexDisk\\Work\\SibGIS\\QGisPRJ\\20210731_Tuykan"
                                   "\\Data\\Spectrum\\20220210_Calibration_isotope"
                                   "\\Calibration_points\\Spectrum_Calibration_points_cut.shp")

polynom_tot = np.polyfit(calibration_points["int"], calibration_points["tot_ra_con"], 1)
print("total channel regression :{}".format(polynom_tot))

polynom_U1 = np.polyfit(calibration_points["U1"], calibration_points["u_aero"], 1)
print("U1 channel regression :{}".format(polynom_U1))

polynom_U2 = np.polyfit(calibration_points["U2"], calibration_points["u_aero"], 1)
print("U2 channel regression :{}".format(polynom_U2))

polynom_U3 = np.polyfit(calibration_points["U3"], calibration_points["u_aero"], 1)
print("U3 channel regression :{}".format(polynom_U3))

polynom_U4 = np.polyfit(calibration_points["U4"], calibration_points["u_aero"], 1)
print("U4 channel regression :{}".format(polynom_U4))

polynom_Th = np.polyfit(calibration_points["Th"], calibration_points["th_aero"], 1)
print("Th channel regression :{}".format(polynom_Th))

polynom_K = np.polyfit(calibration_points["K"], calibration_points["K_aero"], 1)
print("K channel regression :{}".format(polynom_K))

# plt.figure(figsize=(32, 16))
# plt.scatter(
#     calibration_points['int'],
#     calibration_points['tot_ra_con'],
#     c='red'
# )
# plt.xlabel("int")
# plt.ylabel("tot_ra_con")
# plt.title("total channel")
# plt.scatter(calibration_points['int'] , np.polyval(polynom_tot, calibration_points['int']))
# plt.show()




# print(calibration_points.get('int').values)
# print(calibration_points[['int','tot_ra_con']].values)
print(calibration_points.columns)