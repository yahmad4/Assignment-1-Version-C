#!/usr/bin/env python3

'''
OPS445 Assignment 1
Program: assignment1.py 
The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Author: Yasir Ahmad (Yahmad4)
Semester: Fall 2024
Description: A Python program to calculate an end date given a start date
and a number of days, while validating inputs and considering leap years.
'''

import sys

def day_of_week(date: str) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    day, month, year = (int(x) for x in date.split('/'))
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] 
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + day) % 7
    return days[num]

def leap_year(year: int) -> bool:
    "return true if the year is a leap year"
    """
    Determines if a year is a leap year.
    :param year: Year as an integer.
    :return: True if leap year, False otherwise.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def mon_max(month:int, year:int) -> int:
    "returns the maximum day for a given month. Includes leap year check"
   
    """
    Returns the maximum number of days in a given month and year.
    :param month: Month as an integer (1-12).
    :param year: Year as an integer.
    :return: Maximum number of days in the month.
    """
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if leap_year(year) else 28
    else:
        raise ValueError("Invalid month value. Month should be between 1 and 12.")

def after(date: str) -> str: 
    '''
    after() -> date for next day in DD/MM/YYYY string format

    Return the date for the next day of the given date in DD/MM/YYYY format.
    This function has been tested to work for year after 1582
    '''
    day, mon, year = (int(x) for x in date.split('/'))
    day += 1  # next day

    lyear = year % 4
    if lyear == 0:
        leap_flag = True
    else:
        leap_flag = False  # this is not a leap year

    lyear = year % 100
    if lyear == 0:
        leap_flag = False  # this is not a leap year

    lyear = year % 400
    if lyear == 0:
        leap_flag = True  # this is a leap year
    
    mon_dict= {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
           7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if mon == 2 and leap_flag:
        mon_max = 29
    else:
        mon_max = mon_dict[mon]
    
    if day > mon_max:
        mon += 1
        if mon > 12:
            year += 1
            mon = 1
        day = 1  # if tmp_day > this month's max, reset to 1 
    return f"{day:02}/{mon:02}/{year}"

def before(date: str) -> str:
    "Returns previous day's date as DD/MM/YYYY"
    
    """
    Returns the previous day's date as DD/MM/YYYY.
    :param date: A string in DD/MM/YYYY format.
    :return: A string representing the previous day's date in the same format.
    """
    day, month, year = map(int, date.split('/'))

    # Decrement the day
    day -= 1

    # Handle month transitions
    if day == 0:
        month -= 1  # Move to the previous month
        if month == 0:  # Handle year transition
            month = 12
            year -= 1
        day = mon_max(month, year)  # Get the last day of the previous month

    # Return the previous day as DD/MM/YYYY
    return f"{day:02}/{month:02}/{year}"


def usage():
    "Print a usage message to the user"
    print("Usage: " + str(sys.argv[0]) + " DD/MM/YYYY NN")
    sys.exit()

def valid_date(date: str) -> bool:
    "check validity of date"
    
    """
    Checks if a given date string is valid.
    :param date: A string in DD/MM/YYYY format.
    :return: True if the date is valid, False otherwise.
    """
    try:
        day, month, year = map(int, date.split('/'))

        if month < 1 or month > 12:
            return False

        if day < 1 or day > mon_max(month, year):
            return False

        if year < 0:
            return False

        return True
    except (ValueError, AttributeError):
  
        return False


def day_iter(start_date: str, num: int) -> str:
    "iterates from start date by num to return end date in DD/MM/YYYY"
    
    """
    Iterates from the start date by a number of days (positive or negative).
    :param start_date: A string in DD/MM/YYYY format.
    :param num: An integer, positive for forward iteration and negative for backward iteration.
    :return: The resulting date as a string in DD/MM/YYYY format.
    """
    current_date = start_date

    for _ in range(abs(num)):
        if num > 0:
            current_date = after(current_date)  # Move forward
        else:
            current_date = before(current_date)  # Move backward

    return current_date

if __name__ == "__main__":
    import sys

    # check length of arguments
    if len(sys.argv) != 3:
        usage()

    # check first arg is a valid date
    start_date = sys.argv[1]
    if not valid_date(start_date):
        usage()

    # check that second arg is a valid number (+/-)
    try:
        num_days = int(sys.argv[2])
    except ValueError:
        usage()

    # call day_iter function to get end date, save to x
    end_date = day_iter(start_date, num_days)

    # print(f'The end date is {day_of_week(x)}, {x}.')
    day_name = day_of_week(end_date)
    print(f"The end date is {day_name}, {end_date}.")
