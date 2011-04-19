from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.mk.mk_municipalities import MUNICIPALITY_CHOICES


class MKMunicipalityField(CharField):

    description = _("A Macedonian municipality (5 character HASC)")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = MUNICIPALITY_CHOICES
        kwargs['max_length'] = 5 
        super(MKMunicipalityField, self).__init__(*args, **kwargs)

class UMCNField(CharField):

    description = _("Unique master citizen number (13 digits)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13
        super(UMCNField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from django.contrib.localflavor.mk.forms import UMCNField as FormField
        defaults = {'form_class' : FormField}
        defaults.update(kwargs)
        return super(UMCNField, self).formfield(**defaults)

class MKIdentityCardNumberField(CharField):

    description = _("Macedonian identity card number")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        super(MKIdentityCardNumberField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from django.contrib.localflavor.mk.forms import MKIdentityCardNumberField as FormField
        defaults = {'form_class' : FormField}
        defaults.update(kwargs)
        return super(MKIdentityCardNumberField, self).formfield(**defaults)
