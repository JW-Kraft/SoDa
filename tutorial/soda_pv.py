#%%
import soda
import matplotlib.pyplot as plt
import pandas as pd

#%% Create object of SolarSite
lat = -19.1703
lon = 46.5232

site = soda.SolarSite(lat,lon)

#%% Get irradiance data
year = "2018"
leap_year = False
interval = "30"
utc = False
df = site.get_nsrdb_data(year,leap_year,interval,utc)

#%% Calculate solar power output

clearsky = False
capacity = 1
DC_AC_ratio = 1.2
tilt = 5
azimuth = 0
inv_eff = 99.5
losses = 0
array_type = 0

pwr = site.generate_solar_power_from_nsrdb(clearsky, capacity, DC_AC_ratio, tilt, azimuth, inv_eff, losses, array_type)

#%% Generate synthetic high-resolution power output

resolution = "1min"
solar_data = pd.DataFrame()
i = 0
for date in pd.date_range(start="2018-01-01", end="2018-12-31", freq='D'):
    solar_data = pd.concat([solar_data, site.generate_high_resolution_power_data(resolution, date.strftime("%Y-%m-%d"))])
    print('day '+ str(i))
    i = i + 1

#%% Plot results
plt.plot(solar_data['2018-01-01'], label="1-min average")
plt.plot(pwr['2018-01-01'], label="30-min average")
plt.xticks(rotation=45)
plt.ylabel("AC power (MW)")
plt.legend()
plt.show()

#%% Dump files
solar_data.to_csv('1min_res_pv_mahavelona.csv')
df.to_csv('nsrdb_mahavelona.csv')