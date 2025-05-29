from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages  # Добавь в начало файла, если ещё не импортировал

@login_required
def note_list(request):
    query = request.GET.get('q', '')  # Получаем запрос из строки поиска (или пустую строку по умолчанию)
    
    # Основной фильтр по user и is_deleted
    notes = Note.objects.filter(user=request.user, is_deleted=False)
    
    # Если есть поисковый запрос, фильтруем по заголовку и содержимому
    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    # Сортировка по дате
    notes = notes.order_by('due_date')
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, '✅ Заметка успешно добавлена!')  # Добавляем уведомление
            return redirect('note_list')
        else:
            messages.error(request, '❌ Не удалось добавить заметку. Проверьте правильность данных.')
    else:
        form = NoteForm()
    
    return render(request, 'notes/note_list.html', {'notes': notes, 'form': form, 'query': query})


def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_edit.html', {'form': form, 'note': note})





@login_required
def note_toggle_done(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_done = not note.is_done
    note.save()
    return redirect('note_list')


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.is_deleted = True
    note.save()
    messages.success(request, f"Заметка '{note.title}' перенесена в корзину.")
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
    messages.success(request, f"Заметка '{note.title}' восстановлена из корзины.")
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
