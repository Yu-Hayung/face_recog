from .task import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from .models import *
from django.utils.datastructures import MultiValueDictKeyError

@api_view(['POST'])
@permission_classes([AllowAny])
def enrollment_img(request):

    try:
        id = request.POST["id"]
        company = request.POST["company"]

        try:
            age = request.POST["age"]
        except MultiValueDictKeyError:
            age = None

        try:
            gender = request.POST["gender"]
        except MultiValueDictKeyError:
            gender = None

        try:
            image = request.FILES.get('image').read()
        except MultiValueDictKeyError:
            response_dict = {"result": {"message": "Fail", "reason": "File type err"}}


        if len(image) < 307200 or len(image) > 512000:
            response_dict = {"result": {"message": "Fail", "reason": "img size err"}}


        else:
            result = enroll_img(id, company, image)
            Lookup = FaceRecogApi.objects.filter(id=id, company=company).values()
            # print('Lookup >>> ', Lookup)

            if Lookup:
                idx = Lookup[0]['no']
                db_update = FaceRecogApi.objects.get(no=idx)
                db_update.image = result
                db_update.save()

            else:
                res = FaceRecogApi(id=id, gender=gender, age=age, company=company, image=result)
                res.save()


            response_dict = {"result": "Success"}

        return JsonResponse(response_dict)


    except Exception as e:
        response_dict = {"result": "Fail"}

        save_route = "C:/Users/yuhay/Desktop/enrollment_img_ERR_text.txt"
        # save_route = "/home/ubuntu/face_recog_fin/enrollment_img_ERR_text.txt"

        f = open(save_route, 'a')
        str_a = type(e)
        str_b = str(e) + '//'
        str_txt = '\n' + '@company_:' + str(company) + '@id_:' + str(id) + '@ERR_:' + str_b + str(str_a)
        f.write(str_txt)

        f.close()

        return JsonResponse(response_dict)


@api_view(['POST'])
@permission_classes([AllowAny])
def analy_img(request):

    try:
        id = request.POST["id"]
        company = request.POST["company"]
        try:
            image = request.FILES.get('image').read()

        except MultiValueDictKeyError:
            response_dict = {"result": {"message": "Fail", "reason": "File type err"}}

        if len(image) < 307200 or len(image) > 512000:
            response_dict = {"result": {"message": "Fail", "reason": "img size err"}}

        else:
            result = face_analy(id, company, image)
            response_dict = {"result": result}
            print('response_dict >>>>> ',  response_dict)

        return JsonResponse(response_dict)

    except Exception as e:
        response_dict = {"result": "Fail"}

        save_route = "C:/Users/yuhay/Desktop/analy_img_ERR_text.txt"
        # save_route = "/home/ubuntu/face_recog_fin/analy_img_ERR_text.txt"
        f = open(save_route, 'a')
        str_a = type(e)
        str_b = str(e) + '//'
        str_txt = '\n' + '@company_:' + str(company) + '@id_:' + str(id) + '@ERR_:' + str_b + str(str_a)
        f.write(str_txt)

        f.close()

        return JsonResponse(response_dict)
