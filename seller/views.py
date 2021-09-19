from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in
from datamanagement.models import ProductData,OrderHistory,AllIndiaPinCode
from seller.models import SellerProfile
from localbazeer.settings import MEDIA_URL
from datetime import timedelta
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import json
from accounts.decorators import seller_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def dashboard(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'ordersinweek':len(OrderHistory.objects.filter(sellerid=request.user.id,orderedon__gte=timezone.now().date()-timedelta(days=7))),
        'sortproduct':ProductData.objects.filter(seller_id=SellerProfile.objects.get(user_id=request.user.id).id,available__lte=5).order_by('id')
    }
    return render(request,'seller/dashboard.html',data) 


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def pendingorder(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'pendingorders':OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending').order_by('-orderedon')
    
    }
    return render(request,'seller/pendingorder.html',data)


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def deliveredorder(request):

    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'deliveredorder':OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered').order_by('-orderedon')
    
    }
    return render(request,'seller/deliveredorder.html',data)


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def allorder(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'allorder':OrderHistory.objects.filter(sellerid=request.user.id).order_by('-orderedon')
    
    }

    return render(request,'seller/allordered.html',data)


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
@csrf_protect
@never_cache

def addproduct(request):
    
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'subid':request.user.seller.shopcategoty,
    
    }
    if request.method == 'POST' and request.FILES['photo']:
        photo = request.FILES['photo']
        fs = FileSystemStorage(location='media/shop/product/')
        filename = fs.save(photo.name, photo)
        photoname=fs.generate_filename(filename) 
        name=request.POST.get('name')
        origin=request.POST.get('origin')
        details=request.POST.get('details')
        mrp=request.POST.get('mrp')
        discount=request.POST.get('discount')
        subcategory=request.POST.get('subcategory')
        available=request.POST.get('available')
        newproduct=ProductData.objects.create(
            name=name,
            details=details,
            price=mrp,
            originofproduct=origin,
            available=available,
            review=5,
            discount=discount,
            subcategory=subcategory,
            photo='shop/product/'+photoname,
            seller_id=SellerProfile.objects.get(user_id=request.user.id).id
        )
        newproduct.save()
        data['message']='''<div class="alert alert-success" role="alert">
            Product Saved Successfully</div>'''
        return render(request, 'seller/addproduct.html',data)
    
    return render(request,'seller/addproduct.html',data)


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def updateproduct(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'allproducts':ProductData.objects.filter(seller_id=SellerProfile.objects.get(user_id=request.user.id).id).order_by('id'),
        
    }
    return render(request,'seller/update.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def deleteproduct(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'allproducts':ProductData.objects.filter(seller_id=SellerProfile.objects.get(user_id=request.user.id).id).order_by('id')
    
    }
    return render(request,'seller/delete.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def deleterecord(request):
    try:
        id= request.GET.get('q') ###Just a api
        product=ProductData.objects.get(id=int(id))
        if product.seller_id==SellerProfile.objects.get(user_id=request.user.id).id:
            product.delete()
            return redirect('/seller/deleteproduct')
        else:
            return HttpResponse('<h1>Fail To Delete! Contact with SupportTeam</h1>')
    except:
        return HttpResponse('<h1>Some Error Occured ! Please Retry</h1>')


@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
@csrf_protect
@never_cache
def editrecord(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    try:
        id= request.GET.get('q') ###Just a api
        product=ProductData.objects.get(id=int(id))
        if product.seller_id==SellerProfile.objects.get(user_id=request.user.id).id:
            if request.method=='POST':
                name=request.POST.get('name')
                details=request.POST.get('details')
                price=request.POST.get('mrp')
                discount=request.POST.get('discount')
                available=request.POST.get('available')
                product.name=name
                product.details=details
                product.price=price
                product.discount=discount
                product.available=available
                product.save()
                data['message']='''<div class="alert alert-success" role="alert">
            Product Updated Successfully</div>'''
                data['allproducts']=ProductData.objects.filter(seller_id=SellerProfile.objects.get(user_id=request.user.id).id).order_by('id')
                return render(request,'seller/update.html',data)
            else:
                data['name']=product.name
                data['details']=product.details
                data['price']=product.price
                data['discount']=product.discount
                data['available']=product.available
                return render(request,'seller/editrecord.html',data)
        else:
            return HttpResponse('<h1>Fail To Update! Contact with SupportTeam</h1>')
    except:
        return HttpResponse('<h1>Some Error Occured ! Please Retry</h1>')


    return render(request,'seller/editrecord.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
@csrf_protect
@never_cache
def picupdate(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    try:
        id= request.GET.get('q') ###Just a api
        product=ProductData.objects.get(id=int(id))
        if product.seller_id==SellerProfile.objects.get(user_id=request.user.id).id:
            if request.method=='POST'  and request.FILES['photo']:
                name=request.POST.get('name')
                photo = request.FILES['photo']
                fs = FileSystemStorage(location='media/shop/product/')
                filename = fs.save(photo.name, photo)
                photoname=fs.generate_filename(filename)
                product.photo='shop/product/'+photoname
                product.save()
                data['message']='''<div class="alert alert-success" role="alert">
            Picture Updated Successfully</div>'''
                data['allproducts']=ProductData.objects.filter(seller_id=SellerProfile.objects.get(user_id=request.user.id).id).order_by('id')
                return render(request,'seller/update.html',data)
            else:
                data['name']=product.name
                data['picurl']=product.photo
                return render(request,'seller/picupdate.html',data)
        else:
            return HttpResponse('<h1>Fail To Update! Contact with SupportTeam</h1>')
    except:
        return HttpResponse('<h1>Some Error Occured ! Please Retry</h1>')
    return render(request,'seller/picupdate.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def editseller(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        request.user.name=name
        request.user.email=email
        request.user.save()
        data['name']=request.user.name
        data['phone']=request.user.phoneno
        data['email']=request.user.email
        data['message']='''<div class="alert alert-success" role="alert">
            Account Updated Successfully</div>'''
        return render(request,'seller/sellerconfig.html',data)
    else:
        data['name']=request.user.name
        data['phone']=request.user.phoneno
        data['email']=request.user.email
        return render(request,'seller/sellerconfig.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
@csrf_protect
@never_cache
def editshop(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    if request.method=='POST':
        if  request.FILES :
            photo = request.FILES['photo']
            fs = FileSystemStorage(location='media/shop/banner/')
            filename = fs.save(photo.name, photo)
            photoname=fs.generate_filename(filename)
        else:
            photoname= ""
        shopname=request.POST.get('name')
        shopaddress=request.POST.get('shopaddress')
        shoplatitude=request.POST.get('latitude')
        shoplongitude=request.POST.get('longitude')
        profile=request.user.seller
        profile.shopname=shopname
        profile.shopaddress=shopaddress
        profile.shoplatitude=shoplatitude
        profile.shoplongitude=shoplongitude
        if photoname == "":
            pass
        else:
            profile.shopbanner='shop/banner/'+photoname
        profile.save()
        return redirect('/seller/editshop')

    else:
        data['name']=request.user.seller.shopname
        data['shopbanner']=request.user.seller.shopbanner
        data['address']=request.user.seller.shopaddress
        data['longitude']=request.user.seller.shoplongitude
        data['latitude']=request.user.seller.shoplatitude
        return render(request,'seller/editshop.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def deliveryconfig(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    if request.method=='POST':
        deliverycharge=request.POST.get('deliverycharge')
        minprice=request.POST.get('minprice')
        homedelivery=request.POST.get('homedelivery')
        freedelivery=request.POST.get('freedelivery')
        seller=request.user.seller
        seller.deliverycharge=deliverycharge
        seller.minpriceforfreedelivery=minprice
        seller.homedelivery=homedelivery
        seller.freedelivery=freedelivery
        seller.save()
        return redirect('/seller/deliveryconfig')
    else:
        data['deliverycharge']=request.user.seller.deliverycharge
        data['minprice']=request.user.seller.minpriceforfreedelivery
        data['homedelivery']=request.user.seller.homedelivery
        data['freedelivery']=request.user.seller.freedelivery
        data['pincodes']= str(request.user.seller.shoppincodes)
    return render(request,'seller/deliveryconfig.html',data)

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def deletepincode(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    try:
        pincode=request.GET.get('q')
        profile=request.user.seller
        dbpincodes=profile.shoppincodes
        dbpincodes=eval(dbpincodes)
        dbpincodes.remove(int(pincode))
        profile.shoppincodes=dbpincodes
        profile.save()
        return redirect('/seller/deliveryconfig')
    except:
        return HttpResponse('<h1>Some Error Occured ! Contact With Webmaster </h1>')



@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def addpincode(request):
    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }
    try:
        pincode=request.GET.get('q')
        profile=request.user.seller
        dbpincodes=profile.shoppincodes
        dbpincodes=eval(dbpincodes)
        dbpincodes.append(int(pincode))
        profile.shoppincodes=dbpincodes
        profile.save()
        return redirect('/seller/deliveryconfig')
    except:
        return HttpResponse('<h1>Some Error Occured ! Contact With Webmaster </h1>')

@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def updatestatus(request):
    try:
        q= request.GET.get('q') ###Just a api
        choice=request.GET.get('choice')
        order=OrderHistory.objects.get(id=int(q))
        if int(order.sellerid)==int(request.user.seller.user_id):
            if int(choice)==2:
                order.status='cancelled'
            elif int(choice)==1:
                order.status='delivered'
            order.save()
            return redirect('/seller/pending')
        else:
            return HttpResponse('<h1>Fail To Delete! Contact with SupportTeam</h1>')
    except:
        return HttpResponse('<h1>Some Error Occured ! Please Retry</h1>')

# 11 th July Update
@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def changeallindiastatus(request):
    sellerpro=SellerProfile.objects.get(user_id=request.user.id)
    print(sellerpro)
    if int(sellerpro.allindia)==1:
        sellerpro.allindia=0
        sellerpro.save()
    elif int(sellerpro.allindia)==0:
        sellerpro.allindia=1
        sellerpro.save()
    return redirect('/seller/deliveryconfig')

#Show order data
@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def showorderdata(request,idd):
    data={
        'title':'Order Details',
        'MEDIA_URL':MEDIA_URL,
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id))
    }

    try:
        data['product']=OrderHistory.objects.filter(sellerid=request.user.id).get(id=idd)
        return render(request,'seller/orderdata.html',data)
    except:
        return redirect('/seller/pending')        

# 8-august-2020
@login_required(login_url='/account/sellerlogin?next={{request.path}}')
@seller_required
def cancelledorders(request):

    data={
        'title':'Dashboard',
        'MEDIA_URL':MEDIA_URL,
        'pendingordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='pending')),
        'deliveredordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='delivered')),
        'cancelledordersnumber':len(OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled')),
        'totalorders':len(OrderHistory.objects.filter(sellerid=request.user.id)),
        'cancelledorder':OrderHistory.objects.filter(sellerid=request.user.id).filter(status='cancelled').order_by('-orderedon')
    
    }
    return render(request,'seller/cancelledorders.html',data)

# end 8-august-2020