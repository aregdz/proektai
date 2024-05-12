from django import forms

class MultipleImageInput(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs)

class ContactForm(forms.Form):
    # оснавнная форма
    teacher_name = forms.CharField(max_length=100, label='ФИО преподавателя')
    group_name = forms.CharField(max_length=100, label='Название группы')
    subject_name = forms.CharField(max_length=100, label='Название предмета')
    number = forms.IntegerField(min_value=1, label='Количество студентов', max_value=30)
    correct_answers_image = forms.ImageField(label='Загрузите изображение с правильными ответами', required=False)

class UploadImageForm(forms.Form):
    image = forms.ImageField(widget=MultipleImageInput())

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField(label='Загрузите тест')
