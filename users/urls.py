from django.urls import include, path

from .views import YourAPIView,SignUp,Login

urlpatterns = [
    path('your-view/', YourAPIView.as_view(), name='your-view'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    # Define other URL patterns for the users app here
]