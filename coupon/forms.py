from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApllyForm(forms.Form):
	code = forms.CharField()