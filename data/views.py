"""
    Data -> View 
    For binding the urls with the backend. 
"""
from django.views import View
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.models import User
from .models import BankDetail
from .serializers import BankDetailSerializer, UserSerializer 
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetAllData(APIView):
    """
        This class will return all the data saved in the database.
    """
    def get(self, request):
        """
            Get request to fetch all the data in the API.
            :params-> request
            :return-> API response
        """
        # manager.all() is not json serializable that's why values() used to fetcg data
        queryset = BankDetail.objects.values()
        serializer_class = BankDetailSerializer
        return Response(queryset, status=status.HTTP_200_OK)


class CreateNew(APIView):
    """
        This class will create a new bank details and save that in database.
        Also, it will return the same details in the output if created.
    """

    # authentications 
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            Data saving using the get request as nothing credential is there.
            :params-> request
            :return-> API response and status
        """
        serializer_class = BankDetailSerializer(data=request.data)

        # check flag here so that missing element could be tackle here only.
        if not set(request.query_params) >= {'ifsc_code', 'bank_name', 'branch_name', 'branch_address'}:
            error_response = "Missing Fields. Fields Required : 1.ifsc_code 2.bank_name 3.branch_name 4.branch_address"
            error_response = {
                "Error" : "Missing Fields.",
                "Manadatory Field" : (
                    "ifsc_code", "bank_name", "branch_name", "branch_address"
                )
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        # Exception handling while feeding to database
        # Primary key exception handled here.
        try:
            obj, obj_status = BankDetail.objects.get_or_create(
                ifsc_code=request.query_params.get('ifsc_code'),
                bank_name = request.query_params.get('bank_name'),
                branch_name = request.query_params.get('branch_name'),
                branch_address = request.query_params.get('branch_address')
            )
        except IntegrityError:
            return Response({"Error" : "Ifsc Code already exists"}, status=status.HTTP_226_IM_USED)

        # for the API output as manager.get() is not json serializable
        queryset = BankDetail.objects.filter(
            ifsc_code = obj.ifsc_code
        ).values()

        return Response(queryset, status=status.HTTP_201_CREATED)


class UpdateExisting(APIView):
    """
        This class will update an existing bank details and save that in database.
        Also, it will return the same details in the output if updated successfully.
    """
    # authentications 
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
            GET Method used as no credentials are passing through request.
            :params-> request
            :return-> API response and status
        """
        serializer_class = BankDetailSerializer
        
        # check flag if ifsc is passed or not on which basis update will work.
        if 'ifsc_code' not in request.query_params:
            error_response = {
                "error" : "Missing Fields.",
                "Manadatory Field" : "ifsc_code",
                "Fields can be updated" : (
                    "bank_name", "branch_name", "branch_address"
                ),
                "read_me" : "All fields can be updated at a time or you can choose a particular."
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)   
        
        obj = BankDetail.objects.filter(pk=request.query_params.get('ifsc_code'))
        
        # if ifsc_code not available in the database.
        if not obj:
            return Response({"error": "Data not available for this IFSC Code to get updated"},
                            status=status.HTTP_304_NOT_MODIFIED)

        # handling updation using **kwargs as we don't know which field user want to update.
        temp = {}
        for key in request.query_params:
            # ifsc_code is pk that's why excluded.
            if key == 'ifsc_code':
                continue
            temp[key] = request.query_params.get(key)
        
        # exception handling for unwanted keywords.
        try:
            obj.update(**temp)
        except FieldDoesNotExist as e:
            return Response(f"{e}. Make sure you've gone through manual.", 
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(obj.values(), status= status.HTTP_200_OK)


class IndexView(View):
    message = """
        <h1>API - for adding, updating and fetching IFSC Codes for banks registered in RBI</h1>
        <h2>There are specific urls for each of the following operations: </h2>
        <h4>1. Get all bank details -> https://bank-api-2403.herokuapp.com/ifsc/get</h4>
        <h4>2. Create a new bank details -> https://bank-api-2403.herokuapp.com/ifsc/create</h4>
        <h4>3. Update an existing one -> https://bank-api-2403.herokuapp.com/ifsc/update</h4>

        <p>
            <span style="color: red; font-weight: bold">Note : </span>
            The responses are json response so for the best view use <a href="https://www.postman.com">Postman</a>
            or <a href="https://linuxize.com/post/curl-rest-api/">curl request</a>
        </p>

        <p>Also, to create or update one you need to be authorized, you need to pass username and password
        to get the operations done.<br> All of the above requests can be send using GET method. </p>

        Source code : <a href="https://github.com/Aditya715/Bank-Details-API">Github</a>
    """
    def get(self, request):
        return HttpResponse(self.message)