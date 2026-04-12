import database_api as db
import calculate_feature as cf
import os
import shutil
import face_cap
import calculate_feature

root = 'face_data'
source = 'verified'

ls = db.get_image()

for col in ls:
    # print(col[0])
    dir = f'{root}/{col[0]}/image'
    os.makedirs(dir, exist_ok=True)
    for i in col[1]:
        shutil.copy(f'{source}/{col[0]}/image/{i}.jpg', f'{dir}/{i}.jpg')
print('All images copied!')

face_cap.main()

calculate_feature.main()