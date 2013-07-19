from rest_framework import serializers
import models 

class SpendingSerializer():
    class Meta: 
        model = models.Spending
        fields = ['value', 'created', 'modified', 'source', 'currency']

