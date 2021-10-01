from __future__ import absolute_import, unicode_literals
import face_recognition
import cv2
import numpy as np
import os



def image_analysis(existing_image_path, analysis_image_path):
    # existing_image_path = 저장된 이미지 경로
    # analysis_image_path = 비교할 이미지 경로

    if existing_image_path.endswith('.jpg') is True or existing_image_path.endswith('.png') is True or existing_image_path.endswith('.jpng') is True :

        known_face_encodings = []
        known_face_name = '0'

        image = face_recognition.load_image_file(existing_image_path)
        image_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(image_encoding)

        process_this_frame = True


        frame = cv2.imread(analysis_image_path, cv2.IMREAD_COLOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


            for i_face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, i_face_encoding)
                name = 1

                face_distances = face_recognition.face_distance(known_face_encodings, i_face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_name[best_match_index]

    else:
        src = existing_image_path
        file_names = os.listdir(src)

        # 파일명 소문자 일괄 전환
        file_list = []
        for i in file_names:
            i_lower = i.lower()
            if i_lower.endswith('.jpg') is True or i_lower.endswith('.png') is True or existing_image_path.endswith('.jpng') is True:
                file_list.append(i)

        known_face_encodings = []
        known_face_names = []

        for i in file_list:
            name = str(i)
            img_dir = src + '/' + name
            known_face_names.append(img_dir)
            image = face_recognition.load_image_file(img_dir)
            globals()[img_dir] = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(globals()[img_dir])
        else:
            pass

        process_this_frame = True

        frame = cv2.imread(analysis_image_path, cv2.IMREAD_COLOR)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for i_face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, i_face_encoding)
                name = 1

                face_distances = face_recognition.face_distance(known_face_encodings, i_face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = 0



    return int(name)


