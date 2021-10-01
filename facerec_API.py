import requests

data = {"existing_image_path":"C:/Users/yuhay/Desktop/facerec_webcam/BEY.jpg",
        "analysis_image_path":"C:/Users/yuhay/Desktop/facerec_webcam/test_img.jpg"}

r = requests.post('http://127.0.0.1:8000/',
                  data=data)


print(r)

task = requests.form.to_dict(flat=True)
url = '/http://127.0.0.1:8000/'
print(requests.url_root + url)

response = requests.post(requests.url_root + url, json=task)
print('response from server :', response.text)

dictFromServer = response.json()
print(task, dictFromServer)




