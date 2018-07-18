"""
Atlantic Small Multiples
-------------------------
Takes in the most recent COBE-SST dataset, computes anomalies relative to the
1890-1920 climatology, and plots small multiples of the Atlantic Ocean from
1900-2018.

Download link: ftp://ftp.cdc.noaa.gov/Datasets/COBE
(Approx updated on the 7th of each month)

INPUT 1: Path to dataset
"""
import sys
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
import cmocean.cm as cm
import matplotlib as mpl
import esmtools as et


def main():
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
    ds = ds.groupby('time.year').mean('time')
    clim = ds.sel(year=slice(1891, 1920)).mean('year')
    anom = (ds - clim).sel(year=slice(1900, 2018))
    cdata, clons = add_cyclic_point(anom.values, coord=anom.lon)
    canom = xr.DataArray(cdata, coords=[anom.year, anom.lat, clons],
                         dims=['year', 'lat', 'lon'])
    # Plot
    f, axes = plt.subplots(figsize=(18, 18), ncols=10, nrows=12,
                           subplot_kw=dict(
                           projection=ccrs.Orthographic(central_longitude=-25,
                                                        central_latitude=0)))
    for i, ax in enumerate(f.axes):
        if i > 117:
            ax.outline_patch.set_edgecolor('white')
            del ax
        else:
            data = canom.isel(year=i)
            ax.pcolormesh(canom.lon, canom.lat, data, vmin=-2, vmax=2,
                          transform=ccrs.PlateCarree(),
                          cmap=et.vis.discrete_cmpa(16, cm.balance))
            ax.add_feature(cfeature.LAND, facecolor='k')
    f.tight_layout()
    plt.savefig('figs/atlantic_small_multiples.png', bbox_inches='tight',
                pad_inches=1, transparent=True)


if __name__ == '__main__':
    main()
