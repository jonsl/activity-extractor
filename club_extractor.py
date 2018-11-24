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

# xlsx file is timestamped now
now = datetime.datetime.now()
filename = now.strftime('%Y-%m-%d_athlete_data.xlsx')

workbook = xlsxwriter.Workbook(filename, {'default_date_format':'dd/mm/yy'})
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

row=0
col=0

worksheet.write(row, col, 'ID', bold)
worksheet.write(row, col+1, 'Name', bold)
worksheet.write(row, col+2, 'Achievement count', bold)
worksheet.write(row, col+3, 'Date', bold)
worksheet.write(row, col+4, 'Type', bold)
worksheet.write(row, col+5, 'Distance (m)', bold)
worksheet.write(row, col+6, 'Moving Time (s)', bold)
worksheet.write(row, col+7, 'Average Speed (m/s)', bold)
worksheet.write(row, col+8, 'Max Speed (m/s)', bold)
worksheet.write(row, col+9, 'Total Elevation Gain (m)', bold)

worksheet.set_column('A:A', 10)
worksheet.set_column('B:B', 26)
worksheet.set_column('C:C', 10)
worksheet.set_column('D:D', 9)
worksheet.set_column('E:E', 8)
worksheet.set_column('F:F', 12)
worksheet.set_column('G:G', 13)
worksheet.set_column('H:H', 17)
worksheet.set_column('I:I', 14)
worksheet.set_column('J:J', 19)

row += 1

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



workbook.close()

print('\nwrote \'{0}\''.format(filename))
