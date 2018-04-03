
import xlsxwriter
import datetime
import time

from stravalib.client import Client

from units import unit

def read_access_tokens(tokens_file):
	tokens=[]
	try:
		with open('tokens') as fp:  
			for idx, line in enumerate(fp):
				line = line.strip()
				if line:
					tokens.append(line)
	except IOError:
		print('=> unable to open file: \'{0}\''.format(tokens_file))
	else:
		fp.close()
		print("=> read {0} access tokens".format(idx))
		return tokens

def process_access_token(worksheet, access_token) :

	global row, col

	client = Client(access_token=access_token)
	athlete = client.get_athlete()
	activities=[]
	total_distance = 0
	for activity in client.get_activities():
		#print('{0}'.format(activity))
		format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
		worksheet.write(row, col, activity.id)
		worksheet.write(row, col+1, athlete.lastname + ', ' + athlete.firstname)
		worksheet.write(row, col+2, activity.name)
		worksheet.write(row, col+3, activity.achievement_count)
		worksheet.write(row, col+4, activity.start_date.replace(tzinfo=None))
		worksheet.write(row, col+5, activity.type)
		worksheet.write(row, col+6, activity.distance)
		worksheet.write(row, col+7, activity.moving_time.total_seconds())
		worksheet.write(row, col+8, activity.average_speed)
		worksheet.write(row, col+9, activity.max_speed)
		worksheet.write(row, col+10, activity.total_elevation_gain)
		worksheet.write(row, col+11, activity.distance)
		worksheet.write(row, col+12, activity.distance)
		row += 1
		col = 0
		total_distance += int(activity.distance)

	return total_distance

# read all access tokens
tokens = []
tokens = read_access_tokens('tokens')

# xlsx file is timestamped now
now = datetime.datetime.now()
filename = now.strftime('%Y-%m-%d_athlete_data.xlsx');

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

# get activities for the club
activities=[]
total_distance = 0


for idx, token in enumerate(tokens):
	total_dist = process_access_token(worksheet, token)
	total_distance += total_dist
	print('total distance = {0}'.format(total_dist))

print('total total total distance = {0}'.format(total_distance))

workbook.close()

print('\nwrote \'{0}\''.format(filename))


