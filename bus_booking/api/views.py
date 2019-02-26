from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer, UserCreateSerializer

from django.contrib.auth.models import User
from .models import TravellerDetails, TicketDetails
from requests.auth import HTTPDigestAuth
import json

import requests
import urllib3
from base64 import encode

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView
)

url = "http://test.etravelsmart.com/etsAPI/api/"


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserList(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDelete(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CheckEmail(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            return Response("Not available", status=status.HTTP_200_OK)
        return Response("Available", status=status.HTTP_200_OK)


# APIView for user login
class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.error, status.HTTP_400_BAD_REQUEST)


class GetBusInfo(APIView):
    def get(self, request, *args, **kwargs):
        source = self.request.query_params.get('from')
        destination = self.request.query_params.get('to')
        date = self.request.query_params.get('Doj')

        get_bus_url = url + "getAvailableBuses?sourceCity=" + source + "&destinationCity=" + destination + "&doj=" + date

        response = requests.get(get_bus_url, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)

        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)


class GetBusById(APIView):
    def get(self, request, *args, **kwargs):
        source = self.request.query_params.get('sourceCity')
        destination = self.request.query_params.get('destinationCity')
        dateOfJour = self.request.query_params.get('doj')
        routeScheduledId = self.request.query_params.get('routeScheduleId')

        get_bus_by_id = url + "getAvailableBuses?sourceCity=" + source + "&destinationCity=" + destination + "&doj=" + dateOfJour

        response = requests.get(get_bus_by_id, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)

        json_data = json.loads(response.text)

        json_array = json_data['apiAvailableBuses']

        my_list = []

        for d in json_array:
            b_id = d['routeScheduleId']
            if routeScheduledId == b_id:
                my_list.append(d)

        json_data = json.dumps(my_list)

        json_data = json.loads(json_data)

        return Response(json_data, status=status.HTTP_200_OK)


class GetBusSeatInfo(APIView):
    def get(self, request, *args, **kwargs):
        source = self.request.query_params.get('sourceCity')
        destination = self.request.query_params.get('destinationCity')
        dateOfJour = self.request.query_params.get('doj')
        inventory = self.request.query_params.get('inventoryType')
        routeScheduledId = self.request.query_params.get('routeScheduleId')

        get_seat_info = url + "getBusLayout?sourceCity=" + source + "&destinationCity=" + destination + "&doj=" + dateOfJour + "&inventoryType=" + inventory + "&routeScheduleId=" + routeScheduledId

        response = requests.get(get_seat_info, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)

        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)


class getRTCUpdatedFare(APIView):
    def get(self, request, *args, **kwargs):
        blockticket_key = self.request.query_params.get('blockTicketKey')

        get_rtc_url = url + "getRtcUpdatedFare?blockTicketKey=" + blockticket_key

        response = requests.get(get_rtc_url, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)

        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)


class blockBusSeat(APIView):
    def post(self, request, *args, **kwargs):
        # source = request.data["sourceCity"]
        # destin = request.data["destinationCity"]
        # date = request.data["doj"]
        # custName = request.data["customerName"]
        # custLastName = request.data["customerLastName"]
        # custEmail = request.data["customerEmail"]
        # custPhone = request.data["customerPhone"]
        # emergencyPhNum = request.data["emergencyPhNumber"]
        # custAddrss = request.data["customerAddress"]
        # inventory = request.data["inventoryType"]
        # routeId = request.data["routeScheduleId"]
        #
        # # boarding point details
        # baseBoarding = request.data["boardingPoint"]
        # boardId = baseBoarding["id"]
        # location = baseBoarding["location"]
        # time = baseBoarding["time"]
        #
        # # dropping point details
        #
        # baseDropping = request.data["droppingPoint"]
        #
        # dropId = None
        # dropLocation = None
        # dropTime = None
        #
        # if baseDropping is not None:
        #     dropId = baseDropping["id"]
        #     dropLocation = baseDropping["location"]
        #     dropTime = baseDropping["time"]
        #
        # busSeatPaxdetails = request.data["blockSeatPaxDetails"]
        #
        # for busSeat in busSeatPaxdetails:
        #     ac = busSeat["ac"]
        #     age = busSeat["age"]
        #     email = busSeat["email"]
        #     fare = busSeat["fare"]
        #     idNumber = busSeat["idNumber"]
        #     idType = busSeat["idType"]
        #     ladiesSeat = busSeat["ladiesSeat"]
        #     lastName = busSeat["lastName"]
        #     mobile = busSeat["mobile"]
        #     name = busSeat["name"]
        #     nameOnId = busSeat["nameOnId"]
        #     primary = busSeat["primary"]
        #     seatNbr = busSeat["seatNbr"]
        #     sex = busSeat["sex"]
        #     sleeper = busSeat["sleeper"]
        #     title = busSeat["title"]
        #     serviceTaxAmount = busSeat["serviceTaxAmount"]
        #     operatorServiceChargeAbsolute = busSeat["operatorServiceChargeAbsolute"]
        #     totalFareWithTaxes = busSeat["totalFareWithTaxes"]
        #
        #     # row = busSeat["row"]
        #     # column = busSeat["column"]
        #     # zIndex = busSeat["zIndex"]
        #     # width = busSeat["width"]
        #     # length = busSeat["length"]

        block_bus_url = url + "blockTicket"

        response = requests.post(block_bus_url, json=request.data, auth=HTTPDigestAuth("TixdoAPI1", "123456"),
                                 timeout=10)

        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)


class seatBooking(APIView):
    def get(self, request, *args, **kwargs):
        blockticket_key = self.request.query_params.get('blockTicketKey')

        book_url = url + "seatBooking?blockTicketKey=" + blockticket_key

        response = requests.get(book_url, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)

        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)


class getTicketByETSTNumber(APIView):
    def get(self, request, *args, **kwargs):

        ETSTNumber = self.request.query_params.get('ETSTNumber')

        etst_url = url + "getTicketByETSTNumber?ETSTNumber=" + ETSTNumber

        response = requests.get(etst_url, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)

        json_data = json.loads(response.text)

        etstNum = json_data['etstnumber']

        json_array = json_data["travelerDetails"]

        for d in json_array:
            travellerDetails = TravellerDetails()

            travellerDetails.name = d['name']
            travellerDetails.lastName = d['lastName']
            travellerDetails.seatnum = d['seatNo']
            travellerDetails.age = d['age']
            travellerDetails.gender = d['gender']
            travellerDetails.fare = d['fare']
            travellerDetails.etstNumber = etstNum

            ticketStatus = json_data["ticketStatus"]

            if ticketStatus != "CONFIRMED":
                travellerDetails.ticketStatus = ticketStatus

            travellerDetails.save()

            # TicketDetails Database Implementation

            pnr = json_data['opPNR']

            ticketDetails = TicketDetails()
            ticketDetails.etstnum = etstNum
            ticketDetails.pnrnum = pnr
            ticketDetails.ticketdump = json_data
            ticketDetails.ticketStatus = json_data['ticketStatus']
            ticketDetails.save()

        return Response(json_data, status=status.HTTP_200_OK)


class CancelTicketConfirmation(APIView):
    def post(self, request, *args, **kwargs):
        cancel_url = url + "cancelTicketConfirmation"

        response = requests.post(cancel_url, json=request.data, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)
        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)


class CancelTicket(APIView):
    def post(self, request, *args, **kwargs):
        cancel_url = url + "cancelTicket"
        response = requests.post(cancel_url, json=request.data, auth=HTTPDigestAuth("TixdoAPI1", "123456"), timeout=10)
        json_data = json.loads(response.text)

        return Response(json_data, status=status.HTTP_200_OK)
