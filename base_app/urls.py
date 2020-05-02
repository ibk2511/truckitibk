from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('truck_list/', views.TruckListView.as_view(), name='truckList'),
    path('truck_list/<int:pk>/detail', views.TruckDetailView.as_view(), name='truckDetail'),
    path('truck_list/<int:pk>/create_truck_rent', views.create_truck_rent, name='truckrent-create'),
    path('truck_list/<int:pk>/delete', views.delete_truck_view, name='delete-truck'),
    path('', TemplateView.as_view(template_name='base_app/index.html'), name='main_page'),
    path('login/', views.loginView, name='login'),
    path('signup/', views.registerView, name='signup'),
    path('truck_create/', views.create_truck, name='truck-create'),
    path('logout/', views.logOut, name='logout'),
    path('deletetruck/', views.truckDelete, name='deletetruck'),
    path('truckrequests/', views.truckRequest, name='truckrequest'),
    path('cilentrequest/',views.cilentRequest, name="cilentrequest"),
    path('truck_rent/<int:id>/accept/',views.truck_rent_accept,name='truck_rent_accept'),
    path('truck_rent/<int:id>/reject/', views.truck_rent_reject, name='truck_rent_reject')
]
