
from stravalib.client import Client

CLIENT_ID=22927

ACCESS_TOKEN='6678266ba9422748554be8e5aaa46ea8dec5b39a'

# auth
client = Client()
url = client.authorization_url(client_id=CLIENT_ID,
                               redirect_uri='http://myapp.example.com/authorization')

client = Client(access_token=ACCESS_TOKEN)

print('url={0}\n'.format(url))

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
for idx, club_activity in enumerate(client.get_club_activities(clubs[selected_club_idx].id)):
   club_activities.append(club_activity)
   print('{0}. {1}->{2}'.format(idx, club_activity.id, club_activity.name.encode()))

selected_activity_idx = int(input('\nPlease enter activity # > '))
print('selected activity_id is {0}\n'.format(club_activities[selected_activity_idx].id))


