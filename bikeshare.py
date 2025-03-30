import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def print_records(df, city_input):
    """
    Asks user if they're interested in viewing the dataset
    records 5 at a time.  This function gets used inside the get_filters
    function.
    
    Input:
        DF:  the dataframe to be viewed
        city_input:  The city name selected by the user to be viewed

    Returns:
        Prints five records at a time
    """
    record = 1
    city_to_use = list(city_input)[0].title()
    view = str(input("\nWould you like to view the first 5 data records in the {} dataset? Type 'yes' or 'no': ".format(city_to_use)).lower())[0]
    while view == 'y' and record < df.shape[0]:
        for idx in np.arange(1,6):
#             print('-'*55,"\nRECORD {}\n".format(record))
            try:                
                record_val = df.iloc[record,:-1]
                print('-'*55,"\nRECORD {}\n".format(record))
                print(record_val,'\n')
                record += 1
            except:
                continue
        if record >= df.shape[0]:
            print("","-"*55,"\n","END OF RECORDS IN DATASET\n","-"*55,"\n")
        else:
            view = str(input("""\nWould you like to view the next 5 data records? Type 'yes' or 'no': """).lower())[0]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = {'chicago','new york city', 'washington'}
    city_map = {
        'chicago':'chicago', 'new york city':'new_york_city', 'washington':'washington'
    }
    while True:
        city_input = {str(input("""Please enter one of the following cities to review:  Chicago, New York City, Washington:  """).lower())}
        if city_input & cities:
            city = city_map[list(city_input)[0]]
            df = pd.read_csv("{}.csv".format(city), index_col=0)
            df['dt'] = pd.to_datetime(df['Start Time'])
            print_records(df, city_input)
            break
        else:
            print("The city entered is not valid")  
            print("You entered: ", list(city_input)[0])
            
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month_rosetta = {
        1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
        7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
    }
    available_month_num = [month for month in df['dt'].dt.month.unique()]
    available_month_num.sort()
    available_months = [month_rosetta[num] for num in available_month_num]
    available_months.append('all')

    month_map = {
        'jan': 1,'feb': 2,'mar': 3,'apr': 4,'may': 5,'jun': 6,
        'jul': 7,'aug': 8,'sep': 9,'oct': 10,'nov': 11,'dec': 12, 'all': 99
    }
    while True:
        month_input = {str(input("\n\nPlease enter a three-letter month of the year to review. You may also type 'all' to review all available months.  (NOTE:  Only the following months are available {}): ".format(available_months)).lower())[0:3]}

        if month_input & set(available_months):
            month = month_map[list(month_input)[0]]
            break
        else:
            print("The month entered is not valid")  
            print("You entered: ", list(month_input)[0])
            
            


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = {'sun','mon','tue','wed','thu','fri','sat','all'}
    week_rosetta = {
        0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'
    }
    weekday_map = {
        'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6, 'all': 99
    }
    available_day_num = [day for day in df['dt'].dt.weekday.unique()]
    available_day_num.sort()
    available_day = [week_rosetta[day] for day in available_day_num]
    available_day.append('all')
    while True:
        day_input = {str(input("\n\nPlease enter a three-letter day of the week to review. You may also type 'all' to review all available days.  (NOTE:  Only the following days are available {}): ".format(available_day)).lower())[0:3]}
        if day_input & set(available_day):
            day = weekday_map[list(day_input)[0]]
            break
        else:
            print("The day entered is not valid")  
            print("You entered: ", list(day_input)[0])

    print('-'*40)
    return city, month, day
    print('HERE WE ARE',city, month, day)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city_map = {
        'chicago':'chicago', 'new york city':'new_york_city', 'washington':'washington'
    }    
    df = pd.read_csv("{}.csv".format(city))
    df['dt'] = pd.to_datetime(df['Start Time'])
    df['start_end'] = df['Start Station'] + " to " + df['End Station']
    if day != 99:
        df = df[df['dt'].dt.dayofweek == day]
    if month != 99:
        df = df[df['dt'].dt.month == month]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    week_rosetta = {
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 
        5: 'Saturday', 6: 'Sunday'
    }
    month_rosetta = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    # TO DO: display the most common month
    print("Most common month: ",month_rosetta[df['dt'].dt.month.mode()[0]])


    # TO DO: display the most common day of week
    print("Most common day of week: ",week_rosetta[df['dt'].dt.dayofweek.mode()[0]])

    # TO DO: display the most common start hour
    print("Most common start hour: ",df['dt'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most commonly used start station is",
          df['Start Station'].value_counts(ascending = False).reset_index().iloc[0,0],
         "with",
          df['Start Station'].value_counts(ascending = False).reset_index().iloc[0,1],"entries."
         )


    # TO DO: display most commonly used end station
    print("Most commonly used end station is",
          df['End Station'].value_counts(ascending = False).reset_index().iloc[0,0],
         "with",
          df['End Station'].value_counts(ascending = False).reset_index().iloc[0,1],"entries."
         )

    # TO DO: display most frequent combination of start station and end station trip
    print("Most commonly used station combination is",
          df['start_end'].value_counts(ascending = False).reset_index().iloc[0,0],
         "with",
          df['start_end'].value_counts(ascending = False).reset_index().iloc[0,1],"entries."
         )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = np.round(df['Trip Duration'].sum()/60/60,2)
    avg_time = np.round(df['Trip Duration'].mean()/60,2)
    print("In total, riders spent {} hours in bikeshare trips.".format(total_time))


    # TO DO: display mean travel time
    print("The average rider trip was {} minutes long.".format(avg_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    unique_user_types = len(df['User Type'].unique())

    # TO DO: Display counts of user types
    user_types = pd.DataFrame(df['User Type'].value_counts(ascending = False)).reset_index()
    for item in np.arange(0,len(df['User Type'].dropna().unique())):
        print("{}: {} records".format(user_types.iloc[item,0],user_types.iloc[item,1]))


    # TO DO: Display counts of gender
    try:
        gender_types = pd.DataFrame(df['Gender'].value_counts(ascending = False)).reset_index()
        genders = len(df['Gender'].dropna().unique())
        for item in np.arange(0,genders):
            print("{}: {} records".format(gender_types.iloc[item,0],gender_types.iloc[item,1]))
    except:
        pass

    
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("Earliest year of birth:",df['Birth Year'].dropna().astype(int).min())
        print("Most recent year of birth:",df['Birth Year'].dropna().astype(int).max())
        print("Most common year of birth:",df['Birth Year'].replace(0, np.nan).dropna().astype(int).mode()[0])
        print
    except:
        pass
        




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
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


if __name__ == "__main__":
	main()
