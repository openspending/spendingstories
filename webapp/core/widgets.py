#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 07-Aug-2013
# Last mod : 07-Aug-2013
# -----------------------------------------------------------------------------
from django import forms

class SelectAutoComplete(forms.widgets.Select):

    class Media:
        css = {
            'all': ("css/ui-lightness/jquery-ui-1.10.3.custom.min.css",)
        }
        js = ("js/jquery-1.9.1.js", "js/jquery-ui-1.10.3.custom.min.js", "js/admin-story-script.js")

    def __init__(self, attrs=None, choices=()):
        # print "__init__", attrs, choices
        super(SelectAutoComplete, self).__init__(attrs, choices=choices)

    def render(self, name, value, attrs=None, choices=()):
        # if value is None: value = ''
        # final_attrs = self.build_attrs(attrs, name=name)
        # output = [format_html('<select{0}>', flatatt(final_attrs))]
        # options = self.render_options(choices, [value])
        # if options:
        #     output.append(options)
        # output.append('</select>')
        # return mark_safe('\n'.join(output))
        # print "render",super(SelectAutoComplete, self).render(name, value, attrs, choices)
        if attrs is None:
            attrs = {}
        attrs['class'] = "combobox"
        return super(SelectAutoComplete, self).render(name, value, attrs, choices)

    def render_option(self, selected_choices, option_value, option_label):
        # option_value = force_text(option_value)
        # if option_value in selected_choices:
        #     selected_html = mark_safe(' selected="selected"')
        #     if not self.allow_multiple_selected:
        #         # Only allow for a single selection.
        #         selected_choices.remove(option_value)
        # else:
        #     selected_html = ''
        # return format_html('<option value="{0}"{1}>{2}</option>',
        #                    option_value,
        #                    selected_html,
        #                    force_text(option_label))
        # print "render_option", selected_choices, option_value, option_label
        return super(SelectAutoComplete, self).render_option(selected_choices, option_value, option_label)

    def render_options(self, choices, selected_choices):
        # # Normalize to strings.
        # selected_choices = set(force_text(v) for v in selected_choices)
        # output = []
        # for option_value, option_label in chain(self.choices, choices):
        #     if isinstance(option_label, (list, tuple)):
        #         output.append(format_html('<optgroup label="{0}">', force_text(option_value)))
        #         for option in option_label:
        #             output.append(self.render_option(selected_choices, *option))
        #         output.append('</optgroup>')
        #     else:
        #         output.append(self.render_option(selected_choices, option_value, option_label))
        # return '\n'.join(output)
        # print "render_options", choices, selected_choices
        return super(SelectAutoComplete, self).render_options(choices, selected_choices)

# EOF
