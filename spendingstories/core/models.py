from rest_framework           import serializers
from django.utils.translation import ugettext as _
from model_utils.managers     import PassThroughManager
from economics                import Inflation, CPI
from django.db                import models
import datetime
import fields


CPI_DATA_URL = 'http://localhost:8000/static/data/cpi.csv'

YEAR_CHOICES = []
for r in range(1999, (datetime.datetime.now().year)):
    YEAR_CHOICES.append((r,r))



class StoriesQuerySet(models.query.QuerySet):
    relevance_query = "SELECT * FROM core_stories ORDER BY amount_usd_current / %s "

    def validated(self): 
        return self.filter(is_validated=true)





class InflationWrapper(object):
    # Simple Singleton wrapper 
    instance = None
    def __new__(klass, *args, **kargs):
        if instance is None:
            instance = object.__new__(klass, *args, **args)
            instance.cpi = CPI(source=CPI_DATA_URL)
            instance.inflation = Inflation(source=CPI_DATA_URL)
        return instance

    def closest_ajustment_year(self, country=None):
        return self.cpi.closest(
            country=country, 
            date=datetime.date.today(), 
            limit=datetime.timedelta(366*3)).date


    def inflate(self, reference=None, country=None, amount=None):
        '''
        Inflate the given `amount` to the last available inflation year (see 
        closest_ajustment_year)
        '''
        # the target date, i.e the date for which we gonna compute the inflation level 
        # is found by getting the closest date to today having CPI data. 
        target_date = self.closest_ajustment_year(country)
        try: 
            closest_ref_date = self.cpi.closest(country=country, date=reference).date # get the closest date for reference date
        except:
            closest_ref_date = target
        # We inflate the given amount to the targeted year (the closent year available)
        return self.inflation.inflate(target=target_date, reference=closest_ref_date, country=country) 




class Stories(models.Model):
    '''
    The model representing a spending
    '''
    created  = datetime.datetime.now()
    modified = datetime.datetime.now()

    value      = models.DecimalField(_('The spending value'), decimal_places=2, max_digits=15) # The spending amount 
    title      = models.CharField(_('Story title'), max_length=140)
    country    = fields.CountryField() # ISO code of the country 
    source     = models.URLField(_('Story\'s source URL'), max_length=140)
    currency   = models.ForeignKey('Currency')
    continuous = models.BooleanField(_('Is a countinuous spending'), default=False)
    sticky     = models.BooleanField(_('Is a top story'),    default=False)
    year       = models.IntegerField(_('The spending year'), choices=YEAR_CHOICES)
    objects    = PassThroughManager.for_queryset_class(StoriesQuerySet)()
    
    def _inflate_value(self):
        '''
        Used to ajust the value of the story value
        ''' 
        return InflationWrapper().inflate(country=self.country, reference=self.year)
    
    def _convert_to_usd(self):
        '''
        Return the current value converted into USD 
        ''' 
        exchange_rate = self.currency.get_exchange_rate()
        return self.value_current * exchange_rate

    def _get_ajustement_year(self):
        '''
        Return the closest available year for inflation ajustement, ideally it 
        should return the current year - 1 
        ''' 
        return InflationWrapper.closest_ajustment_year(country=self.country)

    # all calculated fields
    value_current            = property(_inflate_value)
    value_current_usd        = property(_convert_to_usd)
    inflation_ajustment_year = property(_get_ajustement_year)

class StoriesSerializer(serializers.Serializer):
    class Meta: 
        model = Stories
        fields = ['value', 'value_usd_current', 'value_current','created', 'modified', 'source', 'currency']






class Currencies(models.Model):
    # The ISO code for currencies, possible values are based on what 
    iso_code = models.CharField(max_length=3)
    # The exchange rate took from OpenExchangeRate
    rate     = models.FloatField()

    def get_exchange_rate(self):
        return self.rate



