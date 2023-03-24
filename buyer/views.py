import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from random import randrange
from django.conf import settings
from seller.models import *

# Create your views here.

def index(request):
    all_pros = product.objects.all()
    try:
        buyer_row =Buyer.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'user_data':buyer_row, 'all_products':all_pros})
    except:
        return render(request, 'index.html',{'all_products': all_pros})


def about(request):
    try:
        buyer_row =Buyer.objects.get(email = request.session['email'])
        return render(request, 'about.html', {'user_data': buyer_row})
    except:
        return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')

def menu(request):
    return render( request, 'menu.html')

def reservation(request):
    return render(request, 'reservation.html')

def service(request):
    return render(request, 'service.html')

def testimonial(request):
    return render(request, 'testimonial.html')


def add_row(request):
    Buyer.objects.create(
        first_name ='yogesh',
        last_name = 'gaykwad',
        email = 'yogesh@gamil.com',
        password = 'yogesh@1253',
        address = '125, mhakalpada, gholar',
        mobile = '9624358648',
        gender = 'male'
    )
    return HttpResponse('row create thai gai')
    
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'msg': 'Email Is Already registered!!'})
        except:
            if request.POST['password'] == request.POST['repassword']:
                s = "Ecommerce Registration!!"
                global user_data
                user_data = [request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password']]
                global c_otp
                c_otp = randrange(1000,9999)
                m = f'Hello User!!\nYour OTP is {c_otp}'
                f = settings.EMAIL_HOST_USER
                r = [request.POST['email']]
                send_mail(s, m, f, r)
                return render(request, 'otp.html', {'msg': 'Check Your MailBox'})
            else:
                return render(request, 'register.html', {'msg': 'Both Passwords do not match!!'})


def otp(request):
    
        if str(c_otp) == request.POST['u_otp']:
            Buyer.objects.create(
                first_name = user_data[0],
                last_name = user_data[1],
                email = user_data[2],
                password = user_data[3]
            )
            return render(request, 'register.html', {'msg': 'Account created successfully!!'})
        else:
            return render(request, 'otp.html', {'msg': 'Wrong OTP enter again!!'})
        

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
        
            buyer_row = Buyer.objects.get(email = request.POST['email'])
            
            if request.POST['password'] == buyer_row.password:
                
                request.session['email'] = request.POST['email'] 
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': 'Wrong Password!!'})
            
        except:
            
            return render(request, 'login.html',{'msg':'email is not registered!!'})

def logout(request):
    del request.session['email']
    return redirect('index')



def cart(request):
    u1 = Buyer.objects.get(email = request.session['email'])
    global c_list
    c_list = Cart.objects.filter(buyer = u1)
    global t_amount
    t_amount = 0
    for i in c_list:
       t_amount += i.price

    # pyment nu button jivit krva mateno no code
    currency = 'INR'
    #print(t_amount * 100)
    amount =  t_amount * 100 # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context.update({'user_data' : u1, 'my_cart_data': c_list, 'total_amount':t_amount})
    

    return render(request, 'cart.html', context=context)



def add_to_cart(requestr, pk):
    p_obj = product.objects.get(id = pk)
    b1 = Buyer.objects.get(email = requestr.session['email'])
    Cart.objects.create(
        product_name = p_obj.product_name,
        price = p_obj.price,
        pic = p_obj.pic,
        buyer = b1 
    )
    return redirect('index')


def del_cart_item(reuqest, c_item):
    c_obj = Cart.objects.get(id = c_item)
    c_obj.delete()
    return redirect('cart')

     



# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt

def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = t_amount  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    # if i in c_list:
                        # i.delete()
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
