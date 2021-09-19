import os
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datamanagement.models import OrderHistory, ProductData
from django.contrib.auth.decorators import login_required
from referral1.models import referralfirst
from .decaorators import toplevel_superuser_required
from accounts.models import CustomUser
from buyer.models import BuyerProfile
from seller.models import SellerProfile
import json, requests
from localbazeer.settings import MEDIA_URL, headers, url
from accounts.models import PhoneOtp, OtpDirectory
from shopqrhandler.models import shopqrdata
from datetime import date, timedelta
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


scope = 'https://www.googleapis.com/auth/analytics.readonly'
key_file_location = os.path.join(os.path.dirname(__file__), './secrects.json')

def adminlogin(request):
    if request.user.is_authenticated and request.user.is_superuser and request.user.is_active:
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            return redirect('/admin')
    else:
        if request.method == 'POST':
            phoneno = int(request.POST.get('ph'))
            password = request.POST.get('p')
            try:
                user = authenticate(request, phoneno=phoneno, password=password)
                if user is not None:
                    if user.is_authenticated and user.is_active and user.is_superuser:
                        login(request, user)
                        if 'next' in request.GET:
                            return redirect(request.GET['next'])
                        else:
                            return redirect('/admin')
                    return HttpResponse("<h1>Invalid Login | Access Forbidden 403</h1>", status=403)
                return HttpResponse("<h1>Invalid Credentials | 401</h1>", status=401)

            except AttributeError:
                return HttpResponse("Anonymous User Error.....Go back & check credentials", status=500)
        return render(request, 'adminpanel/login.html')


def logoutt(request):
    logout(request)
    return redirect('/admin')
@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def dashboard(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'totalorderstillnow': len(OrderHistory.objects.all()),
        'totalusers': len(CustomUser.objects.filter(is_superuser=False)),
        'orderdataratiop': len(OrderHistory.objects.filter(status='pending')),
        'orderdataratiod': len(OrderHistory.objects.filter(status='delivered')),
        'orderdataratioc': len(OrderHistory.objects.filter(status='cancelled')),
    }
    datee = []
    ordersrecord = []
    buyerregistrations=[]
    sellerregistrations=[]
    for i in range(6, -1, -1):
        datee.append(date.today() - timedelta(days=i))
        ordersrecord.append(len(OrderHistory.objects.filter(orderedon__day=(date.today() - timedelta(days=i)).day)))
        buyerregistrations.append(len(CustomUser.objects.filter(date_joined__day=(date.today() - timedelta(days=i)).day).filter(userflag=False)))
        sellerregistrations.append(len(CustomUser.objects.filter(date_joined__day=(date.today() - timedelta(days=i)).day).filter(userflag=True)))
    service = get_service(
        api_name='analytics',
        api_version='v3',
        scopes=[scope],
        key_file_location=key_file_location)
    profile_id = get_first_profile_id(service)
    gadata=get_results(service, profile_id)
    data['date']=datee
    data['ordersrecord']=ordersrecord
    data['buyerregistrations']=buyerregistrations
    data['sellerregistrations']=sellerregistrations
    data['sessions']=gadata[0]
    data['visitors']=gadata[1]

    return render(request, 'adminpanel/dashboard.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def pendingorders(request):
    data = {'pendingcount': len(OrderHistory.objects.filter(status='pending')),
            'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
            'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
            'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
            'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
            'p1': OrderHistory.objects.filter(status='pending')}
    return render(request, 'adminpanel/pendingorders.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def deliveredorders(request):
    data = {'pendingcount': len(OrderHistory.objects.filter(status='pending')),
            'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
            'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
            'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
            'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
            'p1': OrderHistory.objects.filter(status='delivered')}
    return render(request, 'adminpanel/deliveredorders.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def cancelledorders(request):
    data = {'pendingcount': len(OrderHistory.objects.filter(status='pending')),
            'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
            'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
            'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
            'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
            'p1': OrderHistory.objects.filter(status='cancelled')}
    return render(request, 'adminpanel/cancelledorders.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def orderdata(request):
    orderid = request.GET['q']
    orderdata = OrderHistory.objects.get(id=orderid)
    profile = BuyerProfile.objects.get(id=orderdata.buyer_id)
    customuser = CustomUser.objects.get(id=profile.user_id)
    addressdata = json.loads(profile.address)['address']
    pincode = ''
    address = ''
    for i in addressdata:
        if int(i['id']) == int(orderdata.address):
            pincode = i["pincode"]
            address = i['address']
    y = json.loads(orderdata.details)
    cart = y['cart']
    price = 0
    for i in cart:
        price += int(int(i['price']) * int(i['quantity']))
    customerdata = {
        "name": customuser.name,
        "phoneno": customuser.phoneno,
        "emailid": customuser.email,
        "pincode": pincode,
        "address": address,
        "date": orderdata.orderedon.isoformat(),
        "total": price,
        "method": 'Home Delivery' if orderdata.homedelivery else 'Self Pickup',
    }
    productdata = []
    sellerUser = CustomUser.objects.get(id=orderdata.sellerid)
    sellerProfile = sellerUser.seller
    sellerData = {
        "name": sellerUser.name,
        "phoneno": sellerUser.phoneno,
        "address": sellerProfile.shopaddress,
        "shopname": sellerProfile.shopname,
    }
    for i in y['cart']:
        product = ProductData.objects.get(id=i['id'])
        print(str(product.photo))
        temp = {
            "id": product.id,
            "name": product.name,
            "photo": MEDIA_URL + str(product.photo),
            "quantity": i['quantity'],
            "totalprice": int(int(i['price']) * int(i['quantity']))
        }
        productdata.append(temp)
    finaldata = {
        "customerdata": customerdata,
        "sellerdata": sellerData,
        "products": productdata,
    }

    return JsonResponse(json.dumps(finaldata), safe=False)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def buyerregistration(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        phoneno = request.POST.get('phoneno')
        email = request.POST.get('email')
        password = str(request.POST.get('password'))
        if len(CustomUser.objects.filter(phoneno=phoneno)) != 0:
            data['message'] = '''<div class="alert alert-danger" role="alert">
            Phone Number Already Exsists</div>'''
            return render(request, 'adminpanel/buyerregistration.html', data)
        else:
            user = CustomUser.objects.create_user(
                email=email,
                phoneno=phoneno,
                name=name,
                userflag=False,
                verified=True,
                password=password,
            )
            user.set_password(password)
            user.save()
            userprofile = BuyerProfile.objects.create(
                user=user
            )
            userprofile.save()
            referprofile = referralfirst.objects.create(
                user=user.buyer,
                freedelivery=True,
            )
            referprofile.save()
            data['message'] = '''<div class="alert alert-success" role="alert">
            Account Created Successfully ! Let's Login </div>'''
            return render(request, 'adminpanel/buyerregistration.html', data)

    return render(request, 'adminpanel/buyerregistration.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def sellerregistration(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
    }
    if request.method == 'POST' and request.FILES:
        sellername = request.POST.get('name')
        phoneno = request.POST.get('phoneno')
        email = request.POST.get('email')
        password = request.POST.get('password')
        category = request.POST.get('category')
        shopName = request.POST.get('shopName')
        address = request.POST.get('address')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        homedelivery = request.POST.get('homedelivery')
        deliverycharge = request.POST.get('deliverycharge')
        bannerphoto = request.FILES['bannerphoto']
        fs = FileSystemStorage(location='media/shop/banner/')
        filename = fs.save(bannerphoto.name, bannerphoto)
        photoname = fs.generate_filename(filename)
        user = CustomUser.objects.create_user(
            email=email,
            phoneno=phoneno,
            name=sellername,
            userflag=True,
            password=password,
            verified=True,
        )
        user.set_password(password)
        user.save()
        userprofile = SellerProfile.objects.create(
            user=user,
            shopcategoty=category,
            shopname=shopName,
            shopaddress=address,
            shoplongitude=longitude,
            shoplatitude=latitude,
            homedelivery=homedelivery,
            deliverycharge=deliverycharge,
            shopbanner='shop/banner/' + photoname,
        )
        userprofile.save()
        data['message'] = '<div class="alert alert-success" role="alert">Seller Account Created Successfully</div>'
        return render(request, 'adminpanel/sellerregistration.html', data)
    return render(request, 'adminpanel/sellerregistration.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def sellerprofiles(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'profiles': CustomUser.objects.filter(userflag=True).filter(is_superuser=False),
    }
    return render(request, 'adminpanel/sellerprofiles.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def buyerprofiles(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'profiles': CustomUser.objects.filter(userflag=False).filter(is_superuser=False),
    }
    return render(request, 'adminpanel/buyerrprofiles.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def smsgateway(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False))
    }
    if request.method == 'POST':
        phoneno = request.POST.get('phoneno')
        message = request.POST.get('message')
        payload = "sender_id=FSTSMS&message=" + message + "&language=english&route=p&numbers=" + phoneno
        response = requests.request("POST", url, data=payload, headers=headers)
        tmp = json.loads(response.text)
        msg = tmp['message']
        data['message'] = '<div class="alert alert-success" role="alert">' + msg[0] + '</div>'
        return render(request, 'adminpanel/smsgateway.html', data)
    return render(request, 'adminpanel/smsgateway.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def orerlogs(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'orders': OrderHistory.objects.all()
    }
    return render(request, 'adminpanel/orderlogs.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def newotp(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'otps': PhoneOtp.objects.all(),
    }
    return render(request, 'adminpanel/newotplogs.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def resetotp(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'otps': OtpDirectory.objects.all(),
    }
    return render(request, 'adminpanel/resetotplogs.html', data)


@login_required(login_url='/admin/login?next={{request.path}}')
@toplevel_superuser_required
def qrcodes(request):
    data = {
        'pendingcount': len(OrderHistory.objects.filter(status='pending')),
        'deliverycount': len(OrderHistory.objects.filter(status='delivered')),
        'cancelledcount': len(OrderHistory.objects.filter(status='cancelled')),
        'sellerprofilescount': len(CustomUser.objects.filter(userflag=True).filter(is_superuser=False)),
        'buyerprofilescount': len(CustomUser.objects.filter(userflag=False).filter(is_superuser=False)),
        'qrs': shopqrdata.objects.all(),
    }
    return render(request, 'adminpanel/qrdatalogs.html', data)





def get_service(api_name, api_version, scopes, key_file_location):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scopes=scopes)
    service = build(api_name, api_version, credentials=credentials)
    return service


def get_first_profile_id(service):
    accounts = service.management().accounts().list().execute()
    if accounts.get('items'):
        account = accounts.get('items')[0].get('id')
        properties = service.management().webproperties().list(
                accountId=account).execute()
        if properties.get('items'):
            property = properties.get('items')[0].get('id')
            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()
            if profiles.get('items'):
                return profiles.get('items')[0].get('id')
    return None


def get_results(service, profile_id):
    tmp=[]
    a=service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='7daysAgo',
            end_date='today',
            metrics='ga:sessions').execute()
    tmp.append(a.get('rows')[0][0])
    b=service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='7daysAgo',
            end_date='today',
            metrics='ga:visitors').execute()
    tmp.append(b.get('rows')[0][0])
    return tmp