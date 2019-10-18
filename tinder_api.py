import json
from datetime import datetime

import requests

headers = {
    'app_version': '3',
    'platform': 'ios',
}


# super LIKE '/like/' + likedUserId + '/super'


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
        # 'https://api.gotinder.com/auth',
        'https://api.gotinder.com/v2/auth/login/facebook',
        headers=h,
        # data=json.dumps({'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
        # data=json.dumps({'facebook_token': fb_auth_token}
        data=json.dumps({'token': fb_auth_token})
    )
    try:
        return req.json()['data']['api_token']
    except:
        return None


def recommendations(auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    r = requests.get('https://api.gotinder.com/user/recs', headers=h)
    if r.status_code == 401 or r.status_code == 504:
        raise Exception('Invalid code')

    if 'results' not in r.json():
        print(r.json())

    for result in r.json()['results']:
        print(result)
        yield User(result)


def super_like(user_id):
    try:
        u = 'https://api.gotinder.com/like/%s/super' % user_id
        d = requests.get(u, headers=headers, timeout=0.7).json()
    except KeyError:
        raise
    else:
        return d['match']


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


def get_headers(tinder_token):
    return {'host': 'api.gotinder.com',
            'Authorization': "Token token='#{'" + str(tinder_token) + "'}'",
            'x-client-version': '47217',
            'app-version': '467',
            'Proxy-Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB;q=1, fr-FR;q=0.9',
            'platform': 'ios',
            'Content-Type': 'application/json',
            'User-Agent': 'Tinder/4.7.2 (iPhone; iOS 9.2.1; Scale/2.00)',
            'Connection': 'keep-alive',
            'X-Auth-Token': str(tinder_token),
            'os_version': '90000200001'}


def change_loc(lat, lon, tinder_token):
    req = requests.post(
        'https://api.gotinder.com/user/ping',
        headers=get_headers(tinder_token),  # NYC 40.7128 N, 74.0059
        # tokyo 35.6895 N, 139.6917
        data=json.dumps({'lat': lat, 'lon': lon})
    )
    try:
        return req.json()
    except:
        return None


def profile(tinder_token):
    req = requests.post(
        'https://api.gotinder.com/profile',
        headers=get_headers(tinder_token))
    try:
        return req.json()
    except:
        return None
