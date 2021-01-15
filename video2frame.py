import cv2
import os
import shutil
import tarfile
import zipfile
import gzip
import shutil


def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)


included_activities = {'001': 'drink', '041': 'sneezecough',
                       '042': 'staggering', '043': 'fallingdown', '044': 'headache',
                       '045': 'chestpain', '046': 'backpain', 'A47': 'neckpain', '048': 'nausea',
                       '049': 'fanself', '103': 'yawn', '0104': 'stretch', '0105': 'blownose'}
base_path = 'ntu_dataset'

try:
    os.mkdir('train_frames_v0.3')

except OSError:
    pass
dirs = os.listdir(base_path)
print('processing train folder ...')

for dir in dirs:
    try:
        try:
            shutil.rmtree(os.path.join(base_path, 'nturgb+d_rgb'))
            print('Removed Old')
        except:
            pass
        opener, mode = zipfile.ZipFile, 'r'
        file_unzipped = opener(os.path.join(base_path, dir), mode)
        try:
            file_unzipped.extractall(path=base_path)
        finally:
            file_unzipped.close()
        for file in os.listdir(os.path.join(base_path, 'nturgb+d_rgb')):
            if file.split('A')[1].split('_')[0] in included_activities.keys():
                vidcap = cv2.VideoCapture(os.path.join(base_path, 'nturgb+d_rgb', file))
                folder_name = included_activities[file.split('A')[1].split('_')[0]] + '_' + file.replace('.avi', '')
                try:
                    os.mkdir('train_frames_v0.3/{}'.format(folder_name))
                except OSError:
                    pass
                success, image = vidcap.read()
                count = 0
                success = True
                while success:
                    resized_image = cv2.resize(image, (1280, 720))
                    cv2.imwrite('train_frames_v0.3/{}/frame{}.jpg'.format(folder_name, count),
                                resized_image)  # save frame as JPEG file
                    success, image = vidcap.read()
                    # print('Read a new frame: ', success)
                    count += 1
                print('train_frames_v0.3/{} done!'.format(folder_name))
    except Exception as e:
        print(str(e))
        pass
