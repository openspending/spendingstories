from rest_framework   import filters
from django_filters   import filterset
from django           import forms
from django.db.models import Q
from django.db.models import query
from django.utils     import six
from webapp.core      import models
import collections 
import types 

class OrFilterSet(filterset.FilterSet):
    strict = True
    """
    Copied from django_filters.BaseFilter & customized
    """
    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            valid = self.is_bound and self.form.is_valid()

        if self.strict and self.is_bound and not valid:
            self._qs = self.queryset.none()
            return self._qs

        # start with all the results and filter from there
        qs = self.queryset.all()
        # the complex query we will built
        qg = None 
        for name, filter_ in six.iteritems(self.filters):
            value = None
            if valid:
                value = self.form.cleaned_data[name]
            else:
                raw_value = self.form[name].value()
                try:
                    value = self.form.fields[name].clean(raw_value)
                except forms.ValidationError:
                    # for invalid values either:
                    # strictly "apply" filter yielding no results and get outta here
                    if self.strict:
                        self._qs = self.queryset.none()
                        return self._qs
                    else:  # or ignore this filter altogether
                        pass

            if not self.is_value_empty(value):  # valid & clean data
                if not isinstance(value, (str, unicode)) and (isinstance(value, (collections.Iterable,query.QuerySet))):
                    for sub_value in value:
                        qg = self.build_complex_query(name,sub_value,qg)
                else:
                    qg = self.build_complex_query(name,value,qg)

        if qg is not None:
            qs = qs.filter(qg).distinct()

        if self._meta.order_by:
            order_field = self.form.fields[self.order_by_field]
            data = self.form[self.order_by_field].data
            ordered_value = None
            try:
                ordered_value = order_field.clean(data)
            except forms.ValidationError:
                pass

            if ordered_value in EMPTY_VALUES and self.strict:
                ordered_value = self.form.fields[self.order_by_field].choices[0][0]

            if ordered_value:
                qs = qs.order_by(*self.get_order_by(ordered_value))

        self._qs = qs

        return self._qs

    def build_complex_query(self, name, value, querygroup):
        """
        Because we are dealing with a complex query we need to be able to build
        a complex query when navigating on the filter fields
        """ 
        kwargs = {
            name: value
        }
        query = Q(**kwargs)
        if querygroup is None:
            querygroup = query
        else:
            querygroup |= query
        return querygroup

    def is_value_empty(self, value):
        if isinstance(value, (str, unicode)):
            return value is None or len(value) is 0
        else:
            return value is None or type(value) is types.NoneType

class OrFilterBackend(filters.DjangoFilterBackend):
    default_filter_set = OrFilterSet

