# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column(u'currency_currency', 'symbol',
            self.gf('django.db.models.fields.CharField')(max_length=30, default='', blank=True))
        # Adding field 'Currency.priority'
        db.add_column(u'currency_currency', 'priority',
            self.gf('django.db.models.fields.IntegerField')(default=3),
            keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Currency.priority'
        db.delete_column(u'currency_currency', 'priority')

        db.alter_column(u'currency_currency', 'symbol',
                              self.gf('django.db.models.fields.CharField')(max_length=30, default='&#36;'))
    models = {
        u'currency.currency': {
            'Meta': {'object_name': 'Currency'},
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['currency']