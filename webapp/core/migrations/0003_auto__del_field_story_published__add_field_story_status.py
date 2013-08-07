# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Story.published'
        db.delete_column(u'core_story', 'published')

        # Adding field 'Story.status'
        db.add_column(u'core_story', 'status',
                      self.gf('django.db.models.fields.CharField')(default='pending', max_length=9),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Story.published'
        db.add_column(u'core_story', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Story.status'
        db.delete_column(u'core_story', 'status')


    models = {
        u'core.story': {
            'Meta': {'object_name': 'Story'},
            'continuous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('webapp.core.fields.CountryField', [], {'max_length': '3'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['currency.Currency']"}),
            'current_value': ('django.db.models.fields.FloatField', [], {}),
            'current_value_usd': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inflation_last_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '9'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'themes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Theme']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        u'core.theme': {
            'Meta': {'object_name': 'Theme'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'currency.currency': {
            'Meta': {'object_name': 'Currency'},
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'rate': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['core']