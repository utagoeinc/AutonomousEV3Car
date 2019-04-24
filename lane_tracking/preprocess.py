import os

data_dir = os.path.join(os.getcwd(), 'data')

# create train.txt
with open(os.path.join(data_dir, 'train.txt'), 'w') as train_txt:
    pass

for date_dir in os.listdir(data_dir):
    if os.path.isdir(os.path.join(data_dir, date_dir)):
        with open(os.path.join(data_dir, date_dir, 'actions.txt'), 'r') as actions:
            action_list = actions.readlines()

        image_list = sorted(os.listdir(os.path.join(data_dir, date_dir, 'images')))

        assert len(action_list) == len(image_list)

        with open(os.path.join(data_dir, 'train.txt'), 'a') as train_txt:
            for index in range(len(action_list)):
                train_txt.write('{}, {}'.format(os.path.join(date_dir, 'images', image_list[index]), action_list[index]))
                print('{}, {}'.format(os.path.join(date_dir, 'images', image_list[index]), action_list[index].replace('\n', '')))
