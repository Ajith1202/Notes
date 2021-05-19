from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Note
from .serializers import NoteSerializer

User = get_user_model()

@api_view(['GET', 'POST'])
def NoteListCreateAPIView(request):
    user = request.user
    if not user.is_authenticated:
        content = {"Login to your account."}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        notes_set = user.notes.all()
        serialized_data = NoteSerializer(notes_set, many=True)
        return Response(serialized_data.data)        

    elif request.method == 'POST':
        title = request.data.get('title')
        author = request.user
        content = request.data.get("content")
        note = Note.objects.create(author=author, title=title, content=content)
        note_serializer = NoteSerializer(note, many=False)
        
        return Response(note_serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def NoteUpdateDeleteAPIView(request, pk):
    user = request.user
    if not user.is_authenticated:
        return Response("LOGIN TO YOUR ACCOUNT")

    try :
        note = user.notes.get(id=pk)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)        

    if request.method == 'GET':
        note_serializer = NoteSerializer(note, many=False)
        return Response(note_serializer.data)

    elif request.method == 'PUT':
        note_serializer = NoteSerializer(note, {"title": request.data.get('title'), "content": request.data.get('content')})
        if note_serializer.is_valid():
            note_serializer.save()
            return Response(note_serializer.data)
    
    elif request.method == 'DELETE':
        note.delete()
        return Response("Deleted successfully..")
        
    return Response('Sorry...')
