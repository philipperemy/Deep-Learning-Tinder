import os

import numpy as np
from scipy import misc


# DIR = "/Users/philipperemy/PycharmProjects/Tinder/profile_pics/"
# NEW_DIR = "/Users/philipperemy/PycharmProjects/Tinder/profile_pics_resize/"
# EXT = ".png"


def process_data(old_dir, new_dir, ext):
    image_paths = []
    for dir_path, _, file_names in os.walk(old_dir):
        for filename in [f for f in file_names if f.endswith(ext)]:
            image_paths.append(os.path.join(dir_path, filename))

    N = len(image_paths)
    print "found", N, "images."
    i = 0
    import shutil
    import uuid
    for image_path in image_paths:
        try:
            i += 1
            print "reading", image_path, "(", i, "/", N, ")"

            # new_resize = (256, 256)
            # print "resizing", file_handle.size, "=>", new_resize
            # file_handle = file_handle.resize(new_resize, Image.ANTIALIAS)
            file_name = str(uuid.uuid1()) + os.path.basename(image_path)
            new_full_filename = os.path.join(new_dir, file_name)
            print "writing to", new_full_filename
            shutil.copy(image_path, new_full_filename)
        except IOError as ioe:
            print "error:", ioe, "skipping."


def load_data(dir_name, ext):
    image_paths = []
    for dir_path, _, file_names in os.walk(dir_name):
        for filename in [f for f in file_names if f.endswith(ext)]:
            image_paths.append(os.path.join(dir_path, filename))

    N = len(image_paths)
    X_train = np.zeros((N, 3, 256, 256), dtype="uint8")
    y_train = np.zeros((N,), dtype="uint8")

    i = 0
    for image_path in image_paths:
        image = misc.imread(image_path)
        X_train[i] = image.reshape(3, 256, 256)
        label = image_path.split("/")[-2]
        y_train[i] = int(label == 'like')
        i += 1

        if i % (N / 10) == 0 or i == N:
            print "loaded", i, "images in memory."

    X_test = X_train
    y_test = y_train
    return (X_train, y_train), (X_test, y_test)
