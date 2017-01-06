from core.admin import ReadOnlyAwareAdmin, SliceInline
from core.middleware import get_request
from core.models import User

from django import forms
from django.contrib import admin

from services.vmme.models import *

class VMMEServiceForm(forms.ModelForm):

    class Meta:
        model = VMMEService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VMMEServiceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return super(VMMEServiceForm, self).save(commit=commit)

class VMMEServiceAdmin(ReadOnlyAwareAdmin):

    model = VMMEService
    verbose_name = "VMME Service"
    verbose_name_plural = "VMME Services"
    form = VMMEServiceForm
    inlines = [SliceInline]

    list_display = ('backend_status_icon', 'name', 'enabled')
    list_display_links = ('backend_status_icon', 'name')

    fieldsets = [(None, {
        'fields': ['backend_status_text', 'name', 'enabled', 'versionNumber', 'description',],
        'classes':['suit-tab suit-tab-general',],
        })]

    readonly_fields = ('backend_status_text', )
    user_readonly_fields = ['name', 'enabled', 'versionNumber', 'description',]

    extracontext_registered_admins = True

    suit_form_tabs = (
        ('general', 'VMME Service Details', ),
        ('slices', 'Slices',),
        )

    suit_form_includes = ((
        'top',
        'administration'),
        )

    def get_queryset(self, request):
        return VMMEService.get_service_objects_by_user(request.user)

admin.site.register(VMMEService, VMMEServiceAdmin)

class VMMETenantForm(forms.ModelForm):

    class Meta:
        model = VMMETenant
        fields = '__all__'

    creator = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(VMMETenantForm, self).__init__(*args, **kwargs)

        self.fields['kind'].widget.attrs['readonly'] = True
        self.fields['kind'].initial = "vmme"

        self.fields['provider_service'].queryset = VMMEService.get_service_objects().all()

        if self.instance:
            self.fields['creator'].initial = self.instance.creator
            self.fields['tenant_message'].initial = self.instance.tenant_message

        if (not self.instance) or (not self.instance.pk):
            self.fields['creator'].initial = get_request().user
            if VMMEService.get_service_objects().exists():
                self.fields['provider_service'].initial = VMMEService.get_service_objects().all()[0]

    def save(self, commit=True):
        self.instance.creator = self.cleaned_data.get('creator')
        self.instance.tenant_message = self.cleaned_data.get('tenant_message')
        return super(VMMETenantForm, self).save(commit=commit)


class VMMETenantAdmin(ReadOnlyAwareAdmin):

    verbose_name = "VMME Service Tenant"
    verbose_name_plural = "VMME Service Tenants"

    list_display = ('id', 'backend_status_icon', 'instance', 'tenant_message')
    list_display_links = ('backend_status_icon', 'instance', 'tenant_message', 'id')

    fieldsets = [(None, {
        'fields': ['backend_status_text', 'kind', 'provider_service', 'instance', 'creator', 'tenant_message'],
        'classes': ['suit-tab suit-tab-general'],
        })]

    readonly_fields = ('backend_status_text', 'instance',)

    form = VMMETenantForm

    suit_form_tabs = (('general', 'Details'),)

    def get_queryset(self, request):
        return VMMETenant.get_tenant_objects_by_user(request.user)

admin.site.register(VMMETenant, VMMETenantAdmin)