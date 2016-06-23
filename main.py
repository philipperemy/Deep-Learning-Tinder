#!/usr/bin/env python

from __future__ import print_function

import json
import os
import sys
import urllib

import tinder_api as ti

# get your tinder token here https://gist.github.com/rtt/10403467
# and populate the json credentials.json
credentials = json.load(open('credentials.json', 'r'))

fb_id = credentials['FB_ID']
fb_auth_token = credentials['FB_AUTH_TOKEN']

ti.MODEL_THRESHOLD = 25.0

if __name__ == '__main__':

    print('Deep Learning Tinder bot')
    print('----------')
    print('FB_ID = {}'.format(fb_id))
    print('FB_AUTH_TOKEN = {}'.format(fb_auth_token))

    while True:
        token = ti.auth_token(fb_auth_token, fb_id)

        print('TINDER_TOKEN = {}'.format(token))

        if not token:
            print('could not get Tinder token. Program will exit.')
            sys.exit(0)

        print('Successfully connected to Tinder servers.')

        lat = 34.7
        lon = 135.5
        # http://words.alx.red/tinder-api-2-profile-and-geolocation/
        print(ti.change_loc(lat, lon, token))
        my_profile = ti.profile(token)
        print(json.dumps(my_profile, indent=4, sort_keys=True))

        for user in ti.recommendations(token):
            if not user:
                break

            print(ti.get_brief_desc(user))

            count_photos = 1
            filename_paths = []
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
                print(url, "=>", filename_path)
                urllib.urlretrieve(url, filename_path)
                filename_paths.append(filename_path)
            try:
                action = ti.like_or_nope(filename_paths)
                if action == 'like':
                    print(' -> Like')
                    match = ti.like(user.user_id)
                    if match:
                        print(' -> Match!')
                else:
                    print(' -> nope')
                    ti.nope(user.user_id)

            except Exception, e:
                print('networking error %s' % user.user_id)
                print(e)
                print(str(e))
