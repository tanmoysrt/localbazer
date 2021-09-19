from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in
from datamanagement.models import ProductData,OrderHistory,AllIndiaPinCode
from accounts.models import CustomUser
from seller.models import SellerProfile
from buyer.models import BuyerProfile
from localbazeer.settings import MEDIA_URL, headers,url
import json
from django.contrib.auth.decorators import login_required
from accounts.decorators import buyer_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
import urllib
from django.utils import timezone
import requests


def sendMessage(numbers, content):
    url = f"https://www.fast2sms.com/dev/bulkV2?authorization=j2q8pEbBWH7ZvKrVF6JaTxGkg1PAwfhysUYQSmMo3Xt5u4dLniJfSndABsiDpOGcH2gChWXjbY4rRmIe&route=v3&sender_id=TXTIND&message={content}&language=english&flash=0&numbers={numbers}"
    try:
        res = requests.get(url)
        print(res)
    except:
        print("ERROR : Can't send message")

@login_required(login_url='/account/buyerlogin?next={{request.path}}')
@csrf_protect
@never_cache
def checkout(request):
    if request.method == "POST":
        q=urllib.parse.unquote(request.COOKIES['devicelist'])
        homedelivery=request.POST.get('homedelivery')
        buyer=request.user.buyer.id
        address=request.POST.get('address')
        data=json.loads(q)
        data=data['cartItems']
        orders=[]
        sellers=set()
        for i in data:
            x=dict()
            selected=ProductData.objects.get(id=i['deviceId'])
            x['id']=i['deviceId']
            x['quantity']=i['quantity']
            x['price']=selected.price*(100-selected.discount)/100
            x['sellerid']=selected.seller.user_id
            x['homedelivery']=int(selected.seller.homedelivery)
            orders.append(x)
            sellers.add(x['sellerid'])
        if int(homedelivery)==0:
            for i in sellers:
                a=[]
                for j in orders:
                    if i==j['sellerid']:
                        a.append({'id':j['id'],'quantity':j['quantity'],'price':j['price']})
                        x={'cart':a}
                        y=json.dumps(x)
                neworder=OrderHistory.objects.create(
                    buyer_id=buyer,
                    address=address,
                    details=y,
                    sellerid=i,
                    homedelivery=False,
                )
                neworder.save()
                phon=CustomUser.objects.get(id=i).phoneno
                sendMessage("6295771635,6296276773,{}".format(str(phon)),"New order recieved at {}. Thanks & Regards : localbazer.com".format(str(timezone.now())))
                #payload = "sender_id=SMSIND&language=english&route=qt&numbers=6296276773,"+str(phon)+"&message=31347&variables={#FF#}&variables_values="+str(timezone.now())
                #response = requests.request("POST", url, data=payload, headers=headers)
                # print(response)
                response=render(request,'checkout/success.html')
                response.delete_cookie('devicelist')
        elif int(homedelivery)==1:
            for i in sellers:
                a=[]
                for j in orders:
                    if i==j['sellerid']:
                        a.append({'id':j['id'],'quantity':j['quantity'],'price':j['price']})
                        x={'cart':a}
                        y=json.dumps(x)
                homedeliverychoice=SellerProfile.objects.get(user_id=i).homedelivery
                neworder=OrderHistory.objects.create(
                    buyer_id=buyer,
                    address=address,
                    details=y,
                    sellerid=i,
                    homedelivery=homedeliverychoice,
                )
                neworder.save()
                phon=CustomUser.objects.get(id=i).phoneno
                #payload = "sender_id=SMSIND&language=english&route=qt&numbers=6296276773,"+str(phon)+"&message=31347&variables={#FF#}&variables_values="+str(timezone.now())
                #response = requests.request("POST", url, data=payload, headers=headers)
                # print(response)
                sendMessage("6295771635,6296276773,{}".format(str(phon)),"New order recieved at {}. Thanks & Regards : localbazer.com".format(str(timezone.now())))
                response=render(request,'checkout/success.html')
                response.delete_cookie('devicelist')
        return response
@login_required(login_url='/account/buyerlogin?next={{request.path}}')
@csrf_protect
@never_cache
def test(request):
    return render(request,'checkout/address.html')


# Update 30th July - Remove pincode
def loadaddress(request):
    # pincode=int(request.COOKIES['pincode'])
    address=BuyerProfile.objects.get(user_id=request.user.id).address
    x=json.loads(address)
    y=x['address']
    # z=[]
    # for i in y:
        # if int(i['pincode'])!=pincode:
        # z.append(i)
    # if z != []:
    #     for i in z:
    #         y.remove(i)
    address=json.dumps({'address':y})
    return JsonResponse(address,safe=False)


def addaddress(request):
    if request.method=='POST':
        addres=request.POST.get('address')
        pincod=request.POST.get('pincode')
        buyer=BuyerProfile.objects.get(user_id=request.user.id)
        address=buyer.address
        address=json.loads(address)
        address['address'].append({'id':len(address['address'])+1,'address':addres,'pincode':pincod})
        buyer.address=json.dumps(address)
        buyer.save()
    return HttpResponse('ok')


@buyer_required
@login_required(login_url='/account/buyerlogin?next={{request.path}}')
def checkoutfirst(request):
    try:
        data = urllib.parse.unquote(request.COOKIES['devicelist'])
        data = json.loads(data)
        cartdatas = data['cartItems']
        # print(cartdatas)
    except:
        cartdatas = []
    products = []
    price = 0
    total = 0
    items_list = []
    deliverable = []

    nondeliverable = []
    for cart in cartdatas:
        products = products + [ProductData.objects.get(id=cart['deviceId'])]
        items_list = items_list + [cart['quantity']]
    i = 0
    for product in products:
        #The main total price without discount
        price = price + (product.price * items_list[i])
        #discounted total price
        total = (product.give_total_price * items_list[i]) + total
        i = i+1
        if product.seller.homedelivery:
            deliverable = deliverable + [product]
            # print(deliverable)
        else:
            nondeliverable = nondeliverable + [product]


    #Changing for delivery
    seller_list = []
    for product in deliverable:
         seller_list = seller_list + [(product.seller.user.phoneno)]
    seller_list = set(seller_list)
    seller_list = list(seller_list)
    print(seller_list)
    #slot for calculating remaining price of delivery
    seller_dict_list = []
    for seller in seller_list:
        price_total = 0
        seller_dict = {'phone':0,'price':0}
        for product in deliverable:
            if seller == product.seller.user.phoneno:
                for i in cartdatas:
                    if int(i['deviceId'])==int(product.id):
                        quantity=i['quantity']
                        break
                price_total = price_total + (product.price*(100-product.discount)/100)*quantity
                min_delivery_price = product.seller.minpriceforfreedelivery
        price_total = min_delivery_price - price_total
        seller_dict['phone'] = seller
        seller_dict['price'] = price_total
        seller_dict_list = seller_dict_list + [seller_dict]

    print(seller_dict_list)
    #changing
    
    saving = price - total
    if request.user.is_authenticated:
        if request.user.userflag == False:
            userType = 'buyer'
            address = request.user.buyer.address
    else:
        userType = 'unknown'
    #A flag to detrtmine atleast 1 deliverable product exists or not
    delivery_flag = False
    if deliverable:
        delivery_flag = True
    print( delivery_flag)
    context = {'title':'Checkout | LocalBazeer.com','products':products,'total':total,'saving':saving,'price':price,'address':address,'deliverable':deliverable,'nondeliverable':nondeliverable,'delivery_flag':delivery_flag,'seller_dict_list':seller_dict_list}
    return render(request,'checkout/checkoutpage.html',context)


