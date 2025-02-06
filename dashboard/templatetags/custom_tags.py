import qrcode
import base64
from io import BytesIO
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def generate_qr(unique_id):
    qr = qrcode.make(f'https://program.crademaster.com/register?event={unique_id}')
    qr = qr.resize((200, 200))

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_image_data = buffer.getvalue()
    qr_base64 = base64.b64encode(qr_image_data).decode()

    return mark_safe(f'<img src="data:image/png;base64,{qr_base64}" alt="QR Code">')
