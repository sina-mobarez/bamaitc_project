from django.conf import settings
from django.contrib.auth import login, views
from django.urls import reverse_lazy
import pyotp
from .forms import ContactForm, CustomUserCreationForm, LoginForm, VerifyForm
from .models import ApplicationDesined, DesinedSite, Profile, Wallet
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .utils import send_sms
from .backends import UserModel, UserNotVerified
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.base import View, TemplateView
from django.views import generic
from django.core.mail import send_mail, BadHeaderError









class LoginView(views.LoginView):


    form_class = LoginForm
    template_name = 'registeration/login.html'
    redirect_authenticated_user = True

    
    def get(self, request, *args, **kwargs):
        
        if 'phone' in self.request.session.keys():
            del self.request.session['phone']
        return super().get(self, request, *args, **kwargs)
    

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        try :
            login(self.request, form.get_user())
        except UserNotVerified:
            """ exception will handeled by middleware"""
            pass
        else:
            return HttpResponseRedirect(self.get_success_url())
        


class VerifyMixin:
    
    @property
    def get_user(self):
        try:
            user = UserModel.objects.get(phone=self.request.session['phone'])
            return user
        except UserModel.DoesNotExist:
            return 
        except KeyError:
            return

    @property
    def set_token(self):
        user = self.get_user
        time_otp = pyotp.TOTP(user.key, interval=300)
        time_otp = time_otp.now()
        return time_otp
    


   
        
class VerifyView(VerifyMixin, FormView):
    form_class = VerifyForm
    success_url = reverse_lazy('login-not-auth')
    template_name = 'registeration/verify.html'

    def get(self, request, *args, **kwargs):
        if self.get_user:
            return super().get(self, request, *args, **kwargs)
        else :
            return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        
        otp_code = str(request.POST.get('otp_code'))
        user = self.get_user
        
        if  user.authenticate(otp_code):
            user.is_verified = True
            user.save()
            messages.success(self.request,'شماره مبایل شما تایید شد')
            return super().post(self, request, *args, **kwargs)
        else :
            messages.warning(self.request,'کد تایید اشتباه است ')
            return self.form_invalid(self.form_class)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['phone']=self.request.session['phone']
        return context





class ResendVerifyView(VerifyMixin, View):
    
    def get(self, request, *args, **kwargs):
        if self.get_user:
            user = self.get_user
            phone = user.phone
            token = self.set_token
            
            send_sms(receptor=phone, token=token)
            print('------------otp:', token)
            
        return HttpResponseRedirect(reverse_lazy('verify'))






class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registeration/register.html'
    success_url = reverse_lazy('login-not-auth')
    
    
    
    
    
class NotpermissionOr404(TemplateView):

    template_name = "base/error-404.html"
    
    
class AboutUs(TemplateView):

    template_name = "base/about-us.html"



def invite_code(request):
        code = request.POST['code']
        user = Profile.objects.get(invite_code=code)
        if user:
            wallet = Wallet.objects.get(user=user)
            cash = wallet.cash
            cash += 20000
            wallet.cash = cash
            wallet.save()
            user.use_invite_code = True
            user.save()
            messages.success(request, 'با تشکر از شما کد معهرف با موفقیت ثبت شد')
            
            
    
def Landing(request):
    desined = DesinedSite.objects.all()
    app = ApplicationDesined.objects.all()
    
    
    return render(request, 'base/landing-home.html', {'desined': desined, 'app': app})


    
def contact_form(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'{form.cleaned_data["subject"]} ; Message from {form.cleaned_data["name"]}'
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            recipients = [settings.EMAIL_ADDRESS]
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            messages.success(request, 'نظر شما با موفقیت ارسال شد به زودی به شما پاسخ خواهیم داد ممنون از شما')
            return redirect('landing-home')
    return render(request, 'base/contant-us.html', {'form': form})