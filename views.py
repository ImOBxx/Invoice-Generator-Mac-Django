from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.loader import render_to_string
from .forms import InvoiceForm
from .models import Invoice
import qrcode
from io import BytesIO
import base64
import pdfkit
from django.shortcuts import render
from .models import Invoice
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
import qrcode
from io import BytesIO
import base64
import pdfkit
from .models import Invoice


# Login view
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'app_name/login.html')

# Logout view
def custom_logout(request):
    logout(request)
    return redirect('login')

# Home page view
@login_required
def home(request):
    return render(request, 'app_name/home.html')

# Invoicing overview view
@login_required
def invoicing_overview(request):
    return render(request, 'app_name/overview.html')

# Create invoice view
@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    return render(request, 'app_name/create_invoice.html', {'form': form})

# Invoice detail view
@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Generate QR code
    qr = qrcode.make("https://google.com")
    qr_image = BytesIO()
    qr.save(qr_image, format="PNG")
    qr_image.seek(0)
    qr_code_base64 = base64.b64encode(qr_image.getvalue()).decode("utf-8")

    current_datetime = timezone.localtime(timezone.now())

    return render(request, 'app_name/invoice_detail.html', {
        'invoice': invoice,
        'qr_code_base64': qr_code_base64,
        'current_datetime': current_datetime
    })

# List invoices view
@login_required
def invoices_list(request):
    invoices = Invoice.objects.all().order_by('-invoice_date') 
    return render(request, 'app_name/invoices_list.html', {'invoices': invoices})

# Save invoice view
@login_required
# in views.py
def save_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.is_saved = True  # Example if you have an `is_saved` field
    invoice.save()
    return redirect('invoice_list')  # Ensure this name matches the URL name in urls.py


# Discard (delete) invoice view
@login_required
def discard_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return redirect('invoice_list')

# Print invoice as PDF view
@login_required
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Generate the QR code
    qr = qrcode.make(f"Invoice ID: {invoice.id}")
    qr_image = BytesIO()
    qr.save(qr_image, format="PNG")
    qr_image.seek(0)
    qr_code_base64 = base64.b64encode(qr_image.getvalue()).decode("utf-8")

    # Render the template to HTML
    html_content = render_to_string("app_name/invoice_detail.html", {
        "invoice": invoice,
        "qr_code_base64": qr_code_base64,
    })

    # Generate PDF from the HTML content
    pdf = pdfkit.from_string(html_content, False)

    # Return as a PDF response
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
from django.shortcuts import render
from .models import Invoice
from django.contrib.auth.decorators import login_required

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'app_name/invoice_list.html', {'invoices': invoices})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Invoice

@login_required
def invoices_list(request):
    invoices = Invoice.objects.all().order_by('-date_created')  # Ensure date_created is correctly defined in the model
    return render(request, 'app_name/invoice_list.html', {'invoices': invoices})

from django.shortcuts import get_object_or_404, redirect
from .models import Invoice

@login_required
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return redirect('invoices_list')  # Use the correct URL name here

from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')  # Ensure this URL name matches the login URL pattern in your urls.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
import qrcode
from io import BytesIO
import base64
import pdfkit
from .models import Invoice

@login_required
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Generate the QR code
    qr = qrcode.make(f"Invoice ID: {invoice.id}")
    qr_image = BytesIO()
    qr.save(qr_image, format="PNG")
    qr_image.seek(0)
    qr_code_base64 = base64.b64encode(qr_image.getvalue()).decode("utf-8")

    # Render the template to HTML
    html_content = render_to_string("app_name/invoice_detail.html", {
        "invoice": invoice,
        "qr_code_base64": qr_code_base64,
    })

    try:
        # Generate PDF from the HTML content
        pdf = pdfkit.from_string(html_content, False)
        if pdf:
            # Return as a PDF response
            response = HttpResponse(pdf, content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
            return response
        else:
            return HttpResponse("Failed to generate PDF.", content_type="text/plain")
    except Exception as e:
        # Return an error message if PDF generation fails
        return HttpResponse(f"Error generating PDF: {str(e)}", content_type="text/plain")

