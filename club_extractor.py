import datetime
import sys
import time
from datetime import timedelta

import cursor
from stravalib import unithelper
from stravalib.client import Client
from units import unit
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

import util


ACCESS_TOKEN = '6678266ba9422748554be8e5aaa46ea8dec5b39a'

def _create_athlete_map() -> str:
    athlete_map = {}
    # pull all data into a map of activity lists keyed by athlete name
    for idx, activity in enumerate(client.get_club_activities(selected_club.id)):
        key = util.athlete_fullname(
            activity.athlete.firstname,
            activity.athlete.lastname,
        )
        activity = {
            'name': activity.name,
            'distance': activity.distance,
            'moving_time': activity.moving_time,
            'elapsed_time': activity.elapsed_time,
            'total_elevation_gain': activity.total_elevation_gain,
            'type': activity.type,
            'workout_type': activity.workout_type,
        }
        athlete_map.setdefault(key, []).append(
            activity,
        )

    print(
        '\nProcessed {idx} activities for {athlete_count} athletes'.format(
            idx=idx + 1,
            athlete_count=len(athlete_map),
        )
    )
    return athlete_map

def create_club_workbook(filename: str, athlete_map: dict):
    workbook = Workbook(filename, {'default_date_format':'dd/mm/yy'})
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    row = 0
    col = 0

    worksheet.write(row, col, 'Name', bold)
    worksheet.write(row, col+1, 'Distance (km)', bold)
    worksheet.write(row, col+2, 'Moving Time (s)', bold)
    worksheet.write(row, col+3, 'Elapsed Time (s)', bold)
    worksheet.write(row, col+4, 'Total Elevation Gain (m)', bold)
    worksheet.write(row, col+5, 'Activity Type', bold)

    worksheet.set_column('A:A', 14)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 28)
    worksheet.set_column('F:F', 18)

    row += 1

    total_distance_kilometers = float(0)

    for key in athlete_map:

        athlete_distance_kilometers = 0
        athlete_moving_time_seconds = 0
        athlete_elapsed_time_seconds = 0
        athlete_total_elevation_gain_meters = 0

        for idx, activity in enumerate(athlete_map[key]):
            distance_kilometers = unithelper.kilometers(activity['distance'])
            athlete_distance_kilometers += float(distance_kilometers)
            moving_time = activity['moving_time']
            athlete_moving_time_seconds += moving_time.seconds
            elapsed_time = activity['elapsed_time']
            athlete_elapsed_time_seconds += elapsed_time.seconds
            total_elevation_gain_meters = unithelper.meters(activity['total_elevation_gain'])
            athlete_total_elevation_gain_meters += float(total_elevation_gain_meters)

            worksheet.write(row, col, key)
            worksheet.write(row, col+1, round(float(distance_kilometers), util.DEFAULT_DECIMAL_PLACES))
            worksheet.write(row, col+2, moving_time.seconds)
            worksheet.write(row, col+3, elapsed_time.seconds)
            worksheet.write(row, col+4, float(total_elevation_gain_meters))
            worksheet.write(row, col+5, activity['type'])

            row += 1
            col = 0

        total_distance_kilometers += athlete_distance_kilometers

    print(
        '=> Total distance is {total_distance_kilometers} km'.format(
            total_distance_kilometers=round(total_distance_kilometers, util.DEFAULT_DECIMAL_PLACES),
        )
    )

    workbook.close()
    print(
        '\n=> Wrote "{filename}"\n'.format(
            filename=filename,
        )
    )

if __name__ == '__main__':
    spinner = util.spinning_cursor()

    client = Client(access_token=ACCESS_TOKEN)
    athlete = client.get_athlete()
    print(
        '\n=> Processing clubs for athlete: "{key}"\n'.format(
            key=util.athlete_fullname(
                athlete.firstname,
                athlete.lastname,
            )
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

    athlete_map = _create_athlete_map()

    create_club_workbook(filename, athlete_map)
