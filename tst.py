import data_transform

NEW_DIR = "/Users/philipperemy/PycharmProjects/Tinder/profile_pics_resize/"

# data_transform.load_data(NEW_DIR, EXT)

old_dir = 'data'
new_dir = 'DD_Tinder'

data_transform.process_data(old_dir, new_dir, '.png')