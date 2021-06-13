from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import Address
from users.serializers import AddressSerializer


class AddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        addresses = user.addresses.all()
        if not addresses:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.addresses.filter(id=request.data['id']):
            return Response(status=status.HTTP_404_NOT_FOUND)

        address = request.user.addresses.get(id=request.data['id'])
        address.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        if not request.user.addresses.filter(id=request.data['id']):
            return Response(status=status.HTTP_404_NOT_FOUND)

        address = request.user.addresses.get(id=request.data['id'])
        serializer = AddressSerializer(address, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
