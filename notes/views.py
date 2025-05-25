from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user, is_deleted=False).order_by('due_date')
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_list.html', {'notes': notes, 'form': form})


@login_required
def note_toggle_done(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_done = not note.is_done
    note.save()
    return redirect('note_list')


@login_required
def note_delete(request, pk):  # <--- Функция для удаления в корзину
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_deleted = True
    note.save()
    return redirect('note_list')


@login_required
def trash(request):  # Корзина
    deleted_notes = Note.objects.filter(user=request.user, is_deleted=True)
    return render(request, 'notes/trash.html', {'deleted_notes': deleted_notes})


@login_required
def restore_note(request, pk):  # Восстановить из корзины
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_deleted = False
    note.save()
    return redirect('trash')


@login_required
def permanently_delete_note(request, pk):  # Полное удаление
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    return redirect('trash')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логиним нового пользователя
            return redirect('note_list')  # редирект на главную страницу с заметками
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
