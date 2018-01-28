
import xlsxwriter
import datetime
import time

from stravalib.client import Client

CLIENT_ID=22927

ACCESS_TOKEN='6678266ba9422748554be8e5aaa46ea8dec5b39a'

# auth
client = Client()
url = client.authorization_url(client_id=CLIENT_ID,
        redirect_uri='http://localhost:8000/')
print('\nurl={0}'.format(url))

client = Client(access_token=ACCESS_TOKEN)

# Now store that access token somewhere (a database?)
client.access_token = ACCESS_TOKEN;

athlete = client.get_athlete()
print("\n=> for athlete {id}, I now have an access token {token}\n".format(
	id=athlete.id, token=client.access_token))

# get club to work with
clubs=[]
for idx, club in enumerate(client.get_athlete_clubs()):
	clubs.append(club)
	print("{0}. {1} {2}".format(idx, club.id, club.name.encode()))

selected_club_idx = int(input('\nPlease enter club # > '))

now = datetime.datetime.now()
filename = now.strftime('%Y-%m-%d_club_data.xlsx');

workbook = xlsxwriter.Workbook(filename, {'default_date_format':'dd/mm/yy'})
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})

row=0
col=0

worksheet.write(row, col, 'ID', bold)
worksheet.write(row, col+1, 'Name', bold)
worksheet.write(row, col+2, 'Athlete', bold)
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

# get activities for the club
club_activities=[]
total_distance = 0
for idx, club_activity in enumerate(client.get_club_activities(clubs[selected_club_idx].id)):
	club_activities.append(club_activity)
	name_field = club_activity.athlete.lastname + ', ' + club_activity.athlete.firstname
	worksheet.write(row, col, club_activity.id)
	worksheet.write(row, col+1, club_activity.name)
	worksheet.write(row, col+2, name_field)
	worksheet.write_datetime(row, col+3, club_activity.start_date.replace(tzinfo=None))
	worksheet.write(row, col+4, club_activity.type)
	worksheet.write(row, col+5, club_activity.distance)
	worksheet.write(row, col+6, club_activity.moving_time.total_seconds())
	worksheet.write(row, col+7, club_activity.average_speed)
	worksheet.write(row, col+8, club_activity.max_speed)
	worksheet.write(row, col+9, club_activity.total_elevation_gain)
	row += 1
	col = 0
	total_distance += int(club_activity.distance)

workbook.close()

print('\nwrote \'{0}\''.format(filename))

print('\nprocessed %s activities' % idx)

print('\nTotal activities distance is {0} km / {1} mi\n'.format(
	round(total_distance / 1000.0, 2), round((total_distance * 0.621371) / 1000.0, 2)))

