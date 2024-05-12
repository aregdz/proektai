import os

from django.http import HttpResponse, Http404
import time
from django.template import RequestContext
from EvalAI.settings import BASE_DIR
from main import ai
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ContactForm, ImageUploadForm

def main(request):
    # Для главной старницы
    return render(request, 'main/main.html')




def forms(request):
    # Страница с формами
    form = ContactForm()
    image_forms = []  # Список изначально пустой

    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Если все поля заполнены, то:
        if form.is_valid():
            # Получаю значение заполненных полей
            current_time = time.localtime()
            current_minutes = current_time.tm_min
            number = form.cleaned_data['number']
            teacher_name  = form.cleaned_data['teacher_name']
            group_name = form.cleaned_data['group_name']
            subject_name = form.cleaned_data['subject_name']
            zzz = [teacher_name, group_name, subject_name]
            namefile = teacher_name[0:2] + group_name[0:3] + subject_name[0:2] + str(current_minutes)

            if 'correct_answers_image' in request.FILES: # валидацию правильных ответов
                correct_img = request.FILES['correct_answers_image'] # переменная с правильными ответами
                handle_uploaded_file(correct_img, namefile, True)  # функция для сохранения в папку


            #Создаю переменную(название папки, где будут храниться картины пользователя)
            # Определяем количество раз для вызова полей, предназначенных для сохранения картин
            image_forms = [ImageUploadForm(request.POST, request.FILES, prefix=str(x)) for x in range(number)]
            # Валидация и сохранение изображений
            if all([f.is_valid() for f in image_forms]):
                for image_form in image_forms:
                    img = image_form.cleaned_data['image']
                    handle_uploaded_file(img, namefile)
                # После успешного сохранения изображений выполняется перенаправление
                # медиаимеджис написал сам в настройках проверить можно
                IMAGE_DIR = os.path.join(settings.MEDIA_IMAGES, namefile) # вызвываю этот путь в переменную
                Exel_path = os.path.join(BASE_DIR, "media", 'exel') # папка для хранения иксель файла
                l = namefile + ".xlsx" # название иксель файла
                ai.create_excel_with_images_from_template(IMAGE_DIR, Exel_path, l, zzz) #вызваю функцию из ai
                request.session['excel_file_name'] = l #передача хначения иксель фала(это нужно для страницы, где гружу иксель пользователю)
                return redirect('results') # после всего перенеаправляю на другую страницу

    # Если это GET-запрос(первый) или форма не валидна - покажем базовую форму и формы для изображений
    return render(request, 'main/forms.html', {'form': form, 'image_forms': image_forms})

def results(request):
    excel_file_name = request.session.get('excel_file_name', 'default_filename.xlsx')
    # Далее, вы отправляете это имя в контекст шаблона
    context = {
        'excel_file_name': excel_file_name,
    }

    return render(request, 'main/results.html', context)


import os


def handle_uploaded_file(image, folder_name, create_trot=False):
    # Определение базовой директории для сохранения изображений
    base_dir = os.path.join(settings.MEDIA_ROOT, 'images')

    # Если необходимо создать папку trot
    if create_trot:
        dir_path = os.path.join(base_dir, folder_name, 'trot')
    else:
        dir_path = os.path.join(base_dir, folder_name)

    # Создание директории, если она не существует
    os.makedirs(dir_path, exist_ok=True)

    # Сохранение файла
    with open(os.path.join(dir_path, image.name), 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)


def contacts(request):
    # для страницы контакты
    return render(request, 'main/contacts.html')

def about(requst):
    # для страницы о нас
    return render(requst, 'main/about.html')

def kak(requst):
    # для страницы о нас
    return render(requst, 'main/kak.html')


def download_excel(request, file_name):
    # Удостоверьтесь, что переменная file_name соответствует имени созданного файла Excel
    # И создайте путь к файлу.
    file_path = os.path.join(BASE_DIR, "media", 'exel', file_name)

    # Проверяем наличие файла
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404 # Если файл не найден, возвращаем ошибку 404
