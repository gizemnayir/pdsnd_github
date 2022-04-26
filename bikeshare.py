import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list=["chicago", "new york city", "washington"]
    while True:
        city=input('Would you like to see data for Chicago, New York City or  Washington?\n').lower()
        if city in city_list:
            break
        else:
            print('Please enter a valid city name')
    # get user input for month (all, january, february, ... , june)
    month_list=("january", "february", "march", "april", "may", "june")
    while True:
        month=input('Which month? January, February, March, April, May or June?\n').lower()
        if month in month_list:
            break
        else:
            print('Please enter a valid month.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list=("monday","tuesday","wednesday","thursday","friday","saturday","sunday","all")
    while True:
        day=input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n').lower()
        if day in day_list:
            break
        else:
            print('Please enter a valid day.')
        print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df= pd.read_csv('C:/Users/gizem.nayir/.atom/{}'.format(CITY_DATA[city]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    most_popular_month=df['month'].mode()[0]
    print('The most popular month is {}'.format(most_popular_month))
    # display the most common day of week
    most_popular_day=df['day_of_week'].mode()[0]
    print('The most popular day is {}'.format(most_popular_day))
    # display the most common start hour
    most_popular_hour=df['hour'].mode()[0]
    print('The most popular hour is {}'.format(most_popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    most_common_start_station=df['Start Station'].mode()[0]
    print('The most popular start station is {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station=df['End Station'].mode()[0]
    print('The most common end station is {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['station']=df['Start Station'] + '&'+df['End Station']
    most_common_station=df['station'].mode()[0]
    print('The most frequent combination of start station and end station is {}'.format(most_common_station))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    day=total_travel_time//86400
    total_travel_time%=86400
    hour=total_travel_time//3600
    total_travel_time%=3600
    minutes=total_travel_time//60
    total_travel_time%=60
    seconds=total_travel_time

    print('Total travel time: {} days, {} hours, {} minutes, {} seconds'.format(day, hour, minutes, seconds,))
    # display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    day=avg_travel_time//86400
    avg_travel_time%=86400
    hour=avg_travel_time//3600
    avg_travel_time%=3600
    minutes=avg_travel_time//60
    avg_travel_time%=60
    seconds=avg_travel_time

    print('Average trip duraiton: {} days, {} hours, {} minutes, {} seconds'.format(day, hour, minutes, seconds,))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types=df['User Type'].value_counts()
    print('User types: {}'.format(user_types))

    # Display counts of gender
    gender=df['Gender'].value_counts()
    print('Genders: {}'.format(gender))
    # Display earliest, most recent, and most common year of birth
    earliest=df['Birth Year'].min()
    recent=df['Birth Year'].max()
    common=df['Birth Year'].mode()[0]
    print('The earliest birth year: {}\n The most recent birth year: {}\n The most common birth year: {}'.format(earliest, recent, common))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """displays raw data as long as user request to see"""
    if input("Would you like to see a few lines of raw data? Yes/No\n").lower()=='yes' :
        x=int(input("How many lines would you like to see?\n"))
        print(df.iloc[:x]) #displays x lines of raw data
        while True:
            if input("Would you like to see more lines of raw data? Yes/No\n").lower()=='yes' :
                i=int(input("How many more lines would you like to see?\n"))
                print(df.iloc[x:i+x]) #displays x+i lines of raw data if user requests
                i+=x
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
