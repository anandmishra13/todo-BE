from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from auth_user.models import User
import json
from .models import Todo

@api_view(['POST'])
def create_todo(request):
    data = json.loads(request.body)
    title = data.get('title')
    username = data.get('username')

    if not title or not username:
        return Response({"error": "Title and username are required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return  Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    todo = Todo(title=title, user=user, description=data.get('description'))
    todo.save()

    return Response({"status": "ToDo created"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_todo(request):
    data = request.query_params
    username = data.get('username')

    if not username:
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "user not found."}, status=status.HTTP_400_BAD_REQUEST)

    todos = Todo.objects(user=user)
    print('todos', todos)
    todos_list = [{
        "id": str(todo.id),
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at,
    } for todo in todos]

    return Response({
        "todos": todos_list
    }, status=status.HTTP_200_OK)


# @csrf_exempt
# def todo_create(request):
#     if request.method == 'GET':
#         return JsonResponse({
#             'message': 'Todo API is working! Use POST to create new todos.',
#             'status': 'ok'
#         })
#
#     elif request.method == 'POST':
#         print("RAW BODY:", request.body)
#         try:
#             # Show parsed data
#             data = json.loads(request.body)
#             print("Parsed JSON:", data)
#
#             todo = Todo(
#                 title=data.get('title', ''),
#                 description=data.get('description', ''),
#                 completed=data.get('completed', False)
#             )
#
#             # Save to DB
#             todo.save()
#
#             return JsonResponse({
#                 'success': True,
#                 'id': str(todo.id),
#                 'title': todo.title,
#                 'description': todo.description,
#                 'completed': todo.completed,
#                 'created_at': todo.created_at.isoformat()
#             }, status=201)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=400)
#
#     return JsonResponse({
#         'success': False,
#         'error': 'Method not allowed'
#     }, status=405)
