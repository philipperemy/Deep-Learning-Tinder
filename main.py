<<<<<<< HEAD
import json
import os
import sys

import wget

import request_model as model
import tinder_api as ti
from tinder_token import get_access_token


def stats(likes, nopes):
    prop_likes = (float(likes) / (likes + nopes)) * 100.0
    prop_nopes = 100.0 - prop_likes
    print('likes = {} ({}%), nopes = {} ({}%)'.format(likes, prop_likes,
                                                      nopes, prop_nopes))
=======
#!/usr/bin/env python

import argparse
import json
import os
import sys
import urllib
from random import randint

import requests
from datetime import datetime

# super LIKE '/like/' + likedUserId + '/super'

headers = {
    'app_version': '3',
    'platform': 'ios',
}

# https://www.facebook.com/connect/login_success.html#access_token=EAAGm0PX4ZCpsBALpCKwbGaPYlWOi9oOQs91YLpm1fWZB1pZBMaAfz3okCnx4JvDtho5pGT28OdCVIdvPPePW9lVTnV8BhTxyZAmW3lrfS1KZAWsDjH0ci6juoY55lZAikCTGOZBieqQoviZCgS9dYbUa07CaB5nP4kTflMb0ZAiinogZDZD&expires_in=6217

# get your tinder token here https://gist.github.com/rtt/10403467
fb_id = 'philippe.remy.161'
fb_auth_token = 'EAAGm0PX4ZCpsBAGRf6fFwCGyFR2rywZB14XbEZAoWM6OszX3VDFemkUjaSH2ZCuPcwypUekjPEFfcHE1ZCK3mzbGA93syZCKVQugd7YZBkXPZAVgJAFZBKbBBrvRNVmneQPk3WKsu2IrBC36t8CbluaZCcOI8k4vn6cAsHUVMT2MyVTgZDZD'


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


def like_or_nope():
    return 'nope' if randint(1, 100) == 31 else 'like'


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


def change_location(tinder_token):
    req = requests.post(
        'https://api.gotinder.com/user/ping',
        headers=get_headers(tinder_token),  # NYC 40.7128 N, 74.0059
        # tokyo 35.6895 N, 139.6917
        data=json.dumps({'lat': 35.6895, 'lon': 139.6917})
    )
    try:
        return req.json()
    except:
        return None
>>>>>>> parent of 744d59f... big refacto


def main():
    credentials = json.load(open('credentials.json', 'r'))
    fb_id = credentials['FB_ID']
    fb_auth_token = get_access_token(credentials['FB_EMAIL_ADDRESS'], credentials['FB_PASSWORD'])
    model_api_host = str(credentials['API_HOST'])
    model_id = str(credentials['MODEL_ID'])

<<<<<<< HEAD
    print('Deep Learning Tinder bot')
    print('----------')
    print('FB_ID = {}'.format(fb_id))
    print('FB_AUTH_TOKEN = {}'.format(fb_auth_token))
    print('MODEL_API_HOST = {}'.format(model_api_host))
    print('MODEL_ID = {}'.format(model_id))

    like_count = 0
    nope_count = 0
=======
    parser = argparse.ArgumentParser(description='Tinder automated bot')
    parser.add_argument('-l', '--log', type=str, default='activity.log', help='Log file destination')

    args = parser.parse_args()

    print 'Tinder bot'
    print '----------'
    matches = 0
    liked = 0
    nopes = 0
>>>>>>> parent of 744d59f... big refacto

    while True:
        token = auth_token(fb_auth_token, fb_id)

        print 'tinder token={}'.format(token)

        # print(profile())
        # exit(0)

        if not token:
            print 'could not get token'
            sys.exit(0)

        # lat = 35.6895
        # lon = 139.6917
        # for i in range(20):
        #    new_lon = lon - i
        #    print('lat = {}, lon = {}'.format(lat, new_lon))
        #    print(change_loc(lat, new_lon))
        lat = 34.7
        lon = 135.5
        print(change_loc(lat, lon, token))
        print(profile(token))

        # http://words.alx.red/tinder-api-2-profile-and-geolocation/
        # print(change_location())
        # exit(1)

        for user in recommendations(token):
            if not user:
                break

<<<<<<< HEAD
=======
            print unicode(user)

>>>>>>> parent of 744d59f... big refacto
            count_photos = 1
            for urls in user.d['photos']:
                directory = "data/" + str(user.age) + "/" + str(user.user_id) + "/"

                if 'tinder_rate_limited_id' in directory:
                    print('Limit reached.')
                    exit(0)

                if not os.path.exists(directory):
                    os.makedirs(directory)

                url = urls['url']
                filename_path = directory + str(count_photos) + ".png"
                count_photos += 1
<<<<<<< HEAD
                print(url, "=>", filename_path)
                wget.download(url, out=filename_path, bar=None)
                filename_paths.append(filename_path)
            try:
                action = model.like_or_nope(filename_paths,
                                            model_api_host=model_api_host,
                                            model_id=model_id)
                if action == 'like':
                    like_count += 1
                    print(' -> Like')
                    stats(like_count, nope_count)
                    match = ti.like(user.user_id)
=======
                print url, "=>", filename_path
                urllib.urlretrieve(url, filename_path)

            try:
                action = 'nope'  # like_or_nope()
                if action == 'like':
                    print ' -> Like'
                    match = like(user.user_id)
>>>>>>> parent of 744d59f... big refacto
                    if match:
                        print ' -> Match!'

                    with open('./liked.txt', 'a') as f:
                        f.write(user.user_id + u'\n')

                else:
<<<<<<< HEAD
                    nope_count += 1
                    print(' -> nope')
                    stats(like_count, nope_count)
                    ti.nope(user.user_id)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
=======
                    print ' -> nope'
                    nope(user.user_id)

            except Exception, e:
                print 'networking error %s' % user.user_id
                print e
                print str(e)

            s = float(randint(250, 2500) / 1000)
>>>>>>> parent of 744d59f... big refacto
