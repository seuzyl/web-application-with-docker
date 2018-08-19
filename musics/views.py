# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from . models import Music
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.template import loader
from django.http import HttpResponse


def index(request):
	template = loader.get_template("musics/index.html")
	context = {}
	return HttpResponse(template.render(context, request))


Class MusicView(APIView):
    def get(self, request, *args, **kwargs):
    	musics = Music.objects.all()
    	music_list = []
    	for music in musics:
    		d = dict()
    		d["song"] = music.song
    		d["singer"] = music.singer
    		d["style"] = music.style
    		d["created"] = music.created
    		music_list.append(d)

    	return Response(data=music_list, status=status.HTTP_200_OK)

    def post(self, request):
    	new_song = request.data
    	Music.objects.create(song=new_song.get("song"),singer=new_song.get("singer"), 
    		                 style=new_song.get("style"),created=new_song.get("created"))
    	return Response(status=status.HTTP_201_CREATED)
    