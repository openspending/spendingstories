from rest_framework          import viewsets
from rest_framework.response import Response


class ChoicesViewSet(viewsets.ViewSet):
    class Meta: 
        #  the choices as queryset 
        choices = None
        """
        Custom way of filtering results, must be a dictionnary like following:
            {
                <url param>:  <object attr>
            }
        """ 
        filters = None

    def list(self,request):
        return Response(self.create_list(request))

    def create_list(self, request):
        _list = [ self.create_element(c) for c in self.__class__.Meta.choices]
        if hasattr(self.__class__.Meta, 'filters'):
            filters = self.__class__.Meta.filters 
            if filters is not None:
                for url_param in filters.keys():
                    url_param_val = request.QUERY_PARAMS.get(url_param)
                    if url_param_val is not None: 
                        obj_attr = filters[url_param]
                        _list = filter(lambda x: x[obj_attr] == url_param_val, _list)
        
        return _list

    def create_element(self, obj):
        raise Exception('IMPLEMENT ME !')