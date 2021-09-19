from django.core.files.storage import FileSystemStorage
from datamanagement.models import OrderHistory, ProductData, FCMTokenDirectory
from seller.models import SellerProfile
from buyer.models import BuyerProfile
from accounts.models import CustomUser
from .serializers import PendingOrderHistoryDataSerializers, ProductDataSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from importlib import import_module
from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend


class PendingOrders(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, request):
        objects = OrderHistory.objects.filter(sellerid=request.user.id).filter(Q(status='pending') | Q(status='packed'))
        main_data = []
        for i in objects:
            orderdata = {}
            customer = CustomUser.objects.get(id=BuyerProfile.objects.get(id=i.buyer_id).user_id)
            orderdata['orderid'] = i.id
            orderdata['name'] = customer.name
            orderdata['mobilenumber'] = customer.phoneno
            y = json.loads(customer.buyer.address)
            for k in y["address"]:
                if int(k["id"]) == i.address:
                    orderdata['address'] = k["address"]
                    break
            orderdata['status'] = i.status
            orderdata['orderedon'] = i.orderedon
            orders = []
            cartdata = json.loads(i.details)["cart"]
            print(cartdata)
            for j in cartdata:
                product = ProductData.objects.get(id=int(j['id']))
                tmp = {
                	"productid":j['id'],
                    "name": product.name,
                    "quantity": j['quantity'],
                    "price": j['price']*j['quantity']
                }
                orders.append(tmp)
            orderdata['details'] = orders
            main_data.append(orderdata)
        return main_data

    def get(self, request):
        if request.user.userflag:
            data = self.get_object(request)
            # serializer = PendingOrderHistoryDataSerializers(data, many=True)
            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class PendingOrdersDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, request, idd):
        try:
            return OrderHistory.objects.filter(sellerid=request.user.id).filter(
                Q(status='pending') | Q(status='packed')).get(id=idd)
        except OrderHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        if request.user.userflag:
            data = self.get_object(request, id)
            try:
                serializer = PendingOrderHistoryDataSerializers(data)
                return Response(serializer.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id):
        if request.user.userflag:
            data = self.get_object(request, id)
            try:
                serializer = PendingOrderHistoryDataSerializers(data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class BuyerDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, addressid):
        if request.user.userflag:
            try:
                customuserid = BuyerProfile.objects.get(id=int(pk)).user_id
                tmp = CustomUser.objects.get(id=int(customuserid))
                y = json.loads(tmp.buyer.address)
                z = ""
                k = ""
                for i in y["address"]:
                    if int(i["id"]) == int(addressid):
                        k = i['address']
                        z = i["pincode"]
                        break
                data = {
                    'name': tmp.name,
                    'phoneno': tmp.phoneno,
                    'email': tmp.email,
                    'address': k,
                    'poncode': z
                }
                return JsonResponse(data, status=status.HTTP_302_FOUND)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AddProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.userflag:
            try:
                photo = request.FILES['file']
                fs = FileSystemStorage(location='media/shop/product/')
                photoname = photo.name.replace(" ", "")
                photoname = photoname.replace("_", "")
                filename = fs.save(photoname, photo)
                photoname = fs.generate_filename(filename)
                name = request.POST.get('name')
                origin = request.POST.get('origin')
                details = request.POST.get('details')
                mrp = request.POST.get('mrp')
                discount = request.POST.get('discount')
                subcategory = request.POST.get('subcategory')
                available = request.POST.get('available')

                newproduct = ProductData.objects.create(
                    name=name,
                    details=details,
                    price=mrp,
                    originofproduct=origin,
                    available=available,
                    review=5,
                    discount=discount,
                    subcategory=subcategory,
                    photo='shop/product/' + photoname,
                    seller_id=SellerProfile.objects.get(user_id=request.user.id).id
                )
                newproduct.save()
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProductDataAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_data(self, id):
        try:
            return ProductData.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        if request.user.userflag and ProductData.objects.get(id=id).seller_id == request.user.seller.id:
            serailizer = ProductDataSerializer(self.get_data(id))
            return Response(serailizer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, id):
        if request.user.userflag and ProductData.objects.get(id=id).seller_id == request.user.seller.id:
            data = self.get_data(id)
            try:
                serializer = ProductDataSerializer(data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@require_http_methods(["POST"])
@csrf_exempt
def registerFCM(request):
    try:
        session_key = request.POST["SESSION_KEY"]
        fcm_token = request.POST["FCM_TOKEN"]
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore(session_key)

        try:
            user_id = session[SESSION_KEY]
            backend_path = session[BACKEND_SESSION_KEY]
            backend = load_backend(backend_path)
            user = backend.get_user(user_id) or AnonymousUser()
        except KeyError:
            user = AnonymousUser()


        if user.is_authenticated:
            if not FCMTokenDirectory.objects.filter(phoneNo = user.phoneno,fcmtoken = fcm_token).exists():
                FCMTokenDirectory.objects.create(
                    phoneNo = user.phoneno,
                    fcmtoken = fcm_token
                )
            return HttpResponse("OK")
        else : return HttpResponse("Not authorized")

    except :
        return HttpResponse("ERROR")