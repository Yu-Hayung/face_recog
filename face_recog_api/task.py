from __future__ import absolute_import, unicode_literals
import face_recognition
import cv2
import numpy as np
import os
import urllib.request
from ftplib import FTP
import ssl
from .models import *


def enroll_img(id, company, image):

    filename = str(company) + "_" + str(id) + ".jpg"  # api 서버
    img = cv2.imdecode(np.fromstring(image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    # save_route_server = "C:/Users/yuhay/Desktop/"
    save_route_server = "/home/ubuntu/face_recog_fin/save_img/"
    cv2.imwrite(save_route_server + filename, img)

    ftp = FTP()
    ftp.connect('withmind.cache.smilecdn.com', 21)
    ftp.login('withmind', 'dnlemakdlsem1!')
    ftp.cwd('./face_recog_img')


    nlst = company in ftp.nlst()

    if nlst == False:
        ftp.mkd('./' + str(company))
        ftp.cwd('./' + str(company))
    else:
        ftp.cwd('./' + str(company))

    upload_img = open(save_route_server + filename, 'rb') # 서버에 저장한 이미지 부르기 변수

    nlst_list = ftp.nlst()

    num = 1
    filename2 = '%s_%d.jpg' %(str(id), num)


    while filename2 in nlst_list:
        # print('filename2 >>>>>>>>', filename2)
        num = num + 1
        filename2 = '%s_%d.jpg' % (str(id), num)


    ftp.storbinary('STOR ' + filename2, upload_img)


    upload_img.close()
    ftp.close()
    os.remove(save_route_server + filename)
    server_route = "https://withmind.cache.smilecdn.com/face_recog_img/"

    # res = FaceRecogApi(id = id, gender = gender, age = age, company = company, image = server_route + filename)
    #
    # res.save()

    result = server_route + str(company) + '/' + filename2


    return result

def face_analy(id, company, image):

    try:
        enrollment_img_db = FaceRecogApi.objects.filter(id=id, company=company)
        enrollment_img_url = enrollment_img_db[0].image
    except Exception as e:
        result = {"result": " unregistered user "}
        return result

    context = ssl._create_unverified_context()
    enrollment_img = urllib.request.urlopen(enrollment_img_url, context=context)
    enrollment_img_data = face_recognition.load_image_file(enrollment_img)

    enrollment_encoding = face_recognition.face_encodings(enrollment_img_data)[0]
    enroll_face_encodings = [enrollment_encoding]

    str_id = str(id)
    face_name = str_id

    globals()[face_name] = face_recognition.face_encodings(enrollment_img_data)[0]
    enroll_face_encodings.append(globals()[face_name])

    compare_img = cv2.imdecode(np.fromstring(image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    compare_face_locations = face_recognition.face_locations(compare_img)
    compare_face_encodings = face_recognition.face_encodings(compare_img, compare_face_locations)

    ###############################################################################
    # 이미지 저장
    filename = str(company) + "_" + str(id) + ".jpg"

    # save_route_server = "C:/Users/yuhay/Desktop/"
    save_route_server = "/home/ubuntu/face_recog_fin/save_img/"
    cv2.imwrite(save_route_server + filename, compare_img)

    ftp = FTP()
    ftp.connect('withmind.cache.smilecdn.com', 21)
    ftp.login('withmind', 'dnlemakdlsem1!')
    ftp.cwd('./face_recog_img')

    # print('ftp.nlst() >>>', company in ftp.nlst())

    nlst = company in ftp.nlst()

    if nlst == False:
        ftp.mkd('./' + str(company))
        ftp.cwd('./' + str(company))
    else:
        ftp.cwd('./' + str(company))

    upload_img = open(save_route_server + filename, 'rb')

    nlst_list = ftp.nlst()

    num = 1
    filename2 = '%s_%d.jpg' % (str(id), num)

    while filename2 in nlst_list:
        # print('filename2 >>>>>>>>', filename2)
        num = num + 1
        filename2 = '%s_%d.jpg' % (str(id), num)

    ftp.storbinary('STOR ' + filename2, upload_img)

    ###############################################################################
    # 동일 여부 분석

    face_names = []
    for face_encoding in compare_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(enroll_face_encodings, face_encoding)

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(enroll_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = face_name[best_match_index]
            face_names.append(name)

        else:
            name = "Unknown"
            face_names.append(name)

    face_names_list = []
    for i in face_names:
        if i == "Unknown":
            face_names_list.append("dismatch")
        else:
            face_names_list.append("match")

    person_ = []
    num = 1
    for i in face_names_list:
        filename_num = 'person_%d' % int(num)
        num += 1
        person_.append(filename_num)

        result = dict(zip(person_, face_names_list))

    upload_img.close()
    ftp.close()
    os.remove(save_route_server + filename)

    return result


