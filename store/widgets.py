from django.forms.widgets import TextInput
from django.utils.html import format_html

class BarcodeInputWidget(TextInput):
    template_name = 'admin/widgets/barcode_input.html'
    
    class Media:
        js = ['js/barcode_scanner.js']
        
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Ensure we have an ID for the input field
        if 'id' not in attrs:
            attrs['id'] = f'id_{name}'
        context['widget']['attrs'] = attrs
        return context
