from rest_framework              import status
from rest_framework              import viewsets
from rest_framework.decorators   import link
from rest_framework.response     import Response
from spendingstories.core.models import Spending, SpendingSerializer

class SpendingViewSet(viewsets.ModelViewSet):
    queryset = Spending.objects 
    serializer_class = SpendingSerializer

    def list(self, request):
        return Response(self.queryset.all()) 

    @link()
    def sort_by_popularity(self):
        return Response(self.queryset.sort_by_popularity())

    @link()
    def between(self, request):
        print request.DATA
        return Response('received DATA: ', DATA)

