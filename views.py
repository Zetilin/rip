from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Reactor, Station, ReactorStation


def index(request):
    reactor_name = request.GET.get("reactor_name", "")
    reactors = Reactor.objects.filter(status=1)

    if reactor_name:
        reactors = reactors.filter(name__icontains=reactor_name)

    draft_station = get_draft_station()

    context = {
        "reactor_name": reactor_name,
        "reactors": reactors
    }

    if draft_station:
        context["reactors_count"] = len(draft_station.get_reactors())
        context["draft_station"] = draft_station

    return render(request, "reactors_page.html", context)


def add_reactor_to_draft_station(request, reactor_id):
    reactor_name = request.POST.get("reactor_name")
    redirect_url = f"/?reactor_name={reactor_name}" if reactor_name else "/"

    reactor = Reactor.objects.get(pk=reactor_id)

    draft_station = get_draft_station()

    if draft_station is None:
        draft_station = Station.objects.create()
        draft_station.owner = get_current_user()
        draft_station.date_created = timezone.now()
        draft_station.save()

    if ReactorStation.objects.filter(station=draft_station, reactor=reactor).exists():
        return redirect(redirect_url)

    item = ReactorStation(
        station=draft_station,
        reactor=reactor
    )
    item.save()

    return redirect(redirect_url)


def reactor_details(request, reactor_id):
    context = {
        "reactor": Reactor.objects.get(id=reactor_id)
    }

    return render(request, "reactor_page.html", context)


def delete_station(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE stations SET status=5 WHERE id = %s", [station_id])

    return redirect("/")


def station(request, station_id):
    if not Station.objects.filter(pk=station_id).exists():
        return redirect("/")

    station = Station.objects.get(id=station_id)
    if station.status == 5:
        return redirect("/")

    context = {
        "station": station,
    }

    return render(request, "station_page.html", context)


def get_draft_station():
    return Station.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()