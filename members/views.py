import json
import razorpay
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Register, Member, Mysqltable, Products, Cart, orders
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

RAZORPAY_KEY_ID = "rzp_test_VWmICmsgQhaxjk"
RAZORPAY_KEY_SECRET = "8mnVhktk5mOO0RaxALnBKaJK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def orderpay(request):
    #sending the details to page of product and amount
    name = request.session.get('name')
    items = None
    if name:
        try:
            items = Cart.objects.filter(user_name=name)
            total = sum(item.price for item in items)
        except Cart.DoesNotExist:
            items = None
    #sending the details to the page of order details
    amount = total * 100
    currency = 'INR'
    receipt = f'order_receipt_{datetime.now().timestamp()}'

    order = client.order.create({
            'amount':amount,
            'currency': currency,
            'receipt':receipt,
        })

    call_back_url = 'verify_payment/'

    new_order = orders(order_id = order['id'], amount = total, currency = currency, receipt = receipt, status = 'created')
    new_order.save()

    return render(request,'purchase.html',{'order_id':order['id'],
                                           'razor_key_id':RAZORPAY_KEY_ID,
                                           'amount':amount,
                                           'callbackurl':call_back_url,
                                           'item':items, 
                                           'total_amount':total}
                                           )

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('razorpay_order_id')
            payment_id = request.POST.get('razorpay_payment_id')
            signature = request.POST.get('razorpay_signature')

            dict = {
                'razorpay_order_id':order_id,
                'razorpay_payment_id':payment_id,
                'razorpay_signature':signature
            }

            client.utility.verify_payment_signature(dict)

            order = orders.objects.get(order_id = order_id)
            order.status = 'Paid'
            order.payment_id = payment_id
            order.save()

            client.payment.capture(payment_id, order.amount * 100)

            name = request.session.get('name')
            if name:
                Cart.objects.filter(user_name=name).delete()

            return redirect('success')

        except:
            return redirect('failure')
        
def success(request):
    return render(request, 'success.html')

def failure(request):
    return render(request, 'failure.html')

def members(request):
    return HttpResponse("Hello world!")

def index(request):
    detail = Mysqltable.objects.all()
    return render(request, 'index.html', {'detail': detail})

def main(request):
    d = Products.objects.all()
    name = request.session.get('name', 'Guest')
    return render(request, 'main.html',{'detail':d,'n':name})

def forms(request):
    m = ''
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        repassword = request.POST.get('repassword','')
        if name and email and password and repassword:
            mail = Mysqltable.objects.filter(email = email).exists()
            if not mail:
                if password == repassword:
                    r = Mysqltable(name = name,email = email, password = make_password(password))
                    r.save()
                    m = 'Registered succesfully'
                    #return redirect('login')
                else:
                    m = 'Password should be same'
            else:
                m = 'Email already Registered'
        else:
            m = 'Please Enter All the Values.'
    return render(request, 'forms.html', {'message':m})

def login(request):
    m = ''
    if request.method == 'POST':
        mail = request.POST.get('email','')
        passwd = request.POST.get('password','')

        if mail and passwd:
            if Mysqltable.objects.filter(email = mail).exists():

                detail = Mysqltable.objects.get(email = mail)
                if check_password(passwd, detail.password):
                    request.session['name'] = detail.name
                    return redirect('main')
                else:
                    m = 'Password is incorrect'
            else:
                m = 'Email does not exist. Please register'
        else:
            m = 'Please Enter The Email/Password'

    return render(request, 'login.html', {'message':m})

def forgotpass(request):
    m = ''
    if request.method == 'POST':
        mail = request.POST.get('mail','')
        oldpassword = request.POST.get('opasswd','')
        newpassword = request.POST.get('npasswd','')
        if mail and oldpassword and newpassword:
            if Mysqltable.objects.filter(email = mail).exists():
                detail = Mysqltable.objects.get(email = mail)
                if check_password(oldpassword, detail.password):
                    if oldpassword != newpassword:
                        detail.password = make_password(newpassword)
                        detail.save()
                        m = 'Password Changed Successfully'
                        return render(request, 'login.html', {'message':m})
                    else:
                        m = 'Password Cant be same as old password'
                else:
                    m = 'Old Password Is Wrong. Please Enter An Right Password'
            else:
                m = 'Email Doesnt Exist.Please Register'
        else:
            m = 'Please Enter All The Field.'
    return render(request, 'forgot.html',{'message':m})

def add_to_cart(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        product_id = data.get('product_id')
        username = request.session.get('name', '') 
        
        if username :
            dat = Products.objects.get(id = product_id)
            item = Cart.objects.filter(user_name=username, product_name=dat.name).first()
            if item:
                item.quantity += 1
                item.price += dat.price
                item.save()
            else:
                r = Cart(user_name = username, product_name = dat.name, price = dat.price, quantity=1, status='Pending')
                r.save()
            return JsonResponse({'message': f'{dat.name} has been added to your cart.'})
        else:
            return JsonResponse({'error': 'Please log in to add items to your cart.'})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def cart(request):
    name = request.session.get('name','')
    items = None 

    if name:
        items = Cart.objects.filter(user_name=name)

    return render(request, 'cart.html', {'task': items})

def logout(request):
    request.session.flush()  
    return redirect('login')

def update_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = request.session.get('name') 
        product_name = data['id']  
        action = data['action']

        item = Cart.objects.get(user_name=name, product_name=product_name)
        product = Products.objects.get(name=product_name)

        if action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
            item.price -= product.price
        elif action == 'increase':
            item.quantity += 1
            item.price += product.price

        item.save()

        return JsonResponse({
            'new_quantity': item.quantity,
            'new_price': item.price,
        })
    
def delete_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = request.session.get('name')
        product_name = data['id']

        Cart.objects.filter(user_name=name, product_name=product_name).delete()

        return JsonResponse({'success': True})
    
'''def purchase(request):
    name = request.session.get('name')
    items = None
    if name:
        try:
            items = Cart.objects.filter(user_name=name)
            total = sum(item.price for item in items)
        except Cart.DoesNotExist:
            items = None
    return render(request, 'purchase.html', {'item':items, 'total_amount':total})'''