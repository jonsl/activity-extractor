
from stravalib.client import Client

CLIENT_ID=22927

ACCESS_TOKEN='6678266ba9422748554be8e5aaa46ea8dec5b39a'

# auth
client = Client()
url = client.authorization_url(client_id=CLIENT_ID,
        redirect_uri='http://localhost:8000/')
print('url={0}\n'.format(url))

client = Client(access_token=ACCESS_TOKEN)

# Extract the code from your webapp response
#code = '6678266ba9422748554be8e5aaa46ea8dec5b39a';#request.get('code') # or whatever your framework does
#access_token = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret='da48c5fcc8df8f640190027dd8c565ea6a57e835', code=code)

# Now store that access token somewhere (a database?)
client.access_token = ACCESS_TOKEN;#access_token
athlete = client.get_athlete()
print("For {id}, I now have an access token {token}".format(id=athlete.id, token=client.access_token))

# get club to work with
clubs=[]
for idx, club in enumerate(client.get_athlete_clubs()):
	clubs.append(club)
	print("{0}. {1} {2}".format(idx, club.id, club.name.encode()))

selected_club_idx = int(input('\nPlease enter club # > '))
print('selected club_id is {0}\n'.format(clubs[selected_club_idx].id))

# get activities for the club
print('{0} Activities'.format(clubs[selected_club_idx].name.encode()))
club_activities=[]
total_distance = 0
for idx, club_activity in enumerate(client.get_club_activities(clubs[selected_club_idx].id)):
	club_activities.append(club_activity)
	print('{0}. {1} {2}:{3} start_date={4} type={5} distance={6} moving_time={7} average_speed={8} max_speed={9} total_elevation_gain={10}'.format(
		idx, club_activity.athlete, club_activity.id, club_activity.name, club_activity.start_date, club_activity.type,
		club_activity.distance, club_activity.moving_time, club_activity.average_speed, club_activity.max_speed,
		club_activity.total_elevation_gain))
	total_distance += int(club_activity.distance)
	if float(club_activity.distance) == 0.0:
		print('distance is 0')
#	if float(club_activity.moving_time) == 0.0:
#		print('moving_time is 0')

print('Total activities distance is {0}KM'.format(total_distance/1000.0))

selected_activity_idx = int(input('\nPlease enter activity # > '))
print('selected activity_id is {0}\n'.format(club_activities[selected_activity_idx].id))

