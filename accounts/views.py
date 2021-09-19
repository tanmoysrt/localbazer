from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse
from .models import CustomUser,PhoneOtp
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.conf import settings
from accounts.models import CustomUser,OtpDirectory
from buyer.models import BuyerProfile
from seller.models import SellerProfile
#11-august-2002
from referral1.models import referralfirst
#11-august-2002 END
from django.contrib.auth.decorators import login_required
from accounts.decorators import seller_required,buyer_required
from localbazeer.settings import headers,url
import requests
import random

def sendMessage(numbers, content):
    url = f"https://www.fast2sms.com/dev/bulkV2?authorization=j2q8pEbBWH7ZvKrVF6JaTxGkg1PAwfhysUYQSmMo3Xt5u4dLniJfSndABsiDpOGcH2gChWXjbY4rRmIe&route=v3&sender_id=TXTIND&message={content}&language=english&flash=0&numbers={numbers}"
    try:
        res = requests.get(url)
        print(res)
    except:
        print("ERROR : Can't send message")


@csrf_protect
@never_cache
def BuyerRegister(request):
    data={'title':'LocalBazeer | Register'}
    if request.method=='POST':
        name=request.POST.get('name')
        phoneno=request.POST.get('phoneno')
        # email=request.POST.get('email')
        # password=str(request.POST.get('password'))
        # password1=str(request.POST.get('password1'))
        # if password != password1:
        #     data['message']='''<div class="alert alert-danger" role="alert">
        #         Password & Confirmed Password Must Be Same</div>'''
            # return render(request,'accounts/buyerregister.html',data)
        # else:
        if len(CustomUser.objects.filter(phoneno=phoneno))!=0:
            data['message']='''<div class="alert alert-danger" role="alert">
            Phone Number Already Exsists</div>'''
            return render(request,'accounts/buyerregister.html',data) 
        else:
            user = CustomUser.objects.create_user(
                email="test@test.com",
                phoneno=phoneno,
                name=name,
                userflag=False,
                verified=False,
                password = "sdhfjxdtfhdghfdhfh" # It will changhe in next line
                )
            user.set_unusable_password()
            user.save()
            userprofile=BuyerProfile.objects.create(
                user=user
            )
            userprofile.save()
            referprofile = referralfirst.objects.create(
                user=user.buyer,
                freedelivery=True,
            )
            referprofile.save()
            if 'refer' in request.GET and request.GET['refer'].strip():
                referprofile.referrerid=int(request.GET['refer'])
                referprofile.save()
            else:
                pass
            otp=random.randint(11111,99999)
            #payload = "sender_id=IMPSMS&language=english&route=qt&numbers="+str(phoneno)+"&message=31943&variables={#BB#}&variables_values="+str(otp)
            verotp = PhoneOtp.objects.create(
                phoneno=phoneno,
                otp=otp,
                message="OTP is {}".format(str(otp)),
            )
            verotp.save()
            sendMessage(str(phoneno),"OTP is {}".format(str(otp)))
            #response = requests.request("POST", url, data=payload, headers=headers)
            # print(response)
            data['message']='''<div class="alert alert-success" role="alert">
            Account Created Successfully ! Let's Login </div>'''
            if 'next' in request.GET:
                return redirect('/account/verify/{}?next={}'.format(phoneno,request.GET['next']))
            else:
                return redirect('/account/verify/{}'.format(phoneno))
    else:
        if 'q' in request.GET:
            data['phonevalue']=int(request.GET['q'])
        return render(request,'accounts/buyerregister.html',data)

@csrf_protect
@never_cache
def SellerRegister(request):
    data={'title':'LocalBazeer Seller Portal | Register'}
    if request.method=='POST':
        name=request.POST.get('name')
        phoneno=request.POST.get('phoneno')
        email=request.POST.get('email')
        password=str(request.POST.get('password'))
        password1=str(request.POST.get('password1'))
        category=request.POST.get('category')
        if password != password1:
            data['message']='''<div class="alert alert-danger" role="alert">
            Password & Confirmed Password Must Be Same</div>'''
            return render(request,'accounts/sellerregister.html',data)
        else:
            if len(CustomUser.objects.filter(phoneno=phoneno))!=0:
                data['message']='''<div class="alert alert-danger" role="alert">
                Phone Number Already Exsists. Try to <a href='/account/sellerlogin'>Login Here</a></div>'''
                return render(request,'accounts/sellerregister.html',data) 
            else:
                user = CustomUser.objects.create_user(
                    email=email,
                    phoneno=phoneno,
                    name=name,
                    userflag=True,
                    password=password,
                    )
                user.set_password(password)
                user.save()
                userprofile=SellerProfile.objects.create(
                    user=user,
                    shopcategoty=category,
                )
                userprofile.save()
                otp=random.randint(11111,99999)
                #payload = "sender_id=IMPSMS&language=english&route=qt&numbers="+str(phoneno)+"&message=32470&variables={#CC#}|{#AA#}&variables_values="+str(name)+"|"+str(otp)
                verotp = PhoneOtp.objects.create(
                    phoneno=phoneno,
                    otp=otp,
                    message="OTP is {}".format(str(otp)),
                )
                verotp.save()
                sendMessage(str(phoneno),"OTP is {}".format(str(otp)))
                #response = requests.request("POST", url, data=payload, headers=headers)
                # print(response)
                data['message']='''<div class="alert alert-success" role="alert">
                Accoint Created Successfully</div>'''
                return redirect('/account/verify/{}'.format(phoneno))
    else:
        return render(request,'accounts/sellerregister.html',data)

        
@csrf_protect
@never_cache
def BuyerLogin(request):
    data={'title':'LocalBazeer | Login'}
    if 'next' in request.GET:
        data['register_url']="/account/buyerregister/?next="+request.GET['next']
    else:
        data['register_url']="/account/buyerregister"
    if not request.user.is_authenticated:
        if request.method=='POST':
            phoneno=request.POST.get('phoneno')
            # password=request.POST.get('password')
            if len(CustomUser.objects.filter(phoneno=phoneno))!=0 :
                if CustomUser.objects.filter(phoneno=phoneno)[0].userflag==False:
                    otp=random.randint(11111,99999)
                    verotp = PhoneOtp.objects.create(
                        phoneno=phoneno,
                        otp=otp,
                        message="OTP is {}".format(str(otp)),
                    )
                    verotp.save()
                    sendMessage(str(phoneno),"OTP is {}".format(str(otp)))
                    
                    if 'next' in request.GET:
                        return redirect(f'/account/verify/{phoneno}?next='+request.GET['next'])
                    else:
                        return redirect(f'/account/verify/{phoneno}')


                else:
                    data['message']='''<div class="alert alert-warning" role="alert">
                    You have no account associated with Buyer Login !</div>'''
                    return render(request,'accounts/buyerlogin.html',data)
                # user = authenticate(request,phoneno=phoneno, password=password)
                # if user is not None:
                #     if CustomUser.objects.filter(phoneno=phoneno)[0].userflag==False:
                #         if CustomUser.objects.get(phoneno=phoneno).verified==False:
                #             return redirect(f'/account/verify/{phoneno}')
                #         else:
                #             login(request,user)
                #             if 'next' in request.GET:
                #                 return redirect(request.GET['next'])
                #             else:
                #                 return redirect('/')
                #     else:
                #         data['message']='''<div class="alert alert-warning" role="alert">
                #         You have no account associated with Buyer Login !</div>'''
                #         return render(request,'accounts/buyerlogin.html',data)
                # else:
                #     data['message']='''<div class="alert alert-danger" role="alert">
                #     Phone No or Password not matched !</div>'''
                #     return render(request,'accounts/buyerlogin.html',data)
            else:
                if 'next' in request.GET:
                    return redirect('/account/buyerregister/?q={}&next={}'.format(phoneno,request.GET['next']))
                else:
                    return redirect('/account/buyerregister/?q={}'.format(phoneno))
        else:
            return render(request,'accounts/buyerlogin.html',data)
    else:
        if request.user.userflag==True:
            logout(request)
            return render(request,'accounts/buyerlogin.html',data)
        else:
            return redirect('/')
            
@csrf_protect
@never_cache
def SellerLogin(request):
    data={'title':'LocalBazeer Seller Portal | Login'}
    if not request.user.is_authenticated:
        if request.method=='POST':
            phoneno=request.POST.get('phoneno')
            password=request.POST.get('password')
            user = authenticate(request,phoneno=phoneno, password=password)
            if user is not None:
                if CustomUser.objects.get(phoneno=phoneno).userflag==True:
                    if CustomUser.objects.get(phoneno=phoneno).verified==False:
                        return redirect(f'/account/verify/{phoneno}')
                    else:
                        login(request,user)
                        if 'next' in request.GET:
                            return redirect(request.GET['next'])
                        else:
                            return redirect('/seller') 
                else:
                    data['message']='''<div class="alert alert-warning" role="alert">
                    You have no account associated with Seller Permission !</div>'''
                    return render(request,'accounts/sellerlogin.html',data)
            else:
                data['message']='''<div class="alert alert-danger" role="alert">
                    Phone No or Password not matched !</div>'''
                return render(request,'accounts/sellerlogin.html',data)
        else:
            return render(request,'accounts/sellerlogin.html',data)
    else:
        if request.user.userflag==False:
            logout(request)
            return render(request,'accounts/sellerlogin.html',data)
        else:
            return redirect('/seller') 

@login_required(login_url='/account/sellerlogin')
def sellerlogout(request):
    logout(request)
    return redirect('/account/sellerlogin',{'message':'''<div class="alert alert-success" role="alert">Logged out  Successfully</div>'''})

@login_required(login_url='/account/buyerlogin')
def buyerlogout(request):
    logout(request)
    return redirect('/')


# @csrf_protect
# @never_cache
# def verifyotp(request,phoneno):
#     data={'title':'LocalBazeer Seller Portal | Verify'}
#     data['phoneno']=phoneno
#     if request.method=='POST':
#         otp1=request.POST.get('otp')
#         row=PhoneOtp.objects.filter(phoneno=phoneno)
#         if len(row)==1:
#             if row[0].count>0:
#                 if row[0].otp==int(otp1):
#                     user=CustomUser.objects.get(phoneno=phoneno)
#                     user.verified=True
#                     user.save()
#                     if user.userflag == False :
#                         referrerprofileid=int(user.buyer.referral.referrerid)
#                         if referrerprofileid != -1:
#                             referrerprofile=referralfirst.objects.get(user_id=referrerprofileid)
#                             referrerprofile.rewardpoint+=20
#                             referrerprofile.save()
#                         login(request,user)
#                         if 'next' in request.GET:
#                             return redirect(request.GET['next'])
#                         else:
#                             data['url'] = '/'
#                     else:
#                         data['url']='/seller'
#                     return render(request,'accounts/success.html',data)
#                 else:
#                     row[0].count-=1
#                     row[0].save()
#                     data['message']='''<div class="alert alert-danger" role="alert">
#                     Entered Otp is incorrect . Re-enter Otp Correctly</div>'''
#                     return render(request,'accounts/verify.html',data)
#             else:
#                 data['message']='''<div class="alert alert-danger" role="alert">
#                 You have tried to verify 3 times today. Try after 24 hours</div>'''
#                 return render(request,'accounts/verify.html',data)
#         else:
#             data['message']='''<div class="alert alert-warning" role="alert">
#             This number is not a registered one. Please register before verification</div>'''
#             return render(request,'accounts/verify.html',data)
#     else:
#         return render(request,'accounts/verify.html',data)


@csrf_protect
@never_cache
def verifyotp(request,phoneno):
    data={'title':'LocalBazeer | Verify'}
    data['phoneno']=phoneno
    if request.method=='POST':
        otp1=request.POST.get('otp')
        row=PhoneOtp.objects.filter(phoneno=phoneno).order_by("-id")
        if len(row)>=1:
            if row[0].count>0:
                if row[0].otp==int(otp1):
                    user=CustomUser.objects.get(phoneno=phoneno)
                    user.verified=True
                    user.save()
                    if user.userflag == False :
                        referrerprofileid=int(user.buyer.referral.referrerid)
                        if referrerprofileid != -1:
                            referrerprofile=referralfirst.objects.get(user_id=referrerprofileid)
                            referrerprofile.rewardpoint+=20
                            referrerprofile.save()
                        login(request,user)
                        if 'next' in request.GET:
                            return redirect(request.GET['next'])
                        else:
                            data['url'] = '/'
                    else:
                        data['url']='/seller'
                    return redirect("/")
                    # return render(request,'accounts/success.html',data)
                else:
                    row[0].count-=1
                    row[0].save()
                    data['message']='''<div class="alert alert-danger" role="alert">
                    Entered Otp is incorrect . Re-enter Otp Correctly</div>'''
                    return render(request,'accounts/verify.html',data)
            else:
                data['message']='''<div class="alert alert-danger" role="alert">
                You have tried to verify 3 times today. Try after 24 hours</div>'''
                return render(request,'accounts/verify.html',data)
        else:
            data['message']='''<div class="alert alert-warning" role="alert">
            This number is not a registered one. Please register before verification</div>'''
            return render(request,'accounts/verify.html',data)
    else:
        return render(request,'accounts/verify.html',data)






@csrf_protect
@never_cache
def resendotp(request):
    
    data={'title':'LocalBazeer Seller Portal | Verify'}
    phoneno=request.GET.get('q')
    row=PhoneOtp.objects.filter(phoneno=phoneno)
    if len(row)==1:
        if row[0].count>0:
            payload=row[0].message
            sendMessage(str(row[0].phoneno),payload)
            # print(response)
            return redirect('/account/verify/{}'.format(phoneno))
        else:
            return render(request,'accounts/maxreached.html')
    else:
        return HttpResponse('<h1>>Fail. Contact with Admin</h1>')

@csrf_protect
@never_cache
def forgetpass(request):
    if request.method == 'POST':
        if int(request.POST.get('step'))== 1:
            phoneno= request.POST.get('phoneno')
            otp=random.randint(11111,99999)
            try:
                if CustomUser.objects.get(phoneno=phoneno):
                    OtpDirectory.objects.create(
                        phoneno=phoneno,
                        otp=otp,
                    )
                    #payload = "sender_id=IMPSMS&language=english&route=qt&numbers="+str(phoneno)+"&message=31943&variables={#BB#}&variables_values="+str(otp)
                    #response = requests.request("POST", url, data=payload, headers=headers)
                    sendMessage(str(phoneno),"OTP is {}".format(str(otp)))
                    # print(response)
                    # print(OtpDirectory.objects.filter(phoneno=phoneno).order_by('-id')[0].otp)
                    return render(request,'accounts/forgetpasssecond.html',{"phoneno":phoneno})
            except:
                return render(request,'accounts/forgetpassfirst.html',{"phoneno":phoneno,"message":'''<div class="alert alert-danger" role="alert">
                This Number {} Does Not Exsists</div>'''.format(phoneno)})

        elif int(request.POST.get('step'))== 2:
            phoneno= request.POST.get('phoneno')
            otp=request.POST.get('otp')
            if OtpDirectory.objects.filter(phoneno=phoneno).order_by('-id')[0].otp == int(otp):
                return render(request,'accounts/forgetpassthird.html',{'phoneno':phoneno})
            else:
                return render(request,'accounts/forgetpassfirst.html',{"message":'''<div class="alert alert-danger" role="alert">
                Otp does not match... Please Retry</div>'''.format(phoneno)})
        elif int(request.POST.get('step'))== 3:
            phoneno= request.POST.get('phoneno')
            password=request.POST.get('password')
            userr=CustomUser.objects.get(phoneno=phoneno)
            userr.set_password(password)
            userr.save()
            return render(request,'accounts/successreset.html')

    return render(request,'accounts/forgetpassfirst.html')