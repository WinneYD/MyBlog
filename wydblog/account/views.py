from django.shortcuts import render,HttpResponse
from .forms import RegistrationForm,UserProfileForm

def register(request):
    if request.method == 'POST':
        user_form=RegistrationForm(request.POST)
        #userprofile_form=UserProfileForm(request.POST)
        if user_form.is_valid(): #*userprofile_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            #new_profile=userprofile_form.save(commit=False)
            #new_profile.user=new_user
           # new_profile.save()
            return HttpResponse('successful')
        else:
            return HttpResponse('sorry')
    else:
        user_form=RegistrationForm()
        #userprofile_form=UserProfileForm()
        return render(request,'account/register.html',{'form':user_form})




# Create your views here.
