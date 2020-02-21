from django import forms
from .models import *

class UserForm(forms.ModelForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','mobile','password','confirm_password')

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','password']

class Merit(forms.ModelForm):
	class Meta:
		model = smerit
		fields = ['gender',
				  'ce_merit',
				  'it_merit',
				  'mech_merit',
				  'ec_merit',
				  'ic_merit',
				  'last_updated',
				 ]

class Notify(forms.ModelForm):
	class Meta:
		model = Notification
		fields = ['subject','message']

class Complaint(forms.ModelForm):
	class Meta:
		model = Grievance
		fields = ['name',
				  'er_no',
				  'email',
				  'department',
				  'g_type',
				  'others',
				  'info',
		]

class LaptopForm(forms.ModelForm):
	class Meta:
		model = Laptop
		fields = ['i_id',
				  'model',
				  'room_no',
				  'hostel',
				  'allocation_date',

		]

class DesktopForm(forms.ModelForm):
	class Meta:
		model = Desktop
		fields = ['i_id',
				  'model',
				  'room_no',
				  'hostel',
				  'allocation_date',

		]

class CupboardForm(forms.ModelForm):
	class Meta:
		model = Cupboard
		fields = ['i_id',
				  'model',
				  'room_no',
				  'hostel',
				  'allocation_date',

		]

class TableForm(forms.ModelForm):
	class Meta:
		model = Table
		fields = ['i_id',
				  'model',
				  'room_no',
				  'hostel',
				  'allocation_date',

		]

class ChairForm(forms.ModelForm):
	class Meta:
		model = Chair
		fields = ['i_id',
				  'model',
				  'room_no',
				  'hostel',
				  'allocation_date',

		]

class BedForm(forms.ModelForm):
	class Meta:
		model = Bed
		fields = ['i_id',
				  'model',
				  'room_no',
				  'hostel',
				  'allocation_date',

		]
