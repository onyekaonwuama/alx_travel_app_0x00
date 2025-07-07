from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'Welcome to ALX Travel App API',
        'endpoints': {
            'admin': reverse('admin:index', request=request, format=format),
            'swagger': reverse('schema-swagger-ui', request=request, format=format),
        }
    })