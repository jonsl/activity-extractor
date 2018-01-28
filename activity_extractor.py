
from stravalib.client import Client

CLIENT_ID=22927

ACCESS_TOKEN='6678266ba9422748554be8e5aaa46ea8dec5b39a'

# auth
client = Client()
url = client.authorization_url(client_id=CLIENT_ID,
        redirect_uri='http://localhost:8888/authorized')
print('url={0}\n'.format(url))

client = Client(access_token=ACCESS_TOKEN)

# Extract the code from your webapp response
code = 13243546;#request.get('code') # or whatever your framework does
access_token = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret='da48c5fcc8df8f640190027dd8c565ea6a57e835', code=code)

# Now store that access token somewhere (a database?)
client.access_token = access_token
athlete = client.get_athlete()
print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))




# get club to work with
clubs=[]
for idx, club in enumerate(client.get_athlete_clubs()):
    clubs.append(club)
    print("{0}. {1} {2}".format(idx, club.id, club.name.encode()))

selected_club_idx = int(input('\nPlease enter club # > '))
print('selected club_id is {0}\n'.format(clubs[selected_club_idx].id))

# get activity streams
#types = ['time', 'distance']
#streams = client.get_activity_streams(123, types=types, resolution='medium')
#if 'distance' in streams.keys():
#    print(streams['distance'].data)

# get activities for the club
print('{0} Activities'.format(clubs[selected_club_idx].name.encode()))
club_activities=[]
total_distance = 0
for idx, club_activity in enumerate(client.get_club_activities(clubs[selected_club_idx].id)):
    try:
        activity = client.get_activity(club_activity.id)
        club_activities.append(activity)
        print('{0}. {1}->{2}'.format(idx, activity.id, activity.name.encode()))
        total_distance += int(activity.distance)
    except Exception as e:
        print('Error cannot retrieve activity')

print('Total activities distance is {0}'.format(total_distance))

selected_activity_idx = int(input('\nPlease enter activity # > '))
print('selected activity_id is {0}\n'.format(club_activities[selected_activity_idx].id))


