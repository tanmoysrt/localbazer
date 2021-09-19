from django.shortcuts import render,redirect
from django.http import HttpResponse
from datamanagement.models import ProductData,AllIndiaPinCode,OrderHistory
from accounts.models import CustomUser
from referral1.models import referralfirst,referralrequest
from django.views.decorators.csrf import csrf_protect
from seller.models import SellerProfile
from .functions import get_query,normalize_query
from localbazeer.settings import MEDIA_URL,MEDIA_ROOT
from django.contrib.auth.decorators import login_required
from accounts.decorators import buyer_required
import urllib
import json
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
import urllib.parse
def home(request):
    totaldata={
        'title':'LocalBazer.com | Home',
        'MEDIA_URL':MEDIA_URL,
    }


    shops = SellerProfile.objects.filter(shopcategoty="food").exclude(shopname="Unnamed Shop").order_by('-ordering_shop')
    # print(shops)
    paginator=Paginator(shops, 10) # number of shops show in the shop list in a single ajax call
    page = request.GET.get('page')
    try:
        shops = paginator.page(page)
    except PageNotAnInteger:
        shops = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        shops = paginator.page(paginator.num_pages)


    if request.is_ajax():
        return render(request,'buyer/ajax_shops_by_catagory.html',{'shops':shops})

    # products = ProductData.objects.filter(seller__shopcategoty="food").order_by("-seller__ordering_shop")
    # paginator = Paginator(products, 4)
    # page = request.GET.get('page')
    # try:
    #     products = paginator.page(page)
    #     totaldata['products']=products
    # except PageNotAnInteger:
    #     products = paginator.page(1)
    #     totaldata['products']=products
    # except EmptyPage:
    #     if request.is_ajax():
    #         return HttpResponse('')
    #     products = paginator.page(paginator.num_pages)
    #     totaldata['products']=products


    # if request.is_ajax():
    #     totaldata['products']=products
    #     return render(request,'buyer/ajax_product_list.html',totaldata)
    
    # totaldata['products']=products
    totaldata["shops"] = shops
    return render(request,'buyer/landing.html',totaldata)

def search(request):
    
    totaldata={
        'MEDIA_URL' : MEDIA_URL,
        'title' : "Search & Find Anything On LocalBazer.com | Your Nearest Shop",
    }
    data=None
    try :
        # Removing pncode filter 30th july - Ts
        # pincode=request.COOKIES['pincode']
        seller=[]
        # lookup=Q(shoppincodes__icontains=int(pincode))|Q(allindia=1)
        # sellers=SellerProfile.objects.filter(lookup)
        sellers=SellerProfile.objects.all()
        for i in sellers:
            seller.append(i.id)
        seller=tuple(seller)
        selectedproducts=ProductData.objects.filter(seller_id__in=seller)
        # print(selectedproducts)
        if 'shop' in request.GET and request.GET['shop'].strip():
            shop=request.GET['shop']
            shopfilter=selectedproducts.filter(seller_id=int(shop))
            if 'q' in request.GET and request.GET['q'].strip():
                query_string=request.GET['q']
                totaldata['query']=query_string
                entry_query = get_query(query_string, ['name', 'details','subcategory'])
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    maxfilter=shopfilter.filter(price__lte=maxx)
                    if 'sub' in request.GET and request.GET['max'].strip():
                        sub=request.GET['sub']
                        subfilter=maxfilter.filter(subcategory=sub)
                        data = subfilter.filter(entry_query) 
                    else:
                        data=maxfilter.filter(entry_query)##Only till max
                elif 'sub' in request.GET and request.GET['sub'].strip():
                    sub=request.GET['sub'] #Sub /not max
                    subfilter=shopfilter.filter(subcategory=sub)
                    data=subfilter.filter(entry_query)
                else:
                    data=shopfilter.filter(entry_query) # No sub/ No Max/ Only search +shop
            elif 'sub' in request.GET and request.GET['sub'].strip():
                sub=request.GET['sub']
                subfilter=shopfilter.filter(subcategory=sub)
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    data=subfilter.filter(price__lte=maxx)  # Sub / Max
                else:
                    data=subfilter
            elif 'max' in request.GET and request.GET['max'].strip():
                maxx=request.GET['max']
                data=shopfilter.filter(price__lte=maxx)  # Sub / Max
            else:
                data=shopfilter

        else:
            if 'q' in request.GET and request.GET['q'].strip():
                query_string=request.GET['q']
                totaldata['query']=query_string
                entry_query = get_query(query_string, ['name', 'details','subcategory'])
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    maxfilter=selectedproducts.filter(price__lte=maxx)
                    if 'sub' in request.GET and request.GET['sub'].strip():
                        sub=request.GET['sub']
                        subfilter=maxfilter.filter(subcategory=sub)
                        data = subfilter.filter(entry_query) 
                    else:
                        data=maxfilter.filter(entry_query)##Only till max
                elif 'sub' in request.GET and request.GET['sub'].strip():
                    sub=request.GET['sub'] #Sub /not max
                    subfilter=selectedproducts.filter(subcategory=sub)
                    data=subfilter.filter(entry_query)
                else:
                    data=selectedproducts.filter(entry_query) # No sub/ No Max/ Only search +shop
            elif 'sub' in request.GET and request.GET['sub'].strip():
                sub=request.GET['sub']
                subfilter=selectedproducts.filter(subcategory=sub)
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    data=subfilter.filter(price__lte=maxx)  # Sub / Max
                else:
                    data=subfilter
            elif 'max' in request.GET and request.GET['max'].strip():
                maxx=request.GET['max']
                data=selectedproducts.filter(price__lte=maxx)  # Sub / Max
            else:
                data=selectedproducts
    except:
        if 'shop' in request.GET and request.GET['shop'].strip():
            shop=request.GET['shop']
            shopfilter=ProductData.objects.filter(seller_id=int(shop))
            if 'q' in request.GET and request.GET['q'].strip():
                query_string=request.GET['q']
                totaldata['query']=query_string
                entry_query = get_query(query_string, ['name', 'details','subcategory'])
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    maxfilter=shopfilter.filter(price__lte=maxx)
                    if 'sub' in request.GET and request.GET['max'].strip():
                        sub=request.GET['sub']
                        subfilter=maxfilter.filter(subcategory=sub)
                        data = subfilter.filter(entry_query) 
                    else:
                        data=maxfilter.filter(entry_query)##Only till max
                elif 'sub' in request.GET and request.GET['sub'].strip():
                    sub=request.GET['sub'] #Sub /not max
                    subfilter=shopfilter.filter(subcategory=sub)
                    data=subfilter.filter(entry_query)
                else:
                    data=shopfilter.filter(entry_query) # No sub/ No Max/ Only search +shop
            elif 'sub' in request.GET and request.GET['sub'].strip():
                sub=request.GET['sub']
                subfilter=shopfilter.filter(subcategory=sub)
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    data=subfilter.filter(price__lte=maxx)  # Sub / Max
                else:
                    data=subfilter
            elif 'max' in request.GET and request.GET['max'].strip():
                maxx=request.GET['max']
                data=shopfilter.filter(price__lte=maxx)  # Sub / Max
            else:
                data=shopfilter

        else:
            if 'q' in request.GET and request.GET['q'].strip():
                query_string=request.GET['q']
                totaldata['query']=query_string
                entry_query = get_query(query_string, ['name', 'details','subcategory'])
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    maxfilter=ProductData.objects.filter(price__lte=maxx)
                    if 'sub' in request.GET and request.GET['sub'].strip():
                        sub=request.GET['sub']
                        subfilter=maxfilter.filter(subcategory=sub)
                        data = subfilter.filter(entry_query) 
                    else:
                        data=maxfilter.filter(entry_query)##Only till max
                elif 'sub' in request.GET and request.GET['sub'].strip():
                    sub=request.GET['sub'] #Sub /not max
                    subfilter=ProductData.objects.filter(subcategory=sub)
                    data=subfilter.filter(entry_query)
                else:
                    data=ProductData.objects.filter(entry_query) # No sub/ No Max/ Only search +shop
            elif 'sub' in request.GET and request.GET['sub'].strip():
                sub=request.GET['sub']
                subfilter=ProductData.objects.filter(subcategory=sub)
                if 'max' in request.GET and request.GET['max'].strip():
                    maxx=request.GET['max']
                    data=subfilter.filter(price__lte=maxx)  # Sub / Max
                else:
                    data=subfilter
            elif 'max' in request.GET and request.GET['max'].strip():
                maxx=request.GET['max']
                data=ProductData.objects.filter(price__lte=maxx)  # Sub / Max
            else:
                data=ProductData.objects.all()

            
    # return HttpResponse(data)
   
    products = data.order_by('price')
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
        totaldata['products']=products
    except PageNotAnInteger:
        products = paginator.page(1)
        totaldata['products']=products
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        products = paginator.page(paginator.num_pages)
        totaldata['products']=products


    if request.is_ajax():
        totaldata['products']=products
        return render(request,'buyer/ajax_search.html',totaldata)
    
    totaldata['products']=products
    return render(request,'buyer/searchpage.html',totaldata)

def orderdetails(request):
    data={
        'title':'LocalBazer | Not Found',
    }
    if 'id' in request.GET:
        id=request.GET['id']
        if id != "":
            product=ProductData.objects.get(id=id)
            data['product']=product
            data['title']="LocalBazer | "+str(product.name)
    return render(request,'buyer/productdetails.html',data)

def checkpin(request):
    data=0
    if 'pin' in request.GET and request.GET['pin'].strip():
        pin=request.GET['pin']
        allpin=AllIndiaPinCode.objects.all()
        for i in allpin:
            if int(pin) == int(i.pincode):
                data=1
                break
            else:
                continue
    return HttpResponse(data)

def cart(request):
    totaldata={
        'title':'LocalBazer.com | Cart'
    }
    try:
        data = urllib.parse.unquote(request.COOKIES['devicelist'])
        data = json.loads(data)
        cartdatas = data['cartItems']
    except:
        cartdatas = []
    products = []
    
    for cart in cartdatas:
        products = products + [ProductData.objects.get(id=cart['deviceId'])]
    totaldata['products']=products
    return render(request,'buyer/cart_page.html',totaldata)
@login_required(login_url='/account/buyerlogin?next={{request.path}}')
@buyer_required
def orderhistory(request):
    data={
        'history':OrderHistory.objects.filter(buyer_id=request.user.buyer.id).order_by("-id"),
        'title':'Order History | LocalBazer.com'
    }

    return render(request,'buyer/orderhistory.html',data)
    
def shopcategory(request):
    try:
        # pincode=request.COOKIES['pincode']
        if 'q' in request.GET and request.GET['q'].strip():
            q=request.GET['q']
            # lookup=Q(shoppincodes__icontains=int(pincode))|Q(allindia=1)
            # shops = SellerProfile.objects.filter(lookup).filter(shopcategoty=q).order_by('-ordering_shop')
            shops = SellerProfile.objects.filter(shopcategoty=q).exclude(shopname="Unnamed Shop").order_by('-ordering_shop')
        else:
            # lookup=Q(shoppincodes__icontains=int(pincode))|Q(allindia=1)
            # shops = SellerProfile.objects.filter(lookup).order_by('-ordering_shop')
            shops = SellerProfile.objects.exclude(shopname="Unnamed Shop").order_by('-ordering_shop')
    except:
        if 'q' in request.GET and request.GET['q'].strip():
            q=request.GET['q']
            shops = SellerProfile.objects.filter(shopcategoty=q).exclude(shopname="Unnamed Shop").order_by('-ordering_shop')
        else:
            shops = SellerProfile.objects.all().exclude(shopname="Unnamed Shop").order_by('-ordering_shop')
    # print(shops)
    paginator=Paginator(shops, 5) # number of shops show in the shop list in a single ajax call
    page = request.GET.get('page')
    try:
        shops = paginator.page(page)
    except PageNotAnInteger:
        shops = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        shops = paginator.page(paginator.num_pages)


    if request.is_ajax():
        return render(request,'buyer/ajax_shops_by_catagory.html',{'shops':shops})

    data ={
        'shops':shops,
        'title':'Search Local Shop'
        }
    return render(request,'buyer/shop_by_catagory.html',data)

def shoppage(request):
    if 'q' in request.GET and request.GET['q'].strip():
        q=request.GET['q']
        data={
            'products':ProductData.objects.filter(seller_id=int(q)).order_by("-id"),
            'title':SellerProfile.objects.get(id=int(q)).shopname+" | LocalBazer.com",
            'shopdata':SellerProfile.objects.get(id=int(q)),
            'sellerid':q,
            'sellername':CustomUser.objects.get(id=SellerProfile.objects.get(id=int(q)).user_id).name,
            'metaimage':SellerProfile.objects.get(id=int(q)).shopbanner,
        }
        return render(request,"buyer/shoppage.html",data)
    else:
        return HttpResponse("404 Not Found")

@login_required(login_url='/account/buyerlogin?next={{request.path}}')
@buyer_required
def accountspage(request):
    link='''Sign Up at LocalBazer.com . Delivery Charge on your first order will be free .
Order products , foods from your local shop with Cash On Delivery
Signup Now : https://localbazer.com/account/buyerregister/?refer='''+str(request.user.buyer.id)
    data={
        'title' : "Accounts | LocalBazer.com",
        'name':request.user.name,
        'total_orders':len(OrderHistory.objects.filter(buyer_id=request.user.buyer.id)),
        'reward_coins':int(request.user.buyer.referral.rewardpoint),
        'referral_counts':len(referralfirst.objects.filter(referrerid=request.user.buyer.id)),
        'free_delivery':request.user.buyer.referral.freedelivery,
        'link':"https://localbazer.com/account/buyerregister/?refer="+str(request.user.buyer.id),
        'link1':urllib.parse.quote(link),
    }
    return render(request,"buyer/accountdetails.html",data)


@login_required(login_url='/account/buyerlogin?next={{request.path}}')
@buyer_required
def referralpage(request):
    data={
        'title' : "Refer & Earn | LocalBazer.com",
        'name':request.user.name,
        'reward_coins':int(request.user.buyer.referral.rewardpoint),
        'referral_counts':len(referralfirst.objects.filter(referrerid=request.user.buyer.id)),
    }
    if request.method == 'POST':
        if int(request.POST.get('processid')) == 1 :
            referwithdraw=referralrequest.objects.create(
                userid=request.user.id,
                phoneno=request.user.phoneno,
                additionalphoneno=request.POST.get('paytmno'),
                rewardpoint=100,
                option='paytm',
            )
            referaccount = request.user.buyer.referral
            referaccount.rewardpoint-=100
            referaccount.save()
            referwithdraw.save()
            return redirect("/profile")
        elif int(request.POST.get('processid')) == 2 :
            referwithdraw=referralrequest.objects.create(
                userid=request.user.id,
                phoneno=request.user.phoneno,
                additionalphoneno=request.POST.get('mobileno'),
                rewardpoint=100,
                option='amazonpay',
            )
            referaccount = request.user.buyer.referral
            referaccount.rewardpoint-=100
            referaccount.save()
            referwithdraw.save()
            return redirect("/profile")
        elif int(request.POST.get('processid')) == 3 :
            referwithdraw=referralrequest.objects.create(
                userid=request.user.id,
                phoneno=request.user.phoneno,
                additionalphoneno=request.POST.get('mobileno'),
                rewardpoint=100,
                option='recharge',
            )
            referaccount = request.user.buyer.referral
            referaccount.rewardpoint-=100
            referaccount.save()
            referwithdraw.save()
            return redirect("/profile")
    return render(request,"buyer/referralpage.html",data)
