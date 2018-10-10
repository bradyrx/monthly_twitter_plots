import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import esmtools as et

def main():
    snow = pd.read_csv('data/boulder.first.snow.csv', header=None,
                       names=['year', 'month', 'day'])
    data = np.empty((len(snow),))
    for index, row in snow.iterrows():
        if row['month'] == 'September':
            offset = 0
        elif row['month'] == 'October':
            offset = 30
        elif row['month'] == 'November':
            offset = 61
        data[index] = offset + row['day']
    year = snow['year'].values
    # mpl aesthetics
    mpl.rcParams['font.size'] = 15
    # Figure
    f, ax = plt.subplots(figsize=(12,4))
    # colored blocks for each month
    ax.fill_between(year, 0, 30, color='#edf8fb')
    ax.fill_between(year, 30, 61, color='#b3cde3')
    ax.fill_between(year, 61, 91, color='#8c96c6')
    # time series
    plt.plot(year, data, color='k', linewidth=2.5, alpha=0.75)
    plt.scatter(year, data, color='k', s=49, zorder=4)
    # mean, min, max
    plt.plot([1948,2018], [np.nanmean(data), np.nanmean(data)], '--', 
             color='#696969', linewidth=2, alpha=0.6, zorder=1) 
    plt.plot([1948,2018], [np.nanmax(data), np.nanmax(data)], '--', color='#696969',
             linewidth=2, alpha=0.4)
    plt.plot([1948,2018], [np.nanmin(data), np.nanmin(data)], '--', color='#696969',
             linewidth=2, alpha=0.4)
    # highlight record dates
    plt.scatter(year[26], data[26], color='#0571b0', zorder=4, s=64, 
                edgecolor='#0571b0')
    plt.scatter(year[66], data[66], color='#0571b0', zorder=4, s=64, 
                edgecolor='#0571b0')
    plt.scatter(year[68], data[68], color='#ca0020', zorder=4, s=64, 
                edgecolor='#ca0020')
    # aesthetics
    ax.set_xlim([1946,2020])
    plt.xticks(np.arange(1948,2019,10), rotation=45)
    ax.set_ylim([1, 91])
    yticks = [1,15,30,45,61,76,91]
    ylabels = ['Sep 1', 'Sep 15', 'Sep 30', 'Oct 15', 'Oct 31',
               'Nov 15', 'Nov 30']
    plt.yticks(yticks, ylabels, rotation='horizontal')
    sns.despine(trim=True)
    ax.set_title('First Recorded Snow in Boulder, CO', fontsize=20)
    ax.set_ylabel('Date of First Snow', fontsize=16)
    ax.set_xlabel('Year', fontsize=16)
    et.vis.savefig('../figs/boulder_first_snow', extension='.png')

if __name__ == '__main__':
    main()
