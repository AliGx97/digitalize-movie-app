from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja.responses import codes_4xx
from pydantic import EmailStr, Field
import requests
from account.authorization import PasswordResetTokenAuthentication
from account.models import Otp
from account.schemas import AccountCreateBody, AccountOut, AccountLoginBody, PasswordResetToken, PasswordSchema, OtpIn, \
    AccountUpdate, AccountInfo
from account.authorization import TokenAuthentication, get_tokens_for_user
from django.contrib.auth import get_user_model, authenticate
from ninja import Router, File
from ninja.files import UploadedFile
from utils.schemas import MessageOut
from django.core.mail import EmailMessage
from django.conf import settings

User = get_user_model()

account_controller = Router(tags=['Accounts'])


@account_controller.post('/signup', response={201: MessageOut, 400: MessageOut})
def register_user(request, payload: AccountCreateBody, image: UploadedFile = File(None)):
    if payload.password1 != payload.password2:
        return 400, {'msg': 'Passwords didn\'t match'}
    try:
        user = User.objects.get(email__iexact=payload.email)
        return 400, {'msg': 'Email is already used'}
    except User.DoesNotExist:
        user = User.objects.create_user(
            name=payload.name, email=payload.email, password=payload.password1
        )
        if image:
            res = requests.post(
                url=settings.IMGBB_URL,
                files={'image': image.read()},
                params={'key': settings.IMGBB_KEY}
            )
            if res.ok:
                data = res.json()['data']
                image_url = data['url']
                user.profile = image_url
                user.save()
        otp = Otp.objects.create(user=user)
        email_to_send = EmailMessage(
            subject='Your OTP code',
            body=f'This is your OTP code attached\n {otp.number}',
            from_email=settings.EMAIL_HOST_USER,
            to=[payload.email],
        )
        email_to_send.send(fail_silently=True)
        return 201, {'msg': "User created successfully"}


@account_controller.post('/verify', response={200: MessageOut, codes_4xx: MessageOut})
def verify_user(request, email: EmailStr, otp: int):
    try:
        user = User.objects.get(email=email)
        user_otp = Otp.objects.get(user=user)
        if otp == user_otp.number:
            user_otp.delete()
            user.is_verified = True
            user.save()
            return 200, {'msg': 'User verified sucessfully'}
        else:
            return 404, {'msg': 'Otp was no match'}
    except User.DoesNotExist:
        return 404, {'msg': 'User was not found with that email'}


@account_controller.post('/login', response={200: AccountOut, codes_4xx: MessageOut})
def login_user(request, paylod: AccountLoginBody):
    user = authenticate(email=paylod.email, password=paylod.password)
    if not user:
        return 404, {'msg': 'Email or password are incorrect, please try again'}
    if not user.is_verified:
        otp = Otp.objects.create(user=user)
        mail_to_send = EmailMessage(
            subject='Password Reset',
            body=f"Your password reset otp is: {otp.number}",
            to=[user.email, ]
        )
        mail_to_send.send(fail_silently=True)
        return 403, {'msg': 'Please Verify your account'}
    token = get_tokens_for_user(user)
    print(token)
    return 200, {
        'token': token,
        'user': user
    }


@account_controller.get('/forget-password', response={200: MessageOut, codes_4xx: MessageOut})
def password_reset_email(request, email: EmailStr):
    try:
        user = User.objects.get(email__iexact=email)
        otp = Otp.objects.create(user=user)
        mail_to_send = EmailMessage(
            subject='Password Reset',
            body=f"Your password reset otp is: {otp.number}",
            to=[user.email, ]
        )
        mail_to_send.send(fail_silently=True)
        return 200, {'msg': 'Otp sent to your email'}
    except User.DoesNotExist:
        return 404, {'msg': 'There is no user with that email address'}


@account_controller.post('/forget-passord/otp', response={200: PasswordResetToken, codes_4xx: MessageOut})
def receive_password_reset_otp(request, email: EmailStr, payload: OtpIn):
    try:
        user = User.objects.get(email__iexact=email)
        user_otp = Otp.objects.get(user=user)
        if payload.otp != user_otp.number:
            return 404, {'msg': 'The otp is not correct'}
        token = get_tokens_for_user(user, password_reset=True)
        return 200, {'token': token}
    except User.DoesNotExist:
        return 404, {'msg': 'There is no such user'}


@account_controller.post('/forget-passord', auth=PasswordResetTokenAuthentication(), response={
    200: AccountOut,
    codes_4xx: MessageOut
})
def change_password(request, payload: PasswordSchema):
    if payload.password1 != payload.password2:
        return 400, {'msg': 'Passwords didn\'t match'}

    user = User.objects.get(id=request.auth['id'])
    user.set_password(payload.password1)
    user.save()
    Otp.objects.get(user=user).delete()
    token = get_tokens_for_user(user)
    return 200, {
        'token': token,
        'user': user
    }


@account_controller.get('/me', auth=TokenAuthentication(), response={200: AccountInfo})
def get_user_info(request):
    user = get_object_or_404(User, id=request.auth['id'])
    return user


@account_controller.put('/me', auth=TokenAuthentication(), response={200: MessageOut})
def update_user_info(request, payload: AccountUpdate):
    user = User.objects.get(id=request.auth['id'])
    if payload.name:
        user.name = payload.name
    if payload.gender in ['Male', 'Female']:
        user.gender = payload.gender
    if payload.birth_date:
        user.birth_date = payload.birth_date
    if payload.phone:
        user.phone = payload.phone
    user.save()
    return 200, {'msg': 'Information updated successfully.'}
