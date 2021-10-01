import face_recognition
import cv2
import numpy as np


def image_analysis(existing_image_path, analysis_image_path):
    known_face_encodings = []
    known_face_names = '1'

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
            name = 0

            face_distances = face_recognition.face_distance(known_face_encodings, i_face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]


    return int(name)


existing_image_path = "C:/Users/yuhay/Desktop/facerec_webcam/BEY.jpg"
# analysis_image_path = "C:/Users/yuhay/Desktop/facerec_webcam/BEY2.jpg"

# 불일치 이미지
analysis_image_path = "C:/Users/yuhay/Desktop/facerec_webcam/test_img.jpg"

test = image_analysis(existing_image_path, analysis_image_path)

print('일치 : 1 / 불일치 : 0')
print(test)

