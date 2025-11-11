from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Estoque, Venda, Atividade, DiarioBordo, RPD, LogPODDiario
from .serializers import EstoqueSerializer, VendaSerializer, AtividadeSerializer, DiarioBordoSerializer, RPDSerializer, LogPODDiarioSerializer

class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only see and manage their own stock items
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user for the new stock item
        serializer.save(usuario=self.request.user)

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only see and manage their own sales
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user for the new sale
        venda = serializer.save(usuario=self.request.user)

        # Decrement stock quantity
        estoque_item = venda.estoque_item
        if estoque_item.quantidade >= venda.quantidade:
            estoque_item.quantidade -= venda.quantidade
            estoque_item.save()
        else:
            # Handle insufficient stock (e.g., raise an error)
            raise serializers.ValidationError("Quantidade em estoque insuficiente.")

class AtividadeViewSet(viewsets.ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only see and manage their own activities
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user for the new activity
        serializer.save(usuario=self.request.user)

class DiarioBordoViewSet(viewsets.ModelViewSet):
    queryset = DiarioBordo.objects.all()
    serializer_class = DiarioBordoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class RPDViewSet(viewsets.ModelViewSet):
    queryset = RPD.objects.all()
    serializer_class = RPDSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class LogPODDiarioViewSet(viewsets.ModelViewSet):
    queryset = LogPODDiario.objects.all()
    serializer_class = LogPODDiarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)