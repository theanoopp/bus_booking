"""bus_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', views.UserCreateAPIView.as_view(), name='Register'),
    path('api/login/', views.UserLoginAPIView.as_view(), name='Login'),
    path('users/update/<pk>', views.UserUpdate.as_view()),
    path('api/users/', views.UserList.as_view()),
    path('api/users/current/', views.CurrentUserView.as_view()),
    path('api/users/check/', views.CheckEmail.as_view()),
    path('users/delete/<pk>', views.UserDelete.as_view()),

    path('users/<pk>', views.UserDetail.as_view()),


    path('internal/link/', views.GetBusInfo.as_view()),#
    path('internal/getSeatInfo/', views.GetBusSeatInfo.as_view()),#
    path('internal/getBusById/', views.GetBusById.as_view()),#
    path('internal/getUpdatedFare/', views.getRTCUpdatedFare.as_view()),#
    path('internal/blockTicket/', views.blockBusSeat.as_view()),#
    path('internal/seatBooking/', views.seatBooking.as_view()),#
    path('internal/getTicket/', views.getTicketByETSTNumber.as_view()),#
    path('internal/cancelTicketConfirmation/', views.CancelTicketConfirmation.as_view()),
    path('internal/cancelTicket/', views.CancelTicket.as_view()),

]
