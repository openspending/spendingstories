from rest_framework          import viewsets
from rest_framework.response import Response


class ChoicesViewSet(viewsets.ViewSet):
    class Meta: 
        #  the choices as queryset 
        choices = None

    def list(self,request):
        return Response(self.create_list(request))

    def create_list(self, request):
        return [ self.create_element(c) for c in self.__class__.Meta.choices]

    def create_element(self, obj):
        raise Exception('IMPLEMENT ME !')