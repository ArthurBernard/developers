#!/usr/bin/env python3
# coding: utf-8

""" Function to display some usfull statistics about using bike. """

import sys
import time
import pandas as pd
import numpy as np

from load import load_csv


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday', 'sunday']

path = '/'.join(sys.argv[0].split('/')[:-1])
PATH_DATA = path + '/Bike_raw_data.zip' if path else 'Bike_raw_data.zip'


def choose_one_of_them(_list):
    """ Choose one argument among the following list.

    Parameters
    ----------
    (list) _list : List of choices.

    Returns
    -------
    (str) _input - the chose argument.

    """
    _input = ''
    _list_title = [arg.title() for arg in _list]
    while _input not in _list:
        _input = input('Select one of them {}'.format(_list_title)).lower()

    return _input


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print('Hello! Let\'s explore some bikeshare data!')
    # Get city
    print('Which city do you want to analyze ?')
    city = choose_one_of_them(list(CITY_DATA.keys()))

    # Get month
    print('Which month do you want to analyze ?')
    month = choose_one_of_them(MONTHS)

    # Get day of week
    print('Which day do you want to analyze ?')
    day = choose_one_of_them(DAYS)

    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply
        no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('You choose to load data from {} for {} month and {} day'
          ''.format(city, month, day))
    # Get the file corresponding to the selected city
    city_file = CITY_DATA[city]
    # Load data in a data frame
    df = load_csv(PATH_DATA, city_file)
    # Rename columns with underscore instead of space
    df = df.rename(columns={c: '_'.join(c.split(' ')) for c in df.columns})
    # Convert date into a datetime object
    df.Start_Time = pd.to_datetime(df.Start_Time)
    df.End_Time = pd.to_datetime(df.End_Time)

    # Sort data to filter faster ? Not sure
    df = df.sort_values('Start_Time')

    # Filter by month
    if month != 'all':
        m_idx = df.Start_Time.dt.month_name().apply(lambda x: x.lower())
        df = df.loc[m_idx == month]

    # Filter by day
    if day != 'all':
        d_idx = df.Start_Time.dt.day_name().apply(lambda x: x.lower())
        df = df.loc[d_idx == day]

    # Set info about month, day and hour
    df.loc[:, 'month'] = df.Start_Time.dt.month_name()
    df.loc[:, 'day'] = df.Start_Time.dt.day_name()
    df.loc[:, 'hour'] = df.Start_Time.dt.hour

    return df


def _get_max_count_by(df, by):
    return df.groupby(by).count().iloc[:, 0].idxmax()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Compute and display the most common month
    max_month = _get_max_count_by(df, 'month')
    print('The most frequent month is', max_month)

    # Compute and display the most common day of week
    max_day = _get_max_count_by(df, 'day')
    print('The most frequent day is', max_day)

    # Compute and display the most common start hour
    h = _get_max_count_by(df, 'hour')
    h_1 = h + 1 if h < 24 else 1
    print("The most frequent start hour is between {} and {}".format(h, h_1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Compute and display most commonly used start station
    max_start = _get_max_count_by(df, 'Start_Station')
    print('The most commonly used start station is', max_start)

    # Compute and display most commonly used end station
    max_end = _get_max_count_by(df, 'End_Station')
    print('The most commonly used end station is', max_end)

    # Display most frequent combination of start station and end station trip
    df = df.assign(comb=df.Start_Station.map(str) + " => " + df.End_Station)
    _from, _to = _get_max_count_by(df, 'comb').split(' => ')
    print('And the most commonly combination of start and end station is from '
          '{} station to {} station'.format(_from, _to))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Compute and display total travel time
    tot_dur = df.Trip_Duration.sum()
    print('The total travel time is', _text_time(tot_dur))

    # Compute and display mean travel time
    mean_dur = df.Trip_Duration.mean()
    print('The mean travel time is', _text_time(mean_dur))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def _text_time(duration):
    """ Transform a number of seconds into year, week, day, hour and minute.

    Parameters
    ----------
    duration : int
        Number of seconds.

    Returns
    -------
    str
        Corresponding number of year, week, day, hour and minute.

    """
    duration = int(duration)
    txt = '{:02d}s'.format(duration % 60)
    if duration > 60:
        duration //= 60
        txt = '{:02d}m:'.format(duration % 60) + txt

    if duration > 60:
        duration //= 60
        txt = '{:02d}h:'.format(duration % 24) + txt

    else:
        return txt

    if duration > 24:
        duration //= 24
        txt = '{:d} day(s) '.format(duration % 7) + txt

    else:
        return txt

    if duration > 7:
        duration //= 7
        txt = '{:d} week(s) '.format(duration % 52) + txt

    if duration > 52:
        duration //= 52
        txt = '{:d} year(s) '.format(duration) + txt

    return txt


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby('User_Type').count().iloc[:, 0]
    print('There are {df.Subscriber} subscribers and {df.Customer} customers'
          ''.format(df=user_type))

    # Display counts of gender
    if 'Gender' in df:
        gender = df.groupby('Gender').count().iloc[:, 0]
        print('There is {df.Female} females and {df.Male} males'
              ''.format(df=gender))

    else:
        print('There are no data about gender.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        common_birth = df.groupby('Birth_Year').count().iloc[:, 0].idxmax()
        print('The earliest birth year is {:.0f}, the most recent is {:.0f}, '
              'and the most common is {:.0f}'
              ''.format(df.loc[:, 'Birth_Year'].min(),
                        df.loc[:, 'Birth_Year'].max(),
                        common_birth))

    else:
        print('There are no data about birth years.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    """ Choose among cities, month, day, and display statistics. """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


def test_random():
    """ Test random combination of city, month and day. """
    city = np.random.choice(list(CITY_DATA.keys()))
    month = np.random.choice(MONTHS)
    day = np.random.choice(DAYS)
    df = load_data(city, month, day)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    print('end')


if __name__ == "__main__":
    main()
    # test_random()
