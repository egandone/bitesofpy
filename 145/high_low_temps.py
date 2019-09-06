from collections import namedtuple
from datetime import date

import pandas as pd

pd.set_option('mode.chained_assignment', None)

DATA_FILE = "http://projects.bobbelderbos.com/pcc/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")

def high_low_record_breakers_for_2015():
   """Extract the high and low record breaking temperatures for 2015

   The expected value will be a tuple with the highest and lowest record
   breaking temperatures for 2015 as compared to the temperature data
   provided.

   NOTE:
   The date values should not have any timestamps, should be a datetime.date() object.
   The temperatures in the dataset are in tenths of degrees Celsius, so you must divide them by 10

   Possible way to tackle this challenge:

   1. Create a DataFrame from the DATA_FILE dataset.
   2. Manipulate the data to extract the following:
      * Extract highest temperatures for each day between 2005-2015
      * Extract lowest temperatures for each day between 2005-2015
      * Remove February 29th from the dataset to work with only 365 days
   3. Separate data into two separate DataFrames:
      * high/low temperatures between 2005-2014
      * high/low temperatures for 2015
   4. Iterate over the 2005-2014 data and compare to the 2015 data:
      * For any temperature that is higher/lower in 2015 extract ID, Date, Value
   5. From the record breakers in 2015, extract the high/low of all the temperatures
      * Return those as STATION namedtuples, (high_2015, low_2015)
   """
   df = pd.read_csv(DATA_FILE)
   df['Date'] = pd.to_datetime(df['Date']).apply(lambda x: x.date())
   df['yyyy'] = df['Date'].apply(lambda x: x.year)
   df['mmdd'] = df['Date'].apply(lambda x: f'{x:%m-%d}')
   max_temps = df[df['Element'] == 'TMAX']
   min_temps = df[df['Element'] == 'TMIN']

   overall_maxs = max_temps.groupby('mmdd')['Data_Value'].max()
   max_temps['overall_max'] = max_temps['mmdd'].apply(lambda x: overall_maxs[x])

   overall_mins = min_temps.groupby('mmdd')['Data_Value'].min()
   min_temps['overall_min'] = min_temps['mmdd'].apply(lambda x: overall_mins[x])

   max_records = max_temps[(max_temps['yyyy'] == 2015) & (max_temps['Data_Value'] == max_temps['overall_max'])]
   max_record = max_records.loc[max_records['Data_Value'].idxmax()]
   max_station = STATION(ID=max_record['ID'], Date=max_record['Date'], Value=max_record['Data_Value']/10.)

   min_records = min_temps[(min_temps['yyyy'] == 2015) & (min_temps['Data_Value'] == min_temps['overall_min'])]
   min_record = min_records.loc[min_records['Data_Value'].idxmin()]
   min_station = STATION(ID=min_record['ID'], Date=min_record['Date'], Value=min_record['Data_Value']/10.)

   return (max_station, min_station)

if __name__ == '__main__':
    print(high_low_record_breakers_for_2015())
