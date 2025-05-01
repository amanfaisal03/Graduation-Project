from rest_framework.response import Response 
from rest_framework.decorators import api_view
from STT import *



@api_view(['GET'])
def check_video(request):
    input_url = request.query_params.get('input_url')  
    if not input_url:
        return Response({'error': 'No input URL provided.'}, status=400)
    
    





