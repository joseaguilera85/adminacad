#-------------------------------------
# egresos/views.py

# Import required modules and functions
from django.shortcuts import render, get_object_or_404, redirect
from .models import Egreso, PurchaseOrder, PurchaseOrderItem, Vendor
from .forms import VendorForm, PurchaseOrderItemForm, PurchaseOrderForm
from datetime import date
from django.core.mail import send_mail
from django.conf import settings

#-------------------------
### Menu ###
#-------------------------

# Main Menu View
def main_menu(request):
    return render(request, 'egresos/menu_egresos.html')

#-------------------------
### Gastos ###
#-------------------------
# List Egresos (Expenses)
def lista_egresos(request):
    # Get all egresos with related purchase orders
    egresos = Egreso.objects.all().select_related('purchase_order')
    # Filter purchase order items related to these egresos
    purchase_order_items = PurchaseOrderItem.objects.filter(purchase_order__in=[egreso.purchase_order for egreso in egresos if egreso.purchase_order is not None])
    
    # Send data to the template
    context = {
        'egresos': egresos,
        'purchase_order_items': purchase_order_items,
    }
    return render(request, 'egresos/lista_egresos.html', context)

#-------------------------
### Proveedores ###
#-------------------------
# List all vendors
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'egresos/vendor_list.html', {'vendors': vendors})

#-------------------------
# Add new vendor
def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new vendor
            return redirect('egresos:vendor_list')
    else:
        form = VendorForm()  # Empty form for GET request
    return render(request, 'egresos/create_vendor.html', {'form': form})

#-------------------------
# Edit existing vendor
def edit_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()  # Save changes to the vendor
            return redirect('egresos:vendor_list')
    else:
        form = VendorForm(instance=vendor)  # Prefill form with existing data
    return render(request, 'egresos/edit_vendor.html', {'form': form, 'vendor': vendor})

#-------------------------
# Delete a vendor
def delete_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        vendor.delete()  # Delete the vendor
        return redirect('egresos:vendor_list')
    return render(request, 'egresos/confirm_delete_vendor.html', {'vendor': vendor})

#-------------------------
### Compras ###
#-------------------------
# List all purchase orders
def purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all().order_by('order_date') 
    return render(request, 'egresos/purchase_order_list.html', {'purchase_orders': purchase_orders})

#-------------------------
# Create a new purchase order
def create_purchase_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            purchase_order = form.save()  # Save new purchase order
            return redirect('egresos:create_purchase_order_item', purchase_order_id=purchase_order.id)
    else:
        form = PurchaseOrderForm()
        form.fields['status'].choices = [('pendiente', 'Pendiente')]  # Default status choice
        
    return render(request, 'egresos/create_purchase_order.html', {'form': form})

#-------------------------
# Create purchase order item
def create_purchase_order_item(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST)
        if form.is_valid():
            purchase_order_item = form.save(commit=False)
            purchase_order_item.purchase_order = purchase_order  # Associate item with purchase order
            purchase_order_item.save()
            return redirect('egresos:create_purchase_order_item', purchase_order_id=purchase_order.id)
    else:
        form = PurchaseOrderItemForm()

    items = PurchaseOrderItem.objects.filter(purchase_order=purchase_order)  # Fetch all items for this order

    return render(request, 'egresos/create_purchase_order_item.html', {
        'form': form,
        'purchase_order': purchase_order,
        'items': items
    })

#-------------------------
# View purchase order item details
def view_purchase_order_item(request, purchase_order_id):
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    items = purchase_order.items.all()  # Get all items for this purchase order
    return render(request, 'egresos/view_purchase_order_item.html', {
        'purchase_order': purchase_order,
        'items': items,
    })

#-------------------------
# Edit purchase order details
def edit_purchase_order(request, order_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=order_id)
    original_status = purchase_order.status  # Store original status for comparison

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        if form.is_valid():
            updated_order = form.save()  # Save the updated purchase order

            # Check if status changed to 'enviada' (sent), and send an email if so
            if original_status != "enviada" and updated_order.status == "enviada":
                subject = "Purchase Order Status Updated"
                message = f"The status of purchase order {purchase_order.id} is now 'Enviada'."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ["recipient@example.com"], fail_silently=False)
            
            # Check if status changed to 'recibida' (received) and create Egreso entries for items
            if original_status != "recibida" and updated_order.status == "recibida":
                for item in purchase_order.purchaseorderitem_set.all():
                    Egreso.objects.create(
                        project=purchase_order.project,
                        categoria=item.categoria,
                        subcategoria=item.subcategoria,
                        empresa=purchase_order.empresa,
                        amount=item.price * item.quantity,
                        date=date.today(),
                        description=f"Egreso for {item.item_name}",
                        purchase_order=purchase_order
                    )
            return redirect('egresos:purchase_order_list')
    else:
        form = PurchaseOrderForm(instance=purchase_order)

        # Adjust status field choices based on the current status
        if purchase_order.status == "pendiente":
            form.fields['status'].choices = [('pendiente', 'Pendiente'), ('enviada', 'Enviada')]
        elif purchase_order.status == "enviada":
            form.fields['status'].choices = [('enviada', 'Enviada'), ('recibida', 'Recibida')]

    return render(request, 'egresos/edit_purchase_order.html', {'form': form, 'purchase_order': purchase_order})

#-------------------------
# Delete purchase order
def delete_purchase_order(request, order_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=order_id)

    if request.method == 'POST':
        purchase_order.delete()  # Delete the purchase order
        return redirect('egresos:purchase_order_list')

    return render(request, 'egresos/confirm_delete_purchase_order.html', {'purchase_order': purchase_order})

#-------------------------
# Edit purchase order item
def edit_purchase_order_item(request, purchase_order_id, item_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id)
    purchase_order_item = get_object_or_404(PurchaseOrderItem, id=item_id, purchase_order=purchase_order)

    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST, instance=purchase_order_item)
        if form.is_valid():
            form.save()  # Save updated purchase order item
            return redirect('egresos:create_purchase_order_item', purchase_order_id=purchase_order.id)
    else:
        form = PurchaseOrderItemForm(instance=purchase_order_item)

    items = PurchaseOrderItem.objects.filter(purchase_order=purchase_order)

    return render(request, 'egresos/edit_purchase_order_item.html', {
        'form': form,
        'purchase_order': purchase_order,
        'items': items,
        'purchase_order_item': purchase_order_item
    })

#-------------------------
# Delete purchase order item
def delete_purchase_order_item(request, purchase_order_id, item_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id)
    purchase_order_item = get_object_or_404(PurchaseOrderItem, id=item_id, purchase_order=purchase_order)
    purchase_order_item.delete()  # Delete the item
    return redirect('egresos:create_purchase_order_item', purchase_order_id=purchase_order.id)

#-------------------------
### Almacen ###
#-------------------------
# Almacen (Warehouse) View
def almacen(request):
    purchase_orders = PurchaseOrder.objects.exclude(status="pendiente").order_by('order_date')  # Exclude orders with 'pendiente' status and order by 'order_date'
    return render(request, 'egresos/almacen.html', {'purchase_orders': purchase_orders})


#-------------------------------------
