import requests
#
# mp_encoder = {
#         'image': ('test.jpg', open('C:/Users/yuhay/Desktop/tamy.jpg', 'rb')),
#         'gender':(None, 0),
#         'age': (None, 11),
#         'id': (None, "222nada"),
#         'company': (None, 'hayung_2222test')
#     }
#
#
# r = requests.post(
#     'https://withimgpu.com/enrollment_img/',
#     # 'http://127.0.0.1:8000/enrollment_img/',
#     files=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
#     # The MultipartEncoder provides the content-type header with the boundary:
#     # headers={'Content-Type': mp_encoder.content_type}

# )
#
# print('r.content >>> ', r.content)
# print('r >>> ', r)

##############################################################################################################

mp_encoder = {
        'image': ('test.jpg', open('C:/Users/yuhay/Desktop/tamy.jpg', 'rb')),
        'id': (None, "222nada"),
        'company': (None, 'hayung_2222test')
    }


r = requests.post(
    'https://withimgpu.com/analy_img/',
    # 'http://127.0.0.1:8000/analy_img/',
    files=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
    # The MultipartEncoder provides the content-type header with the boundary:
    # headers={'Content-Type': mp_encoder.content_type}
)

print('r.content >>> ', r.content)
print('r >>> ', r)