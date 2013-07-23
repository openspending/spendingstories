from rest_framework           import serializers
from django.utils.translation import ugettext as _
from model_utils.managers     import PassThroughManager
from economics                import Inflation, CPI
from django.db                import models
import datetime 


CPI_DATA_URL = 'http://localhost:8000/static/data/cpi.csv'

YEAR_CHOICES = []
for r in range(1999, (datetime.datetime.now().year)):
    YEAR_CHOICES.append((r,r))



class SpendingQuerySet(models.query.QuerySet):

    def validated(self): 
        return self.filter(is_validated=true)

    def sortByValue(self):
        return self.order_by('-value')

    def sortByPopularity(self):
        return self.order_by('-popularity')

    def between(lower_boundary, upper_boundary):
        return self.fitler(value__gte=lower_boundary, value__lte=upper_boundary)


class InflationWrapper(object):
    instance = None
    # Simple Singleton 
    def __new__(klass, *args, **kargs):
        if instance is None:
            instance = object.__new__(klass, *args, **args)
            instance.cpi = CPI(source=CPI_DATA_URL)
            instance.inflation = Inflation(source=CPI_DATA_URL)
        return instance

    def inflate(self, reference=None, country=None):
        # the target date, i.e the date for which we gonna compute the inflation level 
        # is found by getting the closest date to today having CPI data. 
        target_date = self.cpi.closest(country=country, date=datetime.date.today(), limit=datetime.timedelta(366*3)).date
        try: 
            closest_ref_date = self.cpi.closest(country=country, date=reference).date # get the closest date for reference date
        except:
            closest_ref_date = target
        # We inflate the given amount to the targeted year (the closent year available)
        inflated = self.inflation.inflate(target=target_date, reference=closest_ref_date, country=country) 
        return (inflated, target_date)



class Spending(models.Model):
    '''
    The model representing a spending
    '''
    value                    = models.DecimalField(_('The spending value'), decimal_places=2, max_digits=15) # The spending amount 
    value_current            = models.DecimalField(decimal_places=2, max_digits=15) # The spending amount inflated
    value_usd_current        = models.DecimalField(decimal_places=2, max_digits=15) # The spending amount in USD inflated
    inflation_reference_year = models.IntegerField()
    country                  = models.CharField(max_length=3) # ISO code of the country 
    source                   = models.URLField()
    name                     = models.CharField(max_length=140)
    currency                 = models.ForeignKey('Currency')
    continuous               = models.BooleanField(_('Is a countinuous spending'), default=False) 

    year     = models.IntegerField(_('The spending year'), choices=YEAR_CHOICES)
    objects  = PassThroughManager.for_queryset_class(SpendingQuerySet)()
    created  = datetime.datetime.now()
    modified = datetime.datetime.now()

    def save(self):
        inflator =  InflationWrapper()
        self.value_current = inflator.inflate(reference=self.year, 
            country=self.country)
        self.value_usd_current = self.currency.get_rate() * self.value_current
        self.modified = datetime.datetime.now()
        super(Spending, self).save()


class SpendingSerializer(serializers.Serializer):
    class Meta: 
        model = Spending
        fields = ['value', 'value_usd_current', 'value_current','created', 'modified', 'source', 'currency']



class Currency(models.Model):
    # The ISO code for currencies, possible values are based on what 
    iso_code = models.CharField(max_length=3)
    # The exchange rate took from OpenExchangeRate
    rate = models.FloatField()



