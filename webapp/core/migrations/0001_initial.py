# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("currency", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'Theme'
        db.create_table(u'core_theme', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Theme'])

        # Adding model 'Story'
        db.create_table(u'core_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('webapp.core.fields.CountryField')(max_length=3)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=140, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['currency.Currency'])),
            ('continuous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('current_value', self.gf('django.db.models.fields.FloatField')()),
            ('current_value_usd', self.gf('django.db.models.fields.FloatField')()),
            ('inflation_last_year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
        ))
        db.send_create_signal(u'core', ['Story'])

        # Adding M2M table for field themes on 'Story'
        m2m_table_name = db.shorten_name(u'core_story_themes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm[u'core.story'], null=False)),
            ('theme', models.ForeignKey(orm[u'core.theme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['story_id', 'theme_id'])


    def backwards(self, orm):
        # Deleting model 'Theme'
        db.delete_table(u'core_theme')

        # Deleting model 'Story'
        db.delete_table(u'core_story')

        # Removing M2M table for field themes on 'Story'
        db.delete_table(db.shorten_name(u'core_story_themes'))


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
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'themes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Theme']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        u'core.theme': {
            'Meta': {'object_name': 'Theme'},
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