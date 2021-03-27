# Get the datetime-formatted version of any sensor timestamp
# with the function below

# Added by Nick 3/26/2021

month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
}


def sensor_timestamp_to_datetime(time_stamp):
    # Take our date of form "Sat Mar 27 23:05:55 2021", and split it at the spaces...
    date_comps = time_stamp.split(' ')
    # Transform it into Python datetime format "2021-03-27 23:05:55"
    return date_comps[4] + "-" + month_map[date_comps[1]] + "-" + date_comps[2] + " " + date_comps[3]
