from django.shortcuts import render, redirect
from django.http import HttpResponse
from Admin.models import Category, Product
from User.models import Payment, UserInfo, MyCart, Payment, Order_Master
from datetime import datetime
from django.contrib import messages



    
def home(request):
    cats = Category.objects.all() #to show all ctatagory name in drapdown
    products = Product.objects.all()
    return render(request,"home.html",{"cats":cats,"products":products})



def ShowProduct(request,cid):  #the product available in  cid (category_id)
    cats = Category.objects.all()
    products = Product.objects.filter(cat_id = cid)
    return render(request,"home.html",{"cats":cats,"products":products})




def SignUp(request):
    if(request.method=="GET"):
        return render(request,"SignUp.html",{})
        
    else:
        u1 = UserInfo()
        u1.username = request.POST["uname"]
        u1.password = request.POST["pwd"]
        u1.save()
        messages.error(request,"You are already register with us please LogIn with ID and Password")
        
        return redirect(alertPage)



def Login(request):
    if(request.method=="GET"):
        cats = Category.objects.all()
        return render(request,"Login.html",{"cats":cats}) 
    else:
        username = request.POST["uname"]
        password = request.POST["pwd"]
        try:
            u1 = UserInfo.objects.get(username=username,password=password)
            #Create session
            request.session["uname"] = username 
            return redirect(home)
                     
        except:
            messages.error(request,"You are a new user, Please Sign Up First!!!")

            return redirect(SignUp)




def Logout(request):
    request.session.clear()
    return redirect(home)



def ViewDetails(request,product_id):  # through this only one product comes
    cats = Category.objects.all()
    p1 = Product.objects.get(id=product_id)
    return render(request,"ViewDetails.html",{"product":p1, "cats":cats})



def alertPage(request):
    cats = Category.objects.all()
    return render(request,"Alert.html",{"cats":cats})




def AddToCart(request):
    if("uname" in request.session):
       #Add to cart is applicable only thoes who has log in currently that's why check if session is created or not
        u1 = UserInfo.objects.get(username=request.session["uname"])  #this the data which we store in cart
        p1 = Product.objects.get(id=request.POST["productid"])
        qty = request.POST["qty"]

        try:
            #to check is a user add same product  again if yes then we goes directly home without adding again
            item = MyCart.objects.get(user=u1,Product=p1)
            messages.error(request,"Item already in cart")
            
        except:
            #if user add new product then we will accept and stored in MyCart database
            cart = MyCart()
            cart.user = u1
            cart.Product=p1
            cart.qty = qty
            cart.save()
            #return HttpResponse("Added in the cart")
            messages.success(request,"Item added successfully to cart!!") 
        
        return redirect(alertPage)
    else:
        
        return redirect(Login)





def ShowAllCartItems(request): #this data fetch from MyCart , the user get loged in page
    if(request.method=="GET"):

        if("uname" in request.session):
            cats = Category.objects.all()
            items = MyCart.objects.filter(user = request.session["uname"])

            total = 0
            for item in items:
                total += item.qty * item.Product.price
            #print(total)
            request.session["total"] = total
            return render(request,"ShowAllCartItems.html",{"items": items,"cats":cats})
        else:
            return redirect(Login)
    else:
        action = request.POST["action"]
        productid= request.POST["Product_id"]
        items = MyCart.objects.get(user = request.session["uname"],Product = Product.objects.get(id=productid))
        if(action=="Update"):
            qty = request.POST["item_qty"]
            
            items.qty = qty
            items.save()
            
        else:
            items.delete()
        return redirect(ShowAllCartItems)




def Makepayment(request):
    if(request.method=="GET"):
        cats = Category.objects.all()
        return render(request, "CardDetails.html",{"cats":cats})

    else:
        # Buyer
        uname = request.POST["uname"]
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        
        try:
            #Payment done 
            buyer = Payment.objects.get(uname=uname,card_no=cardno,cvv=cvv,expiry=expiry)
            owner = Payment.objects.get(uname='Shop Owner',card_no="4444333322221111",cvv="856",expiry="07/2026")
            amount = float(request.session["total"])
            # to check account balence is Greater or low than the product price
            if (buyer.balance> amount):  
                buyer.balance -= amount
            else:
                messages.error(request,"Sorry!!! Your account balence is low")
            owner.balance += amount

            buyer.save()
            owner.save()

            #Update Order_Master(this is data base which stored our history) and delete from MyCart(and all cart items release afert done payment)

            items = MyCart.objects.filter(user = request.session["uname"])
            prd_details = []

            for item in items:
                prd_details.append(item.Product.product_name)  # List of all cart items

            o1 = Order_Master()
            o1.username = request.session["uname"]
            o1.date_Of_Oreder = datetime.now()
            o1.amount = float(request.session["total"])
            o1.product_details = ",".join(prd_details) #list joining
            o1.save()
            print(o1)
            for item in items:   #delete cart items
                item.delete()

            #return HttpResponse("Payment Successful !!!")
            messages.success(request,"Payment Successfull !!!") 
        except:            
            messages.error(request,"Invalide Details!!!")
        return redirect(alertPage)
        