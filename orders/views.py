from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from orders.forms import ODOrderForm
from orders.models import ODOrder


# -------------------------------------------------------------------------------------- #
############################## (START) THIS SECTION: MY TASK #############################
# -------------------------------------------------------------------------------------- #

from .models import Vehicle
from .forms import VehicleForm, VehicleFormDelete, VehicleFormChangePhoto
from PIL import Image
from django.conf import settings
import os

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'order/vehicle/vehicle_list.html', {'vehicles': vehicles})


def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            instance_vehicle = form.save(commit=False)
            instance_vehicle.number = instance_vehicle.number.upper()
            instance_vehicle.save()
            messages.success(request, "Vehicle successfully added")
            return redirect(reverse('order:vehicle_list'))
    else:
        form = VehicleForm()
    return render(request, 'order/vehicle/vehicle_add.html', {'form': form})


def vehicle_edit(request, number):
    # get instance with safe method get_object_or_404
    vehicle = get_object_or_404(Vehicle, number=number)
    # if request is POST (submit form)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle successfully edited")
            return redirect(reverse('order:vehicle_list'))
    else:
        # if request is GET (open form edit vehicle)
        form = VehicleForm(instance=vehicle)
    return render(request, 'order/vehicle/vehicle_edit.html', {'form': form, 'vehicle': vehicle})


def vehicle_delete(request, number):
    vehicle = get_object_or_404(Vehicle, number=number)
    if request.method == 'POST':
        form = VehicleFormDelete(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle.delete()
            messages.success(request, "Vehicle successfully delete")
            return redirect(reverse('order:vehicle_list'))
    else:
        form = VehicleFormDelete(instance=vehicle)
    return render(request, 'order/vehicle/vehicle_delete.html', {'form': form, 'vehicle': vehicle})


def vehicle_change_photo(request, number):
    vehicle = get_object_or_404(Vehicle, number=number)
    if request.method == 'POST':
        form = VehicleFormChangePhoto(data=request.POST, files=request.FILES, instance=vehicle)
        if form.is_valid():
            # get instance from form
            instance_vehicle = form.save(commit=False)
            # must be saved first
            instance_vehicle.save()
            
            # if photo field is not empty 
            if request.FILES.get('photo'):
                # create thumbnails with Pillow
                # set thumbnails 
                size = 100, 100
                # get PATH Photo
                photo_root = settings.MEDIA_ROOT+"\\"+instance_vehicle.photo.name
                # in this case, if i used Windows, i need replace \ characters to / characters
                im = Image.open(photo_root.replace("\\", "/"))
                # create thumbnails with size tuple
                im.thumbnail(size)
                # saving image
                im.save(photo_root)
                messages.success(request, "Vehicle successfully changed photo")
                
            return redirect(reverse('order:vehicle_list'))
    else:
        form = VehicleFormChangePhoto(instance=vehicle)
    return render(request, 'order/vehicle/vehicle_change_photo.html', {'form': form, 'vehicle': vehicle})

# ------------------------------------------------------------------------------------ #
############################## (END) THIS SECTION: MY TASK #############################
# ------------------------------------------------------------------------------------ #


def index(request):
    """
    Handle index page for order
    """

    return render(request, 'order/index.html')


def management(request):
    """
    Showing list of order in management home page
    """

    # query on all order records
    orders = ODOrder.objects.all()

    # structured order into simple dict, 
    # later on, in template, we can render it easily, ex: {{ orders }}
    data = {'orders': orders}

    return render(request, 'order/management.html', data)


def create_order(request):
    """
    Handle new order creation
    """

    # Initial form and data
    data = {
        'form': ODOrderForm(),
    }

    # if user submit data from this page, we capture the POST data and save it
    if request.method == 'POST':

        # wrap POST data with the form
        form = ODOrderForm(request.POST)

        # Transaction savepoint (good to provide rollback data)
        sid = transaction.savepoint()

        if form.is_valid():

            # wrap form result into dict ODOrder model fields structure 
            order_data = {
                'name': form.cleaned_data.get('name'),
                'phone': form.cleaned_data.get('phone'),
                'price': form.cleaned_data.get('price'),
            }

            try:
                ODOrder.objects.create(**order_data)
            except:
                transaction.savepoint_rollback(sid)
                messages.error(request, "Oops! Something wrong happened!")

            messages.info(request, "A new record has been created!")

    return render(request, 'order/create_order.html', data)


def edit_order(request, uuid=None):
    """
    How to remove order
    """
    if not uuid:
        return redirect(reverse('order:management'))

    # validate given UUID match with record in database
    try:
        order = ODOrder.objects.get(uuid=uuid)
    except ODOrder.DoesNotExist:
        messages.error(request, "Record not found!")
        return redirect(reverse('order:management'))

    data = {
        'form': ODOrderForm(instance=order),
    }

    # if user submit data from this page, we capture the POST data and save it
    if request.method == 'POST':

        # wrap POST data with the form
        form = ODOrderForm(request.POST, instance=order)

        # Transaction savepoint (good to provide rollback data)
        sid = transaction.savepoint()

        if form.is_valid():

            try:
                form.save()
            except:
                transaction.savepoint_rollback(sid)
                messages.error(request, "Oops! Something wrong happened!")

            messages.info(request, "Record has been updated!")

    return render(request, 'order/edit_order.html', data)


def delete_order(request, uuid=None):
    """
    How to remove order
    """
    if uuid:

        # finding given UUID to match order in database
        try:
            order = ODOrder.objects.get(uuid=uuid)
        except ODOrder.DoesNotExist:
            messages.error(request, "Order not found")
        else:
            # delete order from database
            order.delete()
            messages.success(request, 'Order "{}" has been deleted'.format(order.name))

    return redirect(reverse('order:management'))





