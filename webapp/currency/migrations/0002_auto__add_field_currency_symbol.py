# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Currency.symbol'
        db.add_column(u'currency_currency', 'symbol',
                      self.gf('django.db.models.fields.CharField')(default='&#36;', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Currency.symbol'
        db.delete_column(u'currency_currency', 'symbol')


    models = {
        u'currency.currency': {
            'Meta': {'object_name': 'Currency'},
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['currency']