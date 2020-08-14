#!/usr/bin/env python

from __future__ import print_function

import json
import os
import time
import uuid

import imageio as imageio
import numpy as np
from requests import post


# from scipy.misc.pilutil import imread, imsave


def like_or_nope(_filename_paths, model_api_host, model_id):
    scores = []
    for _url in _filename_paths:
        scores.append(call_model(imageio.imread(_url), api_host=model_api_host, model_id=model_id))
    print(scores)
    if np.any(np.array(scores) > 40.0):
        return 'like'
    return 'nope'


def call_model(image, api_host='', model_id=''):
    tmp_filename = str(uuid.uuid4()) + '.png'
    imageio.imsave(tmp_filename, image)

    path = '/models/images/classification/classify_one.json'
    files = {'image_file': open(tmp_filename, 'rb')}

    try:
        r = post(api_host + path, files=files, params={'job_id': model_id})
    finally:
        os.remove(tmp_filename)
        time.sleep(2)  # wait 2 seconds.

    result = r.json()
    if result.get('error'):
        raise Exception(result.get('error').get('description'))

    for res_element in result['predictions']:
        if 'LIKE' in res_element[0]:
            print(result)
            return res_element[1]
    return 0.0


if __name__ == '__main__':

    credentials = json.load(open('credentials.json', 'r'))
    target_dir = 'FINAL_NOPE/'
    for filename in os.listdir(target_dir):
        if filename.endswith(".jpg"):
            try:
                img = imread(target_dir + filename)
                call_model(img, credentials['API_HOST'], credentials['MODEL_ID'])
            except Exception as e:
                print(str(e))
