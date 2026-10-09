from typing import override

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from .models import Order, Item

admin.site.register(Order)
admin.site.register(Item)

class CartEngagementAdminSite(admin.AdminSite):
    @override
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('most-purchased', self.admin_view(self.most_purhcased_view), name='engagement.most_purchased'),
        ]
        return custom_urls + urls

    def most_purhcased_view(self, request: HttpRequest) -> HttpResponse:
        users = get_user_model().objects.all()

        high_user = None
        high_purchase_count = 0
        for user in users:
            orders = Order.objects.filter(user=user)

            purchase_count = 0
            for order in orders:
                items = Item.objects.filter(order=order)
                for item in items:
                    purchase_count += item.quantity

            if purchase_count > high_purchase_count or high_user is None:
                high_user = user
                high_purchase_count = purchase_count

        template_data = {
            **self.each_context(request),
        }
        template_data['title'] = "Highest Purchasing User"
        template_data['user'] = high_user
        template_data['purchase_count'] = high_purchase_count
        return render(request, 'cart/most_purchased.html', template_data)

cart_engagement_admin_site = CartEngagementAdminSite(name="cart_engagement_admin")
