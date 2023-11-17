from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Block, GroupBlock, PrivateBlock

from .serializers import GroupBlockSerializer, PrivateBlockSerializer

from .decorators import only_unauthenticated

from .forms import SignUpForm, SignInForm
# Create your views here.


# === Sign Up ===
@only_unauthenticated
def sign_up(request):
    if request.POST:
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sign_in')
        return redirect('sign_up')
    else:
        form = SignUpForm()

        return render(request, 'chat/sign_up.html', {'form': form})


# === Sign In ===
@only_unauthenticated
def sign_in(request):
    if request.POST:
        form = SignInForm(request.POST)
        print(form)

        if form.is_valid():
            print('This form is not even valid')
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                print(e)
                return redirect('sign_in')
        else:
            return redirect('sign_in')
    else:
        form = SignInForm()

        return render(request, 'chat/sign_in.html', {'form': form})


# === Sign Out ===
def sign_out(request):
    logout(request)

    return redirect('sign_in')


# === Dashboard ===
@login_required
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
@login_required
def group_block(request, slug):
    detail = get_object_or_404(Block, slug=slug)

    context = {
        'detail': detail,
    }
    return render(request, 'chat/group_block.html', context)


# === Private Block view ===
@login_required
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
