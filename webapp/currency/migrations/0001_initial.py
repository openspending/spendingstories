# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'currency_currency', (
            ('iso_code', self.gf('django.db.models.fields.CharField')(max_length=3, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('rate', self.gf('django.db.models.fields.FloatField')()),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'currency', ['Currency'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table(u'currency_currency')


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