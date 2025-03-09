import pandas as pd

def week_extractor(week_dates=pd.Series(dtype='datetime64[ns]')):
    
    week_range = {}
    
    for i in range(len(week_dates)):
        cur_day = week_dates.iat[i].day_name()  # Using .iat for scalar access
        
        if cur_day == "Monday":
            week_range.update({week_dates.iat[i].date(): f"{week_dates.iat[i].date()}/{(week_dates.iat[i] + pd.Timedelta('6 days')).date()}"})
        elif cur_day == "Tuesday":
            week_range.update({week_dates.iat[i].date(): f"{(week_dates.iat[i] + pd.Timedelta('-1 day')).date()}/{(week_dates.iat[i] + pd.Timedelta('5 days')).date()}"})
        elif cur_day == "Wednesday":
            week_range.update({week_dates.iat[i].date(): f"{(week_dates.iat[i] + pd.Timedelta('-2 days')).date()}/{(week_dates.iat[i] + pd.Timedelta('4 days')).date()}"})
        elif cur_day == "Thursday":
            week_range.update({week_dates.iat[i].date(): f"{(week_dates.iat[i] + pd.Timedelta('-3 days')).date()}/{(week_dates.iat[i] + pd.Timedelta('3 days')).date()}"})
        elif cur_day == "Friday":
            week_range.update({week_dates.iat[i].date(): f"{(week_dates.iat[i] + pd.Timedelta('-4 days')).date()}/{(week_dates.iat[i] + pd.Timedelta('2 days')).date()}"})
        elif cur_day == "Saturday":
            week_range.update({week_dates.iat[i].date(): f"{(week_dates.iat[i] + pd.Timedelta('-5 days')).date()}/{(week_dates.iat[i] + pd.Timedelta('1 day')).date()}"})
        elif cur_day == "Sunday":
            week_range.update({week_dates.iat[i].date(): f"{(week_dates.iat[i] + pd.Timedelta('-6 days')).date()}/{week_dates.iat[i].date()}"})
    
    return week_range

if __name__ == '__main__':
    week_extractor()
