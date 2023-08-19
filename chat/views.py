from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Block, GroupBlock, PrivateBlock

from .serializers import GroupBlockSerializer, PrivateBlockSerializer

from .decorators import only_authenticated

from .forms import SignUpForm
# Create your views here.


def sign_up(request):
    if request.POST:
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
        return HttpResponse('form is not valid!')
    else:
        form = SignUpForm()

        return render(request, 'chat/sign_up.html', {'form': form})


def sign_in(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if form.is_valid():
            login(request, user)
            return redirect('')
    else:
        form = AuthenticationForm()

        return render(request, 'chat/sign_in.html', {'form': form})


def dashboard(request):

    return render(request, 'chat/dashboard.html')


# === Blocks ===
def blocks(request):
    block_list = Block.objects.all()

    context = {
        'blocks': block_list
    }

    return render(request, 'chat/blocks.html', context)


# === Users ===
def candlechat_users(request):
    users = User.objects.all()

    return render(request, 'chat/candlechat_users.html', {'users': users})


# === Group Block view === 
@only_authenticated
def group_block(request, slug):
    detail = get_object_or_404(Block, slug=slug)

    context = {
        'detail': detail,
    }
    return render(request, 'chat/group_block.html', context)


# === Private Block view ===
@only_authenticated
def private_block(request, other_user_id):

    return render(request, 'chat/private_block.html')


# === Group Block Messages API ===
class GroupBlockMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get_block(self, block_slug):
        try:
            return Block.objects.get(slug=block_slug)
        except Block.DoesNotExist:
            raise Http404

    def get(self, request, block_slug):
        block = self.get_block(block_slug)
        messages = GroupBlock.objects.filter(block=block)
        serializer = GroupBlockSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# === Private Block Messages API ===
class PrivateBlockMessagesView(APIView):
    def get_other_user(self, other_user_id):
        try:
            return User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, other_user_id):
        user = User.objects.get(id=other_user_id)

        block_thread = (
            f"block_{request.user.id}_{user.id}"
            if int(request.user.id) > int(user.id)
            else f"block_{user.id}_{request.user.id}"
        )
        private_block_messages = PrivateBlock.objects.filter(block_thread=block_thread).select_related('user')
        serializer = PrivateBlockSerializer(private_block_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
