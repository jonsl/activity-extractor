import datetime
import sys
import time
from datetime import timedelta

import cursor
import xlsxwriter
from stravalib import unithelper
from stravalib.client import Client
from units import unit

import util


def _read_access_tokens(tokens_file):
	tokens=[]
	try:
		with open('tokens') as fp:  
			for idx, line in enumerate(fp):
				line = line.strip()
				if line:
					tokens.append(line)
	except IOError:
		print(
			'=> Unable to open file: "{tokens_file}"'.format(
				tokens_file=tokens_file,
			)
		)
	else:
		fp.close()

	return tokens

def _process_athlete(worksheet, access_token) -> float:
	global row, col

	client = Client(access_token=access_token)
	athlete = client.get_athlete()
	print(
		'Processing athlete: "{lastname}, {firstname}" ...'.format(
			lastname=athlete.lastname,
			firstname=athlete.firstname,
		)
	)

	total_distance_kilometers = float(0)
	for idx, activity in enumerate(client.get_activities()):
		if idx % 20 == 0:
			sys.stdout.write('{}\r'.format(next(spinner)))
			sys.stdout.flush()
			time.sleep(0.1)

		workbook.add_format({'num_format': 'dd/mm/yy'})

		worksheet.write(row, col, activity.id)
		worksheet.write(row, col+1, util.athlete_fullname(athlete.firstname, athlete.lastname))
		worksheet.write(row, col+2, activity.name)
		worksheet.write(row, col+3, activity.achievement_count)
		worksheet.write(row, col+4, activity.start_date.replace(tzinfo=None))
		worksheet.write(row, col+5, activity.type.upper())
		activity_distance_kilometers = float(unithelper.kilometers(activity.distance))
		worksheet.write(row, col+6, round(activity_distance_kilometers, util.DEFAULT_DECIMAL_PLACES))
		worksheet.write(row, col+7, activity.moving_time.seconds)
		activity_average_speed_meters_per_second = float(unithelper.meters_per_second(activity.average_speed))
		worksheet.write(row, col+8, round(activity_average_speed_meters_per_second, util.DEFAULT_DECIMAL_PLACES))
		activity_max_speed_meters_per_second = float(unithelper.meters_per_second(activity.max_speed))
		worksheet.write(row, col+9, round(activity_max_speed_meters_per_second, util.DEFAULT_DECIMAL_PLACES))
		activity_total_elevation_gain_meters = float(unithelper.meters(activity.total_elevation_gain))
		worksheet.write(row, col+10, round(activity_total_elevation_gain_meters, util.DEFAULT_DECIMAL_PLACES))

		row += 1
		col = 0
		total_distance_kilometers += activity_distance_kilometers

	return total_distance_kilometers

spinner = util.spinning_cursor()

# read all access tokens
tokens = []
tokens = _read_access_tokens('tokens')
print(
	'\n=> Read {token_count} access tokens\n'.format(
		token_count=len(tokens),
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
worksheet.write(row, col+2, 'Activity', bold)
worksheet.write(row, col+3, 'Achievement Count', bold)
worksheet.write(row, col+4, 'Date', bold)
worksheet.write(row, col+5, 'Type', bold)
worksheet.write(row, col+6, 'Distance (km)', bold)
worksheet.write(row, col+7, 'Moving Time (s)', bold)
worksheet.write(row, col+8, 'Average Speed (m/s)', bold)
worksheet.write(row, col+9, 'Max Speed (m/s)', bold)
worksheet.write(row, col+10, 'Total Elevation Gain (m)', bold)

worksheet.set_column('A:A', 12)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 20)
worksheet.set_column('D:D', 20)
worksheet.set_column('E:E', 10)
worksheet.set_column('F:F', 14)
worksheet.set_column('G:G', 16)
worksheet.set_column('H:H', 18)
worksheet.set_column('I:I', 24)
worksheet.set_column('J:J', 20)
worksheet.set_column('K:K', 24)

row += 1

cursor.hide()

# get activities for all athletes
total_distance_kilometers = float(0)
for idx, token in enumerate(tokens):
	athlete_total_distance_kilometers = _process_athlete(worksheet, token)
	print(
		'=> Athlete total distance is {athlete_total_distance_kilometers} km'.format(
			athlete_total_distance_kilometers=round(athlete_total_distance_kilometers, util.DEFAULT_DECIMAL_PLACES),
		)
	)
	total_distance_kilometers += athlete_total_distance_kilometers

print(
	'\n=> Total distance is {total_distance_kilometers} km'.format(
		total_distance_kilometers=round(total_distance_kilometers, util.DEFAULT_DECIMAL_PLACES),
	)
)

cursor.show()

workbook.close()
print(
	'\n=> Wrote "{filename}"\n'.format(
		filename=filename,
	)
)
