
CLIENT_ID=22927

ACCESS_TOKEN='6678266ba9422748554be8e5aaa46ea8dec5b39a'

CLUB_ID=338808

from stravalib.client import Client

# activityExtractor

client = Client()
url = client.authorization_url(client_id=CLIENT_ID,
                               redirect_uri='http://myapp.example.com/authorization')

print('url={0}\n'.format(url))

client = Client(access_token=ACCESS_TOKEN)

# get club_id to work with
club_ids=[]
for idx, club in enumerate(client.get_athlete_clubs()):
    club_ids.append(int(club.id))
    print("{0}. {1} {2}".format(idx, club.id, club.name.encode()))

inp = input('\nPlease enter club # > ')
selected_club_id = club_ids[int(inp)]
print('selected club_id is {0}\n'.format(selected_club_id))

# get activities for the club
activity_ids=[]
for idx, activity in enumerate(client.get_club_activities(selected_club_id)):
    activity_ids.append(int(activity.id))
    print("{0}. {1} {2}".format(idx, activity.id, activity.name.encode()))

inp = input('\nPlease enter activity # > ')
selected_activity_id = activity_ids[int(inp)]
print('selected activity_id is {0}\n'.format(selected_activity_id))


