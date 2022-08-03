# General imports
import json
import jwt
from django.utils import timezone
# Django Imports
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import  csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings
from datetime import datetime

# Django Rest Framework imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated


# Local imports
from .serializers import LoginSerializer, RegisterSerializer, ResetSetPasswordSerializer
from .tokens import generate_hybrid_token, generate_tokens
from .authentication import CustomTokenAuthentication, HybridAuthentication
from .utils import handle_sent_account_activation, send_account_activation_email, send_reset_password_email
from .models import User


# from json import jsonify
import stripe



@api_view(['POST'])
def create_customer(request):
    stripe.api_key = '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'
    customer = stripe.Customer.create(
        email="dutarares08@gmail.com",
        name="Pascalin Anamaria",
        shipping={
            "address": {
            "city": "Brothers",
            "country": "US",
            "line1": "27 Fredrick Ave",
            "postal_code": "97712",
            "state": "CA",
            },
            "name": "Rares Duta",
        },
        address={
            "city": "Brothers",
            "country": "US",
            "line1": "27 Fredrick Ave",
            "postal_code": "97712",
            "state": "CA",
        },
    )
    response = {
        "customer": customer['id']
    }
    return Response(response)


@api_view(['POST'])
def create_subscription(request):
    stripe.api_key = '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'

    customer_id = request.data['customerId']
    price_id = request.data['priceId']
    print("Create subscription called")
    print(customer_id, price_id)

    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )
        
        print("response on subscription,", subscription)
        response = {
            "subscriptionId":subscription.id, 
            "clientSecret": subscription.latest_invoice.payment_intent.client_secret
        }

        print("Raspuns la subscription ", response)
        return Response(response)


    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

   



@api_view(['POST'])
def for_payment(request):
    stripe.api_key = 'sk_test_51LQ6WDCFCYzaNOTCoxGgrm5vAWVmVZwGs3IZBhyAIAMxTMSsavVKW1imXERCLh25XSUYGUXSgAuo1UNOk2hyuxE300ArKRzHwj'
  # Use an existing Customer ID if this is a returning customer
    customer = stripe.Customer.create(email="raresduta08@gmail.com")

    print(customer)
    ephemeralKey = stripe.EphemeralKey.create(
        customer=customer['id'],
        stripe_version='2020-08-27',
    )
    paymentIntent = stripe.Subscription.create(
        customer=customer['id'],
        payment_behavior='allow_incomplete',
        items=[
            {"price": "price_1LSNZNCFCYzaNOTCucM3RBLy"},
        ]
    )
    # paymentIntent = stripe.PaymentIntent.create(
    #     amount=1099,
    #     currency='eur',
    #     customer=customer['id'],
    #     automatic_payment_methods={
    #         'enabled': True,
    #     },
    # )


    response ={
        "paymentIntent":paymentIntent.client_secret,
        "ephemeralKey": ephemeralKey.secret,
        "customer": customer.id,
        "publishableKey" :"pk_test_51LQ6WDCFCYzaNOTCPVcLWLSyHRNqMPzZmhRx7dIYyGyI0wSxMItNaGy27Zc0HUB3DlOQFG1uxUThK1w0C2Fb3Vy100G8amM7Wu"
    }
    # return jsonify(paymentIntent=paymentIntent.client_secret,
    #              ephemeralKey=ephemeralKey.secret,
    #              customer=customer.id,
    #              publishableKey='pk_test_51LQ6WDCFCYzaNOTCPVcLWLSyHRNqMPzZmhRx7dIYyGyI0wSxMItNaGy27Zc0HUB3DlOQFG1uxUThK1w0C2Fb3Vy100G8amM7Wu')


    return Response(response)
# 





@api_view(['GET'])
def get_csrf(request):
    response = Response({"message": "Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    return response



@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_obj = serializer.save()
    
    send_account_activation_email(request, user_obj)

    return handle_sent_account_activation(request, user_obj, from_register=True)




from rest_framework.authtoken.models import Token

# @api_view(['POST'])
# # @csrf_protect
# def login_view(request):

#     serializer = LoginSerializer(data=request.POST)
#     serializer.is_valid(raise_exception=True)
    
#     email = serializer.validated_data['email']
#     password = serializer.validated_data['password']

#     user = authenticate(email=email, password=password)
#     if user is not None:
#         if not user.is_confirmed:
#             return handle_sent_account_activation(request, user, from_register=False)

#         # token = Token.objects.create(user=user)
#         # print(token.key)

#         x_forwarded_for = request.META.get('REMOTE_ADDR')
#         print(x_forwarded_for)
#         return Response()
#     #     login(request, user)
#     #     hybrid_token = generate_hybrid_token(user)
#     #     if settings.UPDATE_LAST_LOGIN:
#     #         user.last_login = datetime.now()
#     #         user.save()
#     #     return Response({"is_authenticated": True, "hybrid_token":hybrid_token}, status=status.HTTP_200_OK)
#     # else:
#     #     return Response(status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def resend_account_activation_email(request):
    try:
        identify_user_token = request.POST.get('identify_user_token')
        identify_user_token_payload = jwt.decode(identify_user_token, settings.SECRET_KEY, algorithms=['HS256'])
 
        if not identify_user_token_payload['user_identifier_token']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user_id = identify_user_token_payload['user_id']
        user = User.objects.filter(id=user_id).first()
    
        if user is None or user.is_confirmed:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.last_confirm_account_sent is not None and user.last_confirm_account_sent > timezone.now() - settings.RESEND_ACCOUNT_ACTIVATION_EMAIL_TIMEOUT:
            return Response({"resent_success":False,"message":"Please wait " + str(settings.RESEND_ACCOUNT_ACTIVATION_EMAIL_TIMEOUT_NUMERIC) +" minutes before requesting a new activation email!"}, status=status.HTTP_200_OK)

        send_account_activation_email(request, user)
        return Response({"resent_success":True}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def activate_account_view(request):
    if str(request.user) != "AnonymousUser":
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    try:
        account_activation_token = request.POST.get('account_activation_token')
        account_activation_token_payload = jwt.decode(account_activation_token, settings.SECRET_KEY, algorithms=['HS256'])
        if not account_activation_token_payload['account_activation']:
            return Response({"activation_success":False}, status=status.HTTP_400_BAD_REQUEST)
 
        user_id = account_activation_token_payload['user_id']
        user = User.objects.filter(id = user_id)[0]
        
        if user is None or user.is_confirmed:
            return Response({"activation_success":False},status=status.HTTP_400_BAD_REQUEST)
        
        user.is_confirmed = True
        user.save()
        return Response({"activation_success":True},status=status.HTTP_202_ACCEPTED)
    
    except Exception as e:
        return Response({"activation_success":False}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def send_reset_password_email_view(request):

    if str(request.user) is not "AnonymousUser":
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"account_found":False,"sent_success":False}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.last_reset_password_sent is not None and user.last_reset_password_sent > timezone.now() - settings.RESENT_PASSWORD_RESET_EMAIL_TIMEOUT:
            return Response({"account_found":True,"sent_success":True}, status=status.HTTP_202_ACCEPTED)

        send_reset_password_email(request, user)
        return Response({"account_found":True,"sent_success":True}, status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# cand verificam token-ul de resetare a parolei
# sa vedem daca link-ul de resetare a parolei este valid
# adica o sa punem in el data si dupa data ne dam seama cu last password change

@api_view(['POST'])
def reset_set_new_password(request):
        serializer = ResetSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"reset_success":True},status=status.HTTP_200_OK)
    
    # try:
    #     # reset_password_token = request.POST.get('reset_password_token')
    #     # reset_password_token_payload = jwt.decode(reset_password_token, settings.SECRET_KEY, algorithms=['HS256'])

    #     # if not reset_password_token_payload['reset_password']:
    #     #     return Response(status=status.HTTP_400_BAD_REQUEST)
        
    #     # user_id = reset_password_token_payload['user_id']
    #     # user = User.objects.filter(id = user_id)[0]
    #     # if user is None:
    #     #     return Response(status=status.HTTP_400_BAD_REQUEST)
        
    #     # print(user)
    #     serializer = ResetSetPasswordSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     print(serializer.validated_data)

    #     # wait a second here we need also new password

    # except Exception as e:
    #     print(e)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)





# Login based on custom token

@api_view(['POST'])
@authentication_classes((CustomTokenAuthentication,))
def login_view(request):
    serializer = LoginSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = authenticate(email=email, password=password)
    if user is  None:
        return Response({"message": "Login Failed"}, status=status.HTTP_401_UNAUTHORIZED)

    tokens_pair = generate_tokens(user)

    response = {
        "access_token": tokens_pair['access_token'],
        "refresh_token": tokens_pair['refresh_token']
    }

    if settings.UPDATE_LAST_LOGIN:
        user.last_login = datetime.now()
        user.save()

    return Response(response, status=status.HTTP_200_OK)


# 
#  Problema aia cu confirmarea gen daca confirma dupa link ul tot e bun sa confirme in continuu
# when user is not authenticated AnonymousUser

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
# @csrf_protect
@authentication_classes((CustomTokenAuthentication,))
# @authentication_classes((HybridAuthentication,))
def session_test(request):
    # print(request.user)
    # token = generate_tokens(request.user)
    # print(token)

    # print(request.user.last_confirm_account_sent)
    # print(timezone.now())
    # print(datetime.now())

    print(request.user)
    # 
    return Response({"message":"Session test", "user":request.user.email})

@api_view(['POST'])
def refresh_token(request):
    try:
        old_token = request.data['refresh_token'] 
        payload = jwt.decode(old_token, settings.SECRET_KEY,  algorithms=['HS256'])
        user = User.objects.get(id = payload['user_id']) 

        token_pairs = user.get_tokens
        return Response(token_pairs)
        
    except Exception as e:
        return Response("Token not provided or invalid", status=status.HTTP_401_UNAUTHORIZED)




# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# @authentication_classes((HybridAuthentication,))
# def demo_auth(request):
#     return Response({"is_authenticated":"True", "user":request.user.email})




