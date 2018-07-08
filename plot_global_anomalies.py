"""
Plot Global SST Anomalies
-------------------------
Takes in the most recent COBE-SST dataset, computes anomalies relative to the
1890-1920 climatology, and plots them on a global projection.

Download link: ftp://ftp.cdc.noaa.gov/Datasets/COBE
(Approx updated on the 7th of each month)

INPUT 1: Path to dataset
"""
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import cmocean.cm as cm
import matplotlib as mpl
import esmtools as et


def main():
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November',
                   'December']
    # Set plot parameters
    mpl.rcParams['font.size'] = 20
    mpl.rcParams['font.family'] = ['sans-serif']
    mpl.rcParams['font.sans-serif'] = ['Avant Garde']
    mpl.rcParams['figure.facecolor'] = 'k'
    mpl.rcParams['axes.edgecolor'] = 'w'
    mpl.rcParams['axes.labelcolor'] = 'w'
    mpl.rcParams['text.color'] = 'w'
    mpl.rcParams['xtick.major.size'] = 0
    mpl.rcParams['xtick.minor.size'] = 0
    mpl.rcParams['xtick.color'] = 'w'
    mpl.rcParams['ytick.major.size'] = 0
    mpl.rcParams['ytick.minor.size'] = 0
    mpl.rcParams['savefig.facecolor'] = 'k'
    mpl.rcParams['text.usetex'] = False
    # Import data 
    filepath = sys.argv[1]
    ds = xr.open_dataset(filepath)
    ds = ds['sst']
    latest_month = len(ds.time) - (2018 - 1891) * 12
    ds['time'] = pd.date_range('1891-01', '2018-0' + str(latest_month + 1),
			       freq='M')
    # Create anomalies
    clim = ds.sel(time=slice('1891-01', '1920-12')).groupby('time.month') \
        .mean('time')
    anom = ds.groupby('time.month') - clim
    data = anom.sel(time='2018-0' + str(latest_month)).squeeze()
    cyclic_data, cyclic_lons = add_cyclic_point(data.values, 
					        coord=data.lon.values)
    # Plot
    f, ax = et.vis.make_cartopy(grid_lines=False, frameon=True)
    p = ax.contourf(cyclic_lons, ds.lat, cyclic_data, np.arange(-5, 5.5, 0.5), 
                    transform=ccrs.PlateCarree(), cmap=cm.balance)

    plt.colorbar(p, orientation='horizontal',pad=0.05,fraction=0.05,
                 label='Degrees Celsius')
    # Text Annotation
    plt.text(0.5, 1.10, month_names[latest_month - 1] + 
             ' 2018 Sea Surface Temperature Anomalies',
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes, fontsize=24)
    plt.text(0.5, 1.03, '(Deviation from 1890-1920 Mean)',
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax.transAxes, fontsize=16)
    bottom_left = ('@rileyxbrady' + '\n' + 'Data: JRA COBE-SST' + '\n' +
                   'Code: https://git.io/fNfYQ')
    plt.text(0, -0.2, bottom_left,
             horizontalalignment='left',
             verticalalignment='center',
             transform = ax.transAxes, fontsize=12)
    file_out = month_names[latest_month - 1] + '.2018.COBE-SST.anomalies'
    et.vis.savefig('figs/' + file_out, dpi=300, transparent=False)


if __name__ == '__main__':
    main()
