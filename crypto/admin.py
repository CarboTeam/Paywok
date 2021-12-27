from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (PayeeProfile, PaymentReceipts)
from .services import (create_excel_receipt)
# other
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import reverse


@admin.register(PayeeProfile)
class PayeeProfileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'provide_payment')
    list_display_links = ('first_name', 'last_name',)
    list_editable = ('provide_payment',)
    search_fields = ('email', 'first_name', 'last_name')
    save_on_top = True


@admin.register(PaymentReceipts)
class PaymentReceiptsAdmin(ImportExportModelAdmin):
    def make_published(modeladmin, request, queryset):
        return create_excel_receipt(queryset.first())

    list_display = ('id', 'user_profile', 'created', 'receipt_actions')
    list_display_links = ('user_profile',)
    # list_editable = ['approved', ]
    search_fields = ('user_profile__first_name', 'user_profile__last_name', 'user_profile__email')
    save_on_top = True
    make_published.label = 'Get Receipt'
    make_published.short_description = "Download receipt in xlsx format"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/get_receipt', self.admin_site.admin_view(self.process_receipt),
                 name='get-receipt'),
        ]
        return custom_urls + urls

    def receipt_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Get Receipt</a>',
            reverse('admin:get-receipt', args=[obj.pk]),
        )

    def process_receipt(self, request, pk, *args, **kwargs):
        receipt = self.get_object(request, pk)
        return create_excel_receipt(receipt)

    receipt_actions.short_description = 'Receipt Actions'
    receipt_actions.allow_tags = True


admin.site.site_title = "PayWok admin"
admin.site.site_header = "PayWok admin"
