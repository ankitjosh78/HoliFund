from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MemberForm
from .models import Building, Floor, Member, Room


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "festival/login.html", context)


@login_required
def dashboard(request):
    buildings = Building.objects.all()
    total_collected = Member.objects.aggregate(total=Sum("amount_paid"))["total"] or 0
    context = {
        "buildings": buildings,
        "total_collected": total_collected,
    }
    return render(request, "festival/dashboard.html", context)


@login_required
def building_detail(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    floors = Floor.objects.filter(building=building)
    context = {
        "building": building,
        "floors": floors,
    }
    return render(request, "festival/building_detail.html", context)


@login_required
def floor_detail(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    rooms = Room.objects.filter(floor=floor)
    context = {
        "floor": floor,
        "rooms": rooms,
    }
    return render(request, "festival/floor_detail.html", context)


@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    members = Member.objects.filter(room=room)
    context = {
        "room": room,
        "members": members,
    }
    return render(request, "festival/room_detail.html", context)


@login_required
def add_member(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.room = room
            member.save()
            return redirect("room_detail", room_id=room.id)
    else:
        form = MemberForm()
    context = {
        "form": form,
        "room": room,
    }
    return render(request, "festival/add_member.html", context)


@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("room_detail", room_id=member.room.id)
    else:
        form = MemberForm(instance=member)
    context = {
        "form": form,
        "member": member,
    }
    return render(request, "festival/edit_member.html", context)


@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    room_id = member.room.id
    if request.method == "POST":
        member.delete()
        return redirect("room_detail", room_id=room_id)
    context = {
        "member": member,
    }
    return render(request, "festival/delete_member.html", context)
