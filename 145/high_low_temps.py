from collections import namedtuple
from datetime import date

import pandas as pd

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
   
   # Find all the max temperatures across all stations for every day
   max_temps = df[df['Element'] == 'TMAX'].groupby('Date')['Data_Value'].max()
   # Drop any leap-days - should end up with 365 * 11 = 4015 total rows
   max_temps.drop(inplace=True, index=max_temps[(max_temps.index.day == 29) & (max_temps.index.month == 2)].index)

   # Find all the min temperatures across all stations for every day
   min_temps = df[df['Element'] == 'TMIN'].groupby('Date')['Data_Value'].min()
   # Drop any leap-days - should end up with 365 * 11 = 4015 total rows
   min_temps.drop(inplace=True, index=min_temps[(min_temps.index.day == 29) & (min_temps.index.month == 2)].index)

   before_2015_max_temps = max_temps[max_temps.index.year < 2015]
   before_2015_min_temps = min_temps[min_temps.index.year < 2015]
   in_2015_max_temps = max_temps[max_temps.index.year == 2015]
   in_2015_min_temps = min_temps[min_temps.index.year == 2015]

