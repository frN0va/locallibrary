from django.shortcuts import render

from .models import Room


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    chat_room, _ = Room.objects.get_or_create(name=room_name)
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "room": chat_room,
        "messages": chat_room.messages.select_related("author"),
    })
