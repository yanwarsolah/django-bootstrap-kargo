from django import forms
from django.utils.translation import ugettext_lazy as _
from orders.models import ODOrder
from .models import Vehicle


class ODOrderForm(forms.ModelForm):
    """
    Form to manage Order data-entry
    """
    name = forms.CharField(label=_('Nama Produk'))

    class Meta:
        model = ODOrder
        fields = ('name', 'phone', 'price')


class VehicleForm(forms.ModelForm):
	"""
	Form to manage Vehicle data-entry
	"""
	class Meta:
		model = Vehicle
		fields = ['number', 'name', 'driver', 'capacity']
		exclude = ['photo']

		widgets = {
			'number': forms.TextInput(attrs={'class': 'form-control'}),
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'driver': forms.TextInput(attrs={'class': 'form-control'}),
			'capacity': forms.NumberInput(attrs={'class': 'form-control'})
		}

	def clean_number(self):
		number = self.cleaned_data['number']
		if not number.isalnum():
			raise forms.ValidationError(_('Field number tidak boleh ada spasi'))
		return number


class VehicleFormDelete(forms.ModelForm):
	"""
	Form delete vehicle
	"""
	class Meta:
		model = Vehicle
		fields = ['number']
		exclude = ['id', 'name', 'driver', 'capacity', 'photo']

		widgets = {
			'number': forms.HiddenInput(),
		}


class VehicleFormChangePhoto(forms.ModelForm):
	"""
	Form change photo vehicle
	"""
	class Meta:
		model = Vehicle
		fields = ['number', 'photo']
		exclude = ['id', 'name', 'driver', 'capacity']

		widgets = {
			'number': forms.HiddenInput(),
			'photo': forms.FileInput(),
		}