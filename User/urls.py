from django.urls import path
from User import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home),
    path('ShowProduct/<cid>', views.ShowProduct),
    path('SignUp', views.SignUp),
    path('Login', views.Login),
    path('Logout', views.Logout),
    path('alertPage',views.alertPage),
    path('ViewDetails/<product_id>', views.ViewDetails),
    path('AddToCart',views.AddToCart),
    path('ShowAllCartItems',views.ShowAllCartItems),
    path('Makepayment',views.Makepayment),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)