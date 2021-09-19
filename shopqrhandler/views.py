from django.shortcuts import render,redirect
from .models import shopqrdata
from django.http import HttpResponse

def redirectt(request):
	return redirect('https://play.google.com/store/apps/details?id=buyer.com.localbazer')
    # try: 
    #     q=request.GET['q']
    #     print(q)
    #     idd=shopqrdata.objects.get(qrdata=q).shopid
    #     return redirect('https://play.google.com/store/apps/details?id=buyer.com.localbazer')
    #     # return redirect('/shoppage?q={}'.format(idd))
    # except:
    #     return HttpResponse("<h1>No shops registered yet</h1>")

def register(request):
    if request.method =='GET':
        barid= request.GET['barid']
        shopid=request.GET['shopid']
        shopqrdata.objects.create(
            qrdata=barid,
            shopid=int(shopid)
        )
        return HttpResponse('Done')
    return HttpResponse('ERROR')
