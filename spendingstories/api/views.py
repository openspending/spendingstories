from rest_framework              import status, generics 
from rest_framework              import serializers
from rest_framework.views        import APIView
from rest_framework.decorators   import link
from rest_framework.response     import Response
from spendingstories.core.models import Story
import django_filters


class StoryFilter(django_filters.FilterSet):
    class Meta:
        filter_fields = ('top', 'tag')

class StorySerializer(serializers.Serializer):
    title             = serializers.CharField(max_length=140)
    source            = serializers.URLField()
    value             = serializers.IntegerField()
    # Read Only fields:
    id                = serializers.IntegerField(read_only=True)
    value_current     = serializers.IntegerField(read_only=True)
    value_current_usd = serializers.IntegerField(read_only=True)
    sticky            = serializers.BooleanField(read_only=True)
    created           = serializers.DateTimeField(read_only=True)
    modified          = serializers.DateTimeField(read_only=True)
    class Meta:
        paginated_by = 10


class StoryListAPIView(generics.ListAPIView):
    '''
    The base API for stories, retrieve all stories paginated
    '''
    queryset         = Story.objects.published()
    filter_class     = StoryFilter
    serializer_class = StorySerializer


class ProximityStoryListAPIView(generics.ListAPIView):
    '''
    Get the stories filtered by proximity
    ''' 
    queryset         = Story.objects
    serializer_class = StorySerializer

    def get_queryset(self):
        query_params  = self.request.QUERY_PARAMS
        closest_first = True
        currency_code = 'USD'
        amount        = query_params['amount']

        if 'closest_first' in query_params:
            closest_first = query_params['closest_first']

        if 'currency' in query_params:
            currency_code = query_params['currency']

        if currency_code != 'USD':
            currency = Currency.objects.find(currency=currency_code)
            amount   = currency.rate * amount

        return self.queryset.proximty(amount=amount, closest_first=closest_first)

