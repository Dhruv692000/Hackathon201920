from .forms import *
from .models import *
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import random
from django.http import HttpResponse,HttpResponseNotFound
from .resources import *
from django.contrib.auth.decorators import login_required


notes = Notification.objects.all()


def leave(request):
	applications = Leave.objects.all()
	return render(request,'organization/leave.html',{'applications':applications})
def organization_index(request):
	notes = Notification.objects.all()
	return render(request,'organization/organization_index.html',{'notes':notes})
def signup(request):
	print('signup called');
	if request.method=="POST":
		
		fname=request.POST["first_name"]
		lname=request.POST["last_name"]
		email=request.POST["email"]
		mobile=request.POST["mobile"]
		password=request.POST["password"]
		confirm_password=request.POST["confirm_password"]

		try:
			user=User.objects.get(email=email)
			if user:
				error="Email Already Registered"
				form=UserForm()
				messages.error(request,error)
				return render(request,'organization/signup.html',{'form':form})
		except:
			User.objects.create(first_name=fname,
								last_name=lname,
								email=email,
								mobile=mobile,
								password=password,
								confirm_password=confirm_password)
			messages.success(request,f'SignUp Successfull')
			rec=[email,]
			subject="OTP For Successfull Registration"
			otp=random.randint(10000,99999)
			message="Your OTP For Registration Is "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			send_mail(subject, message, email_from, rec)
			print("Data Inserted Succesfully")
			return render(request,'organization/validate_otp.html',{'otp':otp,'email':email})

	else:
		form=UserForm()
	return render(request,'organization/signup.html',{'form':form})

def validate_otp(request):
	error=""
	if request.method=="POST":
		g_otp=request.POST["g_otp"]
		otp=request.POST["otp"]
		email=request.POST["email"]
		if g_otp==otp:
			user=User.objects.get(email=email)
			user.status="active"
			user.save()
			return redirect('/login')
			
	else:
		error="Your OTP Is Incorrect"
	return render(request,'organization/resend.html',{'error':error,'email':email})

def resend_otp(request):
	if request.method=="POST":
		email=request.POST['email']
		rec=[email,]
		subject="OTP For Successfull Registration"
		otp=random.randint(1000,9999)
		message="Your OTP For Registration Is "+str(otp)
		email_from = settings.EMAIL_HOST_USER
		send_mail(subject, message, email_from, rec)
		return render(request,'organization/validate_otp.html',{'otp':otp,'email':email})
	return render(request,'organization/login.html')

def login(request):
	if request.method == "POST":
		email = request.POST["email"]
		password = request.POST["password"]

		print(email,password);
		return render(request,'organization/organization_index.html',{'notes':notes})
	else:
		form = LoginForm();
		return render(request,'organization/login.html',{'form':form})


def dashboard(request):
	return render(request,'organization/dashboard.html')

@login_required
def setmerit(request):
	if request.method == 'POST':
		gender       = request.POST['gender']
		ce_merit     = request.POST['ce_merit']
		it_merit     = request.POST['it_merit']
		mech_merit   = request.POST['mech_merit']
		ec_merit     = request.POST['ec_merit']
		ic_merit     = request.POST['ic_merit']
		last_updated = request.POST['last_updated']
		
		merit_list = [ce_merit,
					  it_merit,
					  mech_merit,
					  ec_merit,
					  ic_merit,]
			
		for i in range(len(merit_list)): 
  
		    var = i 
		    for j in range(i+1, len(merit_list)): 
		        if merit_list[var] == merit_list[j]: 
		        	messages.error(request,f'ERROR! Two Departments cannot have same Merit Values!');							    			        	
		        	return redirect('setmerit');					
					
		smerit.objects.create(gender=gender,
							  ce_merit=ce_merit,
							  it_merit=it_merit,
							  mech_merit=mech_merit,
							  ec_merit=ec_merit,
							  ic_merit=ic_merit)

		message = "Merit set successfully!"
		return render(request,'organization/dashboard.html',{'message':message})
		
	else:
		form = Merit();
		return render(request,'organization/setmerit.html',{'form':form})

def admission(request):
	if request.method == 'POST':
		first_name = request.POST["first_name"]
		middle_name = request.POST["middle_name"]
		last_name = request.POST["last_name"]
		er_no = request.POST["er_no"]
		date_of_birth = request.POST["dob"]
		gender = request.POST.get("gender")
		department = request.POST["department"]
		semester = request.POST["semester"]
		email = request.POST["email"]
		mobile = request.POST["mobile"]
		password = request.POST["password"]
		confirm_password = request.POST["confirm_password"]
		address = request.POST["address"]
		city = request.POST["city"]
		state = request.POST["state"]
		zipcode = request.POST["zipcode"]
		guardian_name = request.POST["guardian_name"]
		guardian_mobile = request.POST["guardian_mobile"]
		emergency_no = request.POST["emergency_no"]
		profile = request.POST["profile"]
		
		try:
			adm = Admission.objects.get(email=email)
			if adm:
				error = 'Student with same email already registered'
				form = Student()
				return render(request,'organization/admission.html',{'form':form,'error':error})
		except:
			Admission.objects.create(first_name=first_name,
									 middle_name=middle_name,
									 last_name=last_name,
									 er_no=er_no,
									 date_of_birth=date_of_birth,
									 gender=gender,
									 department=department,
									 semester=semester,
									 email=email,
									 mobile=mobile,
									 password=password,
									 confirm_password=confirm_password,
									 address=address,
									 city=city,
									 state=state,
									 zipcode=zipcode,
									 guardian_name=guardian_name,
									 guardian_mobile=guardian_mobile,
									 emergency_no=emergency_no,
									 profile=profile)
			return redirect('/')

	else:
		form=Student()
		return render(request,'organization/admission.html',{'form':form})

@login_required
def notification(request):
	if request.method == 'POST':
		subject = request.POST['subject']
		message = request.POST['message']

		try:
			sub = Notification.objects.get(subject=subject)
			if sub:
				error = f"Notification for {sub} already exist"
				form = Notify()
				return render(request,'organization/notification.html',{'form':form,'error':error})

		except:
			Notification.objects.create(subject=subject,message=message)
			notes = Notification.objects.all()
			return render(request,'organization/organization_index.html',{'notes':notes})

	else:
		form = Notify()
		return render(request,'organization/notification.html',{'form':form})

def login(request):
	if request.method=="POST":
		email=request.POST["email"]
		password=request.POST["password"]
		
		try:
			user=User.objects.get(email=email,password=password)

			if user.status=="active":
				request.session['fname']=user.first_name
				request.session['userpk']=user.pk
				return redirect('organization_index')
			else:
				email=email
				rec=[email,]
				subject="OTP For Successfull Registration"
				otp=random.randint(1000,9999)
				message="Your OTP For Registration Is "+str(otp)
				email_from = settings.EMAIL_HOST_USER
				send_mail(subject, message, email_from, rec)
				return render(request,'organization/validate_otp.html',{'otp':otp,'email':email})
		except:
			error="Email Or Password Is Incorrect"
			return render(request,'organization/login.html',{'error':error})
			
	else:
		form=LoginForm()
	return render(request,'organization/login.html',{'form':form})

def logout(request):
	try:
		del request.session['fname']
		form=LoginForm()
		return redirect('organization_index')
	except:
		pass

def intermediate(request,pk):	
	name=get_object_or_404(Grievance,pk=pk)
	context=Grievance.objects.filter(name=name)
	return render(request,'organization/intermediate.html',{'context':context})

def grievance(request,pk):
	if request.method == "POST" :
		name = request.POST["name"]
		er_no = request.POST["erno"]
		email = request.POST["semail"]
		department = request.POST["department"]
		g_type = request.POST["type"]
		others = request.POST["others"]
		info = request.POST["info"]

		print(email,settings.EMAIL_HOST_USER)
		rec = [settings.EMAIL_HOST_USER,]
		subject = f"Complaint received from {name} of department {department} and enrollment no. {er_no} with email {email} regarding {g_type}"
		message = f"{info}"
		email_from = email
		send_mail(subject, message, email_from, rec)

		name=get_object_or_404(User,pk=pk)
		Grievance.objects.create(name=name)
		context = {'name':name,
			 	   'er_no':er_no,
			 	   'email':email,
			 	   'department':department,
			 	   'g_type':g_type,
			 	   'others':others,
			 	   'info':info}

		print(email_from,settings.EMAIL_HOST_USER)
		return render(request,'organization/intermediate.html',{'context':context})
	else:
		form = Complaint()
		return render(request,'organization/grievance.html',{'form':form})

def inventory(request):
	return render(request,'organization/inventory.html')

def display_laptops(request):
	items = Laptop.objects.all()
	num = Laptop.objects.count()
	context = {
		'items':items,
		'header':'Laptops',
		'num':num
	}
	return render(request,'organization/inventory.html',context)

def display_desktops(request):
	items = Desktop.objects.all()
	num = Desktop.objects.count()
	context = {
		'items':items,
		'header':'Desktops',
		'num':num
	}
	return render(request,'organization/inventory.html',context)

def display_cupboards(request):
	items = Cupboard.objects.all()
	num = Cupboard.objects.count()
	context = {
		'items':items,
		'header':'Cupboards',
		'num':num
	}
	return render(request,'organization/inventory.html',context)

def display_tables(request):
	items = Table.objects.all()
	num = Table.objects.count()
	context = {
		'items':items,
		'header':'Tables',
		'num':num
	}
	print(num)
	return render(request,'organization/inventory.html',context)

def display_chairs(request):
	items = Chair.objects.all()
	num = Chair.objects.count()
	context = {
		'items':items,
		'header':'Chairs',
		'num':num
	}
	return render(request,'organization/inventory.html',context)

def display_beds(request):
	items = Bed.objects.all()
	num = Bed.objects.count()
	context = {
		'items':items,
		'header':'Beds',
		'num':num
	}
	return render(request,'organization/inventory.html',context)

def add_laptop(request):
	if request.method == "POST":
		form = LaptopForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('display_laptops')
	else:
		form = LaptopForm()
		return render(request,'organization/add_new.html',{'form':form})

def add_desktop(request):
	if request.method == "POST":
		form = DesktopForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('display_desktops')
	else:
		form = DesktopForm()
		return render(request,'organization/add_new.html',{'form':form})

def add_cupboard(request):
	if request.method == "POST":
		form = CupboardForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('display_cupboards')
	else:
		form = CupboardForm()
		return render(request,'organization/add_new.html',{'form':form})

def add_table(request):
	if request.method == "POST":
		form = TableForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('display_tables')
	else:
		form = TableForm()
		return render(request,'organization/add_new.html',{'form':form})

def add_chair(request):
	if request.method == "POST":
		form = ChairForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('display_chairs')
	else:
		form = ChairForm()
		return render(request,'organization/add_new.html',{'form':form})

def add_bed(request):
	if request.method == "POST":
		form = BedForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('display_beds')
	else:
		form = BedForm()
		return render(request,'organization/add_new.html',{'form':form})

def edit_laptop(request, pk):
	item = get_object_or_404(Laptop, pk=pk)

	if request.method == "POST":
		form = LaptopForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('organization_index')

	else:
		form = LaptopForm(instance = item)
		return render(request,'organization/edit_item.html',{'form':form})

def edit_desktop(request, pk):
	item = get_object_or_404(Desktop, pk=pk)

	if request.method == "POST":
		form = DesktopForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('organization_index')

	else:
		form = DesktopForm(instance = item)
		return render(request,'organization/edit_item.html',{'form':form})

def edit_cupboard(request, pk):
	item = get_object_or_404(Cupboard, pk=pk)

	if request.method == "POST":
		form = DesktopForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('organization_index')

	else:
		form = DesktopForm(instance = item)
		return render(request,'organization/edit_item.html',{'form':form})

def edit_chair(request, pk):
	item = get_object_or_404(Chair, pk=pk)

	if request.method == "POST":
		form = ChairForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('organization_index')

	else:
		form = ChairForm(instance = item)
		return render(request,'organization/edit_item.html',{'form':form})

def edit_table(request, pk):
	item = get_object_or_404(Table, pk=pk)

	if request.method == "POST":
		form = TableForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('organization_index')

	else:
		form = TableForm(instance = item)
		return render(request,'organization/edit_item.html',{'form':form})

def edit_bed(request, pk):
	item = get_object_or_404(Bed, pk=pk)

	if request.method == "POST":
		form = BedForm(request.POST,instance=item)
		if form.is_valid():
			form.save()
			return redirect('organization_index')

	else:
		form = BedForm(instance = item)
		return render(request,'organization/edit_item.html',{'form':form})

def delete_laptop(request, pk):
	Laptop.objects.filter(id=pk).delete()

	items = Laptop.objects.all()
	num = Laptop.objects.count()
	header = 'Laptops'
	return render(request,'organization/inventory.html',{'items':items,'num':num,'header':header})

def delete_desktop(request, pk):
	Desktop.objects.filter(id=pk).delete()

	items = Desktop.objects.all()
	num = Desktop.objects.count()
	header = 'Desktops'
	return render(request,'organization/inventory.html',{'items':items,'num':num,'header':header})

def delete_cupboard(request, pk):
	Cupboard.objects.filter(id=pk).delete()

	items = Cupboard.objects.all()
	num = Cupboard.objects.count()
	header = 'Cupboards'
	return render(request,'organization/inventory.html',{'items':items,'num':num,'header':header})

def delete_table(request, pk):
	Table.objects.filter(id=pk).delete()
	items = Table.objects.all()
	num = Table.objects.count()
	header = 'Tables'
	return render(request,'organization/inventory.html',{'items':items,'num':num,'header':header})

def delete_chair(request, pk):
	Chair.objects.filter(id=pk).delete()

	items = Chair.objects.all()
	num = Chair.objects.count()
	header = 'Chairs'
	return render(request,'organization/inventory.html',{'items':items,'num':num,'header':header})

def delete_bed(request, pk):
	Bed.objects.filter(id=pk).delete()

	items = Bed.objects.all()
	num = Bed.objects.count()
	header = 'Beds'
	return render(request,'organization/inventory.html',{'items':items,'num':num,'header':header})

def export_as_csv(request):
	laptop_resource = LaptopResource()
	dataset = laptop_resource.export()
	return HttpResponse(dataset.csv, content_type='text/csv')	

def export_as_excel(request):
	laptop_resource = LaptopResource()
	dataset = laptop_resource.export()
	return HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')

def export_as_json(request):
	laptop_resource = LaptopResource()
	dataset = laptop_resource.export()
	return HttpResponse(dataset.json, content_type='application/json')

def circulars(request):
	return render(request,'organization/circulars.html')

def leave_form(request):
	if request.method == "POST":
		form = LeaveForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('leave')
	else:
		form = LeaveForm()
		return render(request,'organization/leave_form.html',{'form':form})


def decline_request(request, pk):
	Leave.objects.filter(id=pk).delete()
	num = Leave.objects.count()
	applications = Leave.objects.all()
	return render(request,'organization/leave.html',{'applications':applications,'num':num})
    
    




    




