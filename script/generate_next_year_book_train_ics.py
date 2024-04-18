import os
import requests
import datetime as dt
import logging
from icalendar import Calendar, Event
import pytz
from pytz import timezone
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constant for the number of days before an event to create a reminder
BOOKING_DAYS = 14
DEFAULT_DIR = "../public/"
# Helper function to fetch holidays data
def fetch_holiday_booking_dates(year):
    url = 'https://cdn.jsdelivr.net/gh/lanceliao/china-holiday-calender/holidayAPI.json'
    response = requests.get(url)
    data = response.json()
    
    booking_dates = set()
    
    for holiday in data['Years'].get(str(year), []):
        start_date = dt.datetime.strptime(holiday['StartDate'], '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(holiday['EndDate'], '%Y-%m-%d').date()
        booking_dates.update([start_date - dt.timedelta(days=1), end_date + dt.timedelta(days=1)])
    
    return booking_dates

# Helper function to fetch compensatory work dates
def fetch_compensatory_dates(year):
    response = requests.get('https://cdn.jsdelivr.net/gh/lanceliao/china-holiday-calender/holidayCal-CO.ics')
    calendar = Calendar.from_ical(response.text)
    comp_dates = []

    for component in calendar.walk('vevent'):
        start = component.get('dtstart').dt.date()
        if start.year == year:
            comp_dates.append(start)

    return comp_dates

# Combine and sort holiday and compensatory dates along with regular weekday dates
def compile_and_sort_dates(year):
    holidays = fetch_holiday_booking_dates(year)
    compensatory = fetch_compensatory_dates(year)
    all_dates = set(holidays) | set(compensatory)
    return sorted(all_dates)

# Calculate reminder dates based on booking rules
def calculate_reminder_dates(sorted_dates):
    return [{'reminder_date': date - dt.timedelta(days=BOOKING_DAYS), 'book_date': date} for date in sorted_dates]

# Generate an ICS file from a list of reminder and book dates
def create_ics_file(reminders, filename="bookTrain.ics"):
    cal = Calendar()
    cal.add('prodid', '-//Custom Calendar//mxm.dk//')
    cal.add('version', '2.0')
    cst_tz = timezone('Asia/Shanghai')  # 定义CST时区
    for reminder in reminders:
        # 将提醒时间从CST转换为UTC
        event_start = cst_tz.localize(dt.datetime.combine(reminder['reminder_date'], dt.time(11, 50, 0)))
        event_end = cst_tz.localize(dt.datetime.combine(reminder['reminder_date'], dt.time(16, 10, 0)))
        event_start_utc = event_start.astimezone(pytz.utc)
        event_end_utc = event_end.astimezone(pytz.utc)
        event = Event()
        event.add('summary', f'火车票提醒 - 订票日期: {reminder["book_date"].isoformat()}')
        event.add('dtstart', event_start_utc)
        event.add('dtend', event_end_utc)
        event.add('dtstamp', dt.datetime.now(pytz.utc))
        event['uid'] = f'{reminder["reminder_date"].isoformat()}-weiainijiujiu@126.com'
        cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    return filename

# Main function to run as a GitHub Actions job
def main():
    year = dt.datetime.now().year + 1 # next year
    sorted_dates = compile_and_sort_dates(year)
    reminder_dates = calculate_reminder_dates(sorted_dates)
    
    # Ensure the directory exists
    if not os.path.exists(DEFAULT_DIR):
        os.makedirs(DEFAULT_DIR)
        logging.info(f"Created directory {DEFAULT_DIR}")
    
    base_filename = "bookTrain.ics"
    full_path = os.path.join(DEFAULT_DIR, base_filename)
    old_filename = os.path.join(DEFAULT_DIR, f"bookTrain-{year - 1}.ics")
    
    if os.path.exists(full_path):
        os.rename(full_path, old_filename)
        logging.info(f"Renamed old file to {old_filename}")
    
    ics_file = create_ics_file(reminder_dates, filename=full_path)
    logging.info(f"ICS file created: {ics_file}")

if __name__ == "__main__":
    main()
