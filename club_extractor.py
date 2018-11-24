import datetime
import sys
import time

import cursor
import xlsxwriter
from stravalib.client import Client
from units import unit


def spinning_cursor():
    while True:  # around forever
        for cursor in '|/-\\':
            yield cursor

spinner = spinning_cursor()

# read all access tokens
ACCESS_TOKEN = '6678266ba9422748554be8e5aaa46ea8dec5b39a'

client = Client(access_token=ACCESS_TOKEN)
athlete = client.get_athlete()
print(
    '\nProcessing Clubs for athlete: "{lastname}, {firstname}"\n'.format(
        lastname=athlete.lastname,
        firstname=athlete.firstname,
    )
)

# get club to process
club_list = []
for idx, club in enumerate(client.get_athlete_clubs()):
    print(
        '{idx}. {name} : {sport_type}, {member_count} Member(s)'.format(
            idx=idx+1,
            name=club.name,
            sport_type=club.sport_type.upper(),
            member_count=club.member_count,
        )
    )
    club_list.append(club)

cursor.show()

club_index = int(input("\nPlease choose a club: ")) - 1

selected_club = club_list[club_index]

# xlsx file is timestamped now
now = datetime.datetime.now()
filename = now.strftime(
    '%Y-%m-%d_{club_name}.xlsx'.format(
        club_name=selected_club.name.replace(' ', '_'),
    )
)

workbook = xlsxwriter.Workbook(filename, {'default_date_format':'dd/mm/yy'})
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

row = col = 0

worksheet.write(row, col, 'Name', bold)
worksheet.write(row, col+1, 'Activity Name', bold)
worksheet.write(row, col+2, 'Distance', bold)
worksheet.write(row, col+3, 'Moving Time', bold)
worksheet.write(row, col+4, 'Elapsed Time', bold)
worksheet.write(row, col+5, 'Total Elevation Gain', bold)
worksheet.write(row, col+6, 'Activity Type', bold)
worksheet.write(row, col+7, 'Workout Type', bold)

worksheet.set_column('A:A', 14)
worksheet.set_column('B:B', 30)
worksheet.set_column('C:C', 10)
worksheet.set_column('D:D', 14)
worksheet.set_column('E:E', 14)
worksheet.set_column('F:F', 22)
worksheet.set_column('G:G', 14)
worksheet.set_column('H:H', 14)

row += 1

total_distance = 0

for idx, activity in enumerate(client.get_club_activities(selected_club.id)):
    worksheet.write(row, col, activity.athlete.lastname + ', ' + activity.athlete.firstname)
    worksheet.write(row, col+1, activity.name)
    worksheet.write(row, col+2, activity.distance)
    worksheet.write(row, col+3, activity.moving_time)
    worksheet.write(row, col+4, activity.elapsed_time)
    worksheet.write(row, col+5, activity.total_elevation_gain)
    worksheet.write(row, col+6, activity.type)
    worksheet.write(row, col+7, activity.workout_type)
    row += 1
    col = 0
    total_distance += int(activity.distance)

print('total_distance is {total_distance}'.format(total_distance=total_distance))  # noqa

workbook.close()

print('\nwrote \'{0}\''.format(filename))
