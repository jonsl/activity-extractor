import datetime
import sys
import time
from datetime import timedelta

import cursor
from stravalib import unithelper
from stravalib.attributes import (DETAILED, META, SUMMARY, Attribute,
                                  ChoicesAttribute, DateAttribute,
                                  EntityAttribute, EntityCollection,
                                  LocationAttribute, TimeIntervalAttribute,
                                  TimestampAttribute, TimezoneAttribute)
from stravalib.client import Client
from units import unit
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

import util


def _read_access_tokens(tokens_file: str) -> list:
    tokens = []
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


def create_activity_workbook(filename: str):
    print(
        '\nPreparing {filename} ... '.format(
            filename=filename,
        )
    )

    spinner = util.spinning_cursor()

    # read all access tokens
    tokens = []
    tokens = _read_access_tokens('tokens')
    print(
        '\n=> Read {token_count} access tokens\n'.format(
            token_count=len(tokens),
        )
    )

    row = 0
    col = 0

    workbook = Workbook(filename, {'default_date_format':'dd/mm/yy'})
    bold = workbook.add_format({'bold': True})
    workbook.add_format({'num_format': 'dd/mm/yy'})

    worksheet = workbook.add_worksheet()

    worksheet.write(row, col, 'ID', bold)
    worksheet.write(row, col+1, 'Athlete', bold)
    worksheet.write(row, col+2, 'Activity Name', bold)
    worksheet.write(row, col+3, 'Achievement Count', bold)
    worksheet.write(row, col+4, 'Date', bold)
    worksheet.write(row, col+5, 'Type', bold)
    worksheet.write(row, col+6, 'Distance (m)', bold)
    worksheet.write(row, col+7, 'Distance (miles)', bold)
    worksheet.write(row, col+8, 'Moving Time (s)', bold)
    worksheet.write(row, col+9, 'Average Speed (m/s)', bold)
    worksheet.write(row, col+10, 'Max Speed (m/s)', bold)
    worksheet.write(row, col+11, 'Total Elevation Gain (m)', bold)
    worksheet.write(row, col+12, 'Suffer Score', bold)
    worksheet.write(row, col+13, 'Average Watts', bold)
    worksheet.write(row, col+14, 'Max Watts', bold)
    worksheet.write(row, col+15, 'Average Cadence', bold)
    worksheet.write(row, col+16, 'Kudos', bold)
    worksheet.write(row, col+17, 'Location City', bold)
    worksheet.write(row, col+18, 'Calories', bold)
    worksheet.write(row, col+19, 'PR Count', bold)

    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 14)
    worksheet.set_column('G:G', 16)
    worksheet.set_column('H:H', 16)
    worksheet.set_column('I:I', 18)
    worksheet.set_column('J:J', 24)
    worksheet.set_column('K:K', 20)
    worksheet.set_column('L:L', 24)
    worksheet.set_column('M:M', 18)
    worksheet.set_column('N:N', 18)
    worksheet.set_column("O:O", 18)
    worksheet.set_column('P:P', 18)
    worksheet.set_column('Q:Q', 18)
    worksheet.set_column('R:R', 18)
    worksheet.set_column('S:S', 18)
    worksheet.set_column('T:T', 18)

    row += 1

    cursor.hide()

    # get activities for all athletes
    total_distance_miles = float(0)
    for idx, access_token in enumerate(tokens):

        client = Client(access_token=access_token)
        athlete = client.get_athlete()
        print(
            'Processing athlete: "{lastname}, {firstname}" ...'.format(
                lastname=athlete.lastname,
                firstname=athlete.firstname,
            )
        )

        athlete_total_distance_miles = float(0)
        athlete_total_distance_meters = float(0)

        for idx, activity in enumerate(client.get_activities()):
            if idx % 20 == 0:
                sys.stdout.write('{}\r'.format(next(spinner)))
                sys.stdout.flush()
                time.sleep(0.1)

            worksheet.write(row, col, activity.id)
            worksheet.write(row, col+1, util.athlete_fullname(athlete.firstname, athlete.lastname))
            worksheet.write(row, col+2, activity.name)
            worksheet.write(row, col+3, activity.achievement_count)
            worksheet.write(row, col+4, activity.start_date.replace(tzinfo=None))
            worksheet.write(row, col+5, activity.type)
            distance_meters = float(unithelper.meters(activity.distance))
            worksheet.write(row, col+6, round(distance_meters, util.DEFAULT_DECIMAL_PLACES))
            distance_miles = float(unithelper.miles(activity.distance))
            worksheet.write(row, col+7, round(distance_miles, util.DEFAULT_DECIMAL_PLACES))
            worksheet.write(row, col+8, activity.moving_time.seconds)
            average_speed_meters_per_second = float(unithelper.meters_per_second(activity.average_speed))
            worksheet.write(row, col+9, round(average_speed_meters_per_second, util.DEFAULT_DECIMAL_PLACES))
            max_speed_meters_per_second = float(unithelper.meters_per_second(activity.max_speed))
            worksheet.write(row, col+10, round(max_speed_meters_per_second, util.DEFAULT_DECIMAL_PLACES))
            total_elevation_gain_meters = float(unithelper.meters(activity.total_elevation_gain))
            worksheet.write(row, col+11, round(total_elevation_gain_meters, util.DEFAULT_DECIMAL_PLACES))
            worksheet.write(row, col+12, activity.suffer_score)  #: a measure of heartrate intensity, available on premium users' activities only
            worksheet.write(row, col+13, activity.average_watts)  #: (undocumented) Average power during activity
            worksheet.write(row, col+14, activity.max_watts)  #: rides with power meter data only
            worksheet.write(row, col+15, activity.average_cadence)  #: (undocumented) Average cadence during activity
            worksheet.write(row, col+16, activity.kudos_count)  #: How many kudos received for activity
            worksheet.write(row, col+17, activity.location_city)  #: The activity location city
            worksheet.write(row, col+18, activity.calories)  #: Calculation of how many calories burned on activity
            worksheet.write(row, col+19, activity.pr_count)  #: How many new personal records earned for the activity

            row += 1
            col = 0  # reset

            athlete_total_distance_miles += distance_miles

        print(
            '=> Athlete total distance is {athlete_total_distance_miles} miles'.format(
                athlete_total_distance_miles=round(athlete_total_distance_miles, util.DEFAULT_DECIMAL_PLACES),
            )
        )
        total_distance_miles += athlete_total_distance_miles

    print(
        '\n=> Total distance is {total_distance_miles} miles'.format(
            total_distance_miles=round(total_distance_miles, util.DEFAULT_DECIMAL_PLACES),
        )
    )

    cursor.show()

    workbook.close()
    print(
        '\n=> Wrote "{filename}"\n'.format(
            filename=filename,
        )
    )

if __name__ == '__main__':
	# xlsx file is timestamped now
	now = datetime.datetime.now()
	filename = now.strftime(
        '%Y-%m-%d_%H-%M-%S_{athlete_data}.xlsx'.format(
            athlete_data='athlete_data',
        )
    )
	create_activity_workbook(filename)
