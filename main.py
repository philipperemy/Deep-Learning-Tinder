import argparse
from datetime import datetime
import json
from random import randint
import requests
import sys
import urllib
import os

# super LIKE '/like/' + likedUserId + '/super'

headers = {
    'app_version': '3',
    'platform': 'ios',
}

# get your tinder token here https://gist.github.com/rtt/10403467
fb_id = 'philippe.remy185'
fb_auth_token = 'CAAGm0PX4ZCpsBAGDFrnVjS119I62PvogRUbDaIH2LHHKgtUKJmTqte8yPir8vz7ws8zwq00gLUTslNxKqiSXPPZBOZAxnL9lOMou6fX75A0hL51ExRfDW3MaWIieF35YpRvJZC50Iim079PVZB1l240p7KEELE4x1WN2LSTkCZAqsRUMKocSeaoYTVBMeEZAfHUOZAzclrZCBfQZDZD'

class User(object):
    def __init__(self, data_dict):
        self.d = data_dict

    @property
    def user_id(self):
        return self.d['_id']

    @property
    def ago(self):
        raw = self.d.get('ping_time')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            secs_ago = int(datetime.now().strftime("%s")) - int(d.strftime("%s"))
            if secs_ago > 86400:
                return u'{days} days ago'.format(days=secs_ago / 86400)
            elif secs_ago < 3600:
                return u'{mins} mins ago'.format(mins=secs_ago / 60)
            else:
                return u'{hours} hours ago'.format(hours=secs_ago / 3600)

        return '[unknown]'

    @property
    def bio(self):
        try:
            x = self.d['bio'].encode('ascii', 'ignore').replace('\n', '')[:50].strip()
        except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError):
            return '[garbled]'
        else:
            return x

    @property
    def age(self):
        raw = self.d.get('birth_date')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            return datetime.now().year - int(d.strftime('%Y'))

        return 0

    def __unicode__(self):
        return u'{name} ({age}), {distance}km, {ago}'.format(
            name=self.d['name'],
            age=self.age,
            distance=self.d['distance_mi'],
            ago=self.ago
        )


def auth_token(fb_auth_token, fb_user_id):
    h = headers
    h.update({'content-type': 'application/json'})
    req = requests.post(
        'https://api.gotinder.com/auth',
        headers=h,
        data=json.dumps({'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
    )
    try:
        return req.json()['token']
    except:
        return None


def recommendations(auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    r = requests.get('https://api.gotinder.com/user/recs', headers=h)
    if r.status_code == 401 or r.status_code == 504:
        raise Exception('Invalid code')
        print r.content

    if not 'results' in r.json():
        print r.json()

    for result in r.json()['results']:
        yield User(result)


def like(user_id):
    try:
        u = 'https://api.gotinder.com/like/%s' % user_id
        d = requests.get(u, headers=headers, timeout=0.7).json()
    except KeyError:
        raise
    else:
        return d['match']


def nope(user_id):
    try:
        u = 'https://api.gotinder.com/pass/%s' % user_id
        requests.get(u, headers=headers, timeout=0.7).json()
    except KeyError:
        raise


def like_or_nope():
    return 'nope' if randint(1, 100) == 31 else 'like'


def change_location():
    req = requests.post(
            'https://api.gotindaer.com/user/ping',
        data=json.dumps({'lat': 39.9167, 'lon': 116.3833})
    )
    try:
        return req.json()
    except:
        return None


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Tinder automated bot')
    parser.add_argument('-l', '--log', type=str, default='activity.log', help='Log file destination')

    args = parser.parse_args()

    print 'Tinder bot'
    print '----------'
    matches = 0
    liked = 0
    nopes = 0

    while True:
        token = auth_token(fb_auth_token, fb_id)

        if not token:
            print 'could not get token'
            sys.exit(0)

        # print "try to update location"
        # print change_location()
        # print "location updated"

        for user in recommendations(token):
            if not user:
                break

            print unicode(user)

            count_photos = 1
            for urls in user.d['photos']:
                directory = "data/" + str(user.age) + "/" + str(user.user_id) + "/"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                url = urls['url']
                filename_path = directory + str(count_photos) + ".png"
                count_photos += 1
                print url, "=>", filename_path
                urllib.urlretrieve(url, filename_path)

            try:
                action = 'nope'  # like_or_nope()
                if action == 'like':
                    print ' -> Like'
                    match = like(user.user_id)
                    if match:
                        print ' -> Match!'

                    with open('./liked.txt', 'a') as f:
                        f.write(user.user_id + u'\n')

                else:
                    print ' -> random nope :('
                    nope(user.user_id)

            except:
                print 'networking error %s' % user.user_id

            s = float(randint(250, 2500) / 1000)
