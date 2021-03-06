import face_recognition
import cv2
import numpy as np
import os
import time

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.



src = 'C:/Users/yuhay/Desktop/facerec_webcam/test_edu_img' # 이미지 경로 .jpg / .png
file_names = os.listdir(src)




# 파일명 소문자 일괄 전환
file_list = []
for i in file_names:
    i_lower = i.lower()
    if i_lower.endswith('.jpg') is True or i_lower.endswith('png'):
        file_list.append(i)

print('file_list >>', file_list)

known_face_encodings = []
known_face_names = []

start_time = time.time()

for i in file_list:
    name = str(i)
    img_dir = src + '/' + name
    known_face_names.append(img_dir)
    image = face_recognition.load_image_file(img_dir)
    globals()[img_dir] = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(globals()[img_dir])
else:
    pass

encodings_time = time.time() - start_time
known_face_encodings_len = len(known_face_encodings)



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

Unknown_count = 0
known_count = 0

src = 'C:/Users/yuhay/Desktop/facerec_webcam/test_img' # 이미지 경로 .jpg / .png
file_names2 = os.listdir(src)

test_img_list = []
for i in file_names2:
    i_lower = i.lower()
    if i_lower.endswith('.jpg') is True or i_lower.endswith('png'):
        test_img = src + '/' + i
        test_img_list.append(test_img)

print('test_img_list >> ', test_img_list)

for i in test_img_list:
    frame = cv2.imread(i, cv2.IMREAD_COLOR)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # 점수 반환기
    if face_names == ['Unknown']:
        Unknown_count += 1
    else:
        known_count += 1

#     print('======================== << match >> ==================================')
#     print('img_name >> ', i)
#     print('match_name >> ', name)
#     print('Unknown_count >> ', Unknown_count, 'known_count >> ', known_count)
#
# print('=================<< encodings_time >>===========================')
# print('encodings_time >>', known_face_encodings_len, '(이미지 개수)  / ', encodings_time)
#
# # 정확도 확률 계산
# print('================================================================')
# print('TOTAL // Unknown_count >> ', Unknown_count, 'known_count >> ', known_count)
# total_count = Unknown_count + known_count
# print('total_count >> ', total_count)
# score = known_count / total_count
# print('score >> ', score, '%')


