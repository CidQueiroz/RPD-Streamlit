from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstoqueViewSet, VendaViewSet, AtividadeViewSet, DiarioBordoViewSet, RPDViewSet, LogPODDiarioViewSet

router = DefaultRouter()
router.register(r'estoque', EstoqueViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'atividades', AtividadeViewSet)
router.register(r'diario_bordo', DiarioBordoViewSet)
router.register(r'rpd', RPDViewSet)
router.register(r'log_pod_diario', LogPODDiarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]