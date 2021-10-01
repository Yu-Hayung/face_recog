from rest_framework.response import Response
import json
from .tasks import image_analysis
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse, HttpResponse

# @api_view(['GET'])
# def helloAPI(request):
#     return Response('hello')

@api_view(['POST'])
@permission_classes([AllowAny])
def post(request):
    request1 = json.dumps(request.data)
    insert_data = json.loads(request1)
    existing_image_path = insert_data.get("existing_image_path")
    analysis_image_path = insert_data.get("analysis_image_path")

    analysis_result = image_analysis(existing_image_path, analysis_image_path)
    print("a >>>>>>>> ", analysis_result)

    # response_dict = {"msessage": "OK", "status": "200"}

    result = '일치 : 0 / 불일치 : 1 >>>>   결과 : ', analysis_result
    # asdasdd

    return HttpResponse(result, status=200)
    # return JsonResponse(response_dict)