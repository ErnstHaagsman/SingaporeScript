import pandas as pd
from pylab import show

aircraft_arrivals = pd.read_csv('aircraft-arrivals-departures.csv')
exports = pd.read_csv('domestic-exports-by-area-annual.csv')

# Set aircraft_arrival's index to a DatetimeIndex
aircraft_arrivals = aircraft_arrivals\
    .set_index(pd.DatetimeIndex(aircraft_arrivals['month']))

# Set exports' index to DatetimeIndex, and ensure numeric values are numeric
exports = exports.set_index(
    pd.DatetimeIndex(exports['year'].apply(
        lambda x: pd.to_datetime(x, format='%Y'))))

exports['domestic_exports'] = exports['domestic_exports']\
    .apply(lambda x: pd.to_numeric(x, errors='coerce'))

# Add an 'aircraft_movements' column to aircraft_arrivals
aircraft_arrivals = aircraft_arrivals\
    .assign(aircraft_movements=
            lambda x: x['aircraft_arrivals'] + x['aircraft_departures'])

annual_movements = aircraft_arrivals.resample('A').sum()

del annual_movements['aircraft_departures']
del annual_movements['aircraft_arrivals']

annual_movements[500]

annual_exports = exports.resample('A').sum()

del annual_exports['year']

singapore_data = pd.merge(annual_movements, annual_exports,
                          left_index=True, right_index=True)

singapore_data.plot()
show()
