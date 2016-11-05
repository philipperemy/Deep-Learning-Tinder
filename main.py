#!/usr/bin/env python

from __future__ import print_function

import json
import os
import sys
import urllib

import request_model as model
import tinder_api as ti

# get your tinder token here https://gist.github.com/rtt/10403467
# and populate the json credentials.json
credentials = json.load(open('credentials.json', 'r'))

fb_id = credentials['FB_ID']
fb_auth_token = credentials['FB_AUTH_TOKEN']
model_api_host = str(credentials['API_HOST'])
model_id = str(credentials['MODEL_ID'])


def stats(likes, nopes):
    prop_likes = (float(likes) / (likes + nopes)) * 100.0
    prop_nopes = 100.0 - prop_likes
    print('likes = {} ({}%), nopes = {} ({}%)'.format(likes, prop_likes,
                                                      nopes, prop_nopes))


if __name__ == '__main__':

    print('Deep Learning Tinder bot')
    print('----------')
    print('FB_ID = {}'.format(fb_id))
    print('FB_AUTH_TOKEN = {}'.format(fb_auth_token))
    print('MODEL_API_HOST = {}'.format(model_api_host))
    print('MODEL_ID = {}'.format(model_id))

    like_count = 0
    nope_count = 0

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

            print(unicode(user))

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
                action = model.like_or_nope(filename_paths,
                                            model_api_host=model_api_host,
                                            model_id=model_id)
                if action == 'like':
                    like_count += 1
                    print(' -> Like')
                    stats(like_count, nope_count)
                    match = ti.like(user.user_id)
                    if match:
                        print(' -> Match!')
                else:
                    nope_count += 1
                    print(' -> nope')
                    stats(like_count, nope_count)
                    ti.nope(user.user_id)

            except Exception as e:
                print(e)
