
import xlsxwriter

from stravalib.client import Client

CLIENT_ID=22927

ACCESS_TOKEN='6678266ba9422748554be8e5aaa46ea8dec5b39a'

# auth
client = Client()
url = client.authorization_url(client_id=CLIENT_ID,
        redirect_uri='http://localhost:8000/')
print('url={0}\n'.format(url))

client = Client(access_token=ACCESS_TOKEN)

# Now store that access token somewhere (a database?)
client.access_token = ACCESS_TOKEN;

athlete = client.get_athlete()
print("For {id}, I now have an access token {token}".format(id=athlete.id, token=client.access_token))

# get club to work with
clubs=[]
for idx, club in enumerate(client.get_athlete_clubs()):
	clubs.append(club)
	print("{0}. {1} {2}".format(idx, club.id, club.name.encode()))

selected_club_idx = int(input('\nPlease enter club # > '))
#print('selected club_id is {0}\n'.format(clubs[selected_club_idx].id))

workbook = xlsxwriter.Workbook('club_data.xlsx', {'default_date_format':'dd/mm/yy'})
worksheet = workbook.add_worksheet()

row=1
col=1

worksheet.write(row, col, 'ID')
worksheet.write(row, col+1, 'Name')
worksheet.write(row, col+2, 'Athlete Name')
worksheet.write(row, col+3, 'Date')
worksheet.write(row, col+4, 'Type')
worksheet.write(row, col+5, 'Distance m')
worksheet.write(row, col+6, 'Moving Time')
worksheet.write(row, col+7, 'Average Speed m/s')
worksheet.write(row, col+8, 'Max Speed m/s')
worksheet.write(row, col+9, 'Total Elevation Gain m')

worksheet.set_column('B:B', 10)
worksheet.set_column('C:C', 40)
worksheet.set_column('D:D', 15)

row += 1

# get activities for the club
#print('{0} Activities'.format(clubs[selected_club_idx].name.encode()))
club_activities=[]
total_distance = 0
for idx, club_activity in enumerate(client.get_club_activities(clubs[selected_club_idx].id)):
	club_activities.append(club_activity)
	name_field = club_activity.athlete.lastname + ', ' + club_activity.athlete.firstname
#	print('{0}. {1}:{2} \'{3}\' start_date={4} type={5} distance={6} moving_time={7} average_speed={8} max_speed={9} total_elevation_gain={10}'.format(
#		idx, club_activity.id, club_activity.name, name_field, club_activity.start_date, club_activity.type,
#		club_activity.distance, club_activity.moving_time, club_activity.average_speed, club_activity.max_speed,
#		club_activity.total_elevation_gain))
	worksheet.write(row, col, club_activity.id)
	worksheet.write(row, col+1, club_activity.name)
	worksheet.write(row, col+2, name_field)
	worksheet.write_datetime(row, col+3, club_activity.start_date.replace(tzinfo=None))
	worksheet.write(row, col+4, club_activity.type)
	worksheet.write(row, col+5, club_activity.distance)
	worksheet.write(row, col+6, club_activity.moving_time)
	worksheet.write(row, col+7, club_activity.average_speed)
	worksheet.write(row, col+8, club_activity.max_speed)
	worksheet.write(row, col+9, club_activity.total_elevation_gain)
	row += 1
	col = 1
	total_distance += int(club_activity.distance)
#	if float(club_activity.distance) == 0.0:
#		print('distance is 0')
#	print('.', end='', flush=True)

workbook.close()

print('\nwritten club_data.xlsx')

print('\nprocessed %s activities' % idx)

print('\nTotal activities distance is {0} km / {1} mi\n'.format(round(total_distance / 1000.0, 2), round((total_distance * 0.621371) / 1000.0, 2)))

