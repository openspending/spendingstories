from rest_framework              import status, generics 
from rest_framework              import serializers
from rest_framework.views        import APIView
from rest_framework.decorators   import link, api_view
from rest_framework.response     import Response
from spendingstories.core.models import Story
import django_filters

@api_view(['GET'])
def api_root_view(request):
    return Response({'message': 'Welcome to Spending Stories API !'})

class StoryFilter(django_filters.FilterSet):
    '''
    Enable the filter on the following fields:

    - `top` (Boolean), filter the stories based on their sticky attribute
    - `country` (String), filter stories for a specific country
        > must be the 3 caracters code ([ISO 3166-1 alpha 3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3))
          of the country to filter 
    '''
    class Meta: 
        model = Story
        fields = ['country',]
    tag = django_filters.ModelMultipleChoiceFilter()
    country = django_filters.ChoiceFilter()

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


class StoryDetailsAPIView(generics.RetrieveUpdateAPIView):
    '''
    API endpoint to retrieve a single story
    '''
    queryset         = Story.objects.published()
    serializer_class = StorySerializer

class StoryListAPIView(generics.ListCreateAPIView):
    '''
    The base API for stories, retrieve all stories paginated
    ## Pagination
    Every list you get is paginated, if you want to get results without pagination
    use the `page_size` parameter set to `0`<br/>
    > Example: `GET /api/stories/?page_size=0`

    ## Filters

    - **top**
    - ** **

    '''
    queryset          = Story.objects.published()
    filter_class      = StoryFilter
    serializer_class  = StorySerializer
    paginate_by       = 10
    paginate_by_param = 'page_size'


class StoryByRelevanceListAPIView(generics.ListAPIView):
    '''
    Get the stories sorted by relevance
    ''' 
    paginate_by = 10
    paginate_by_param = 'page_size'

    queryset         = Story.objects
    serializer_class = StorySerializer

    def get_queryset(self):
        query_params  = self.request.QUERY_PARAMS
        currency_code = 'USD'
        if 'amount' in query_params: 
            amount = query_params['amount']
        else:
            raise Exception('Missing parameters: amount must be specified')

        if 'currency' in query_params:
            currency_code = query_params['currency']

        if currency_code != 'USD':
            currency = Currency.objects.find(currency=currency_code)
            amount   = currency.rate * amount

        return self.queryset.relevance(amount=amount)

