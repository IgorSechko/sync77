from datetime import datetime
import json
from django.shortcuts import render, redirect
from .forms import JSONUploadForm
from .models import Item


def upload_json_view(request):
    error_messages = []
    success = None

    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['json_file']
            data = json.load(json_file)

            name = data.get('name')
            date = data.get('date')

            if name is None or date is None:
                error_messages.append("Файл должен содержать ключи 'name' и 'date'.")
            
            if name and len(name) >= 50:
                error_messages.append("Поле 'name' должно содержать менее 50 символов.")
            
            try:
                datetime.strptime(date, "%Y-%m-%d_%H:%M")
            except ValueError:
                error_messages.append(f"Неверный формат даты: '{date}'. Ожидается YYYY-MM-DD_HH:mm.")

            if not error_messages:
                Item.objects.create(name=name, date=date)
                success = "JSON-файл загружен успешно"

    else:
        form = JSONUploadForm()

    return render(request, 'taskapp/upload.html', {
        'form': form,
        'errors': error_messages,
        'success': success
    })


def all_items_view(request):
    items = Item.objects.all()
    return render(request, 'taskapp/all_items.html', {'items': items})
