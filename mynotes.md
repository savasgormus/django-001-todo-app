- python -m venv env
- .\env\Scripts\activate
- pip install django
- pip install python-decouple
- django-admin startproject main .
- py manage.py migrate
- py manage.py runserver
- py manage.py startapp todo


- decouple ile secretkey'i .env dosyasına kaydettik. app'imizi settings.py dosyasına girdik.

- app'imizi önce kafamızda tasarlayalım. bir yapılacak iş(title), bu işin tanımı(description), bu işin önceliği(priority), tamamlanıp tamamlanmadığı(isCompleted), bu işin oluşturulma tarihi(created_date) ve işin güncellenme tarihi(updated_date) şeklinde bir şablon oluşturacağız. 
- bu şablonla ilgili bir model oluşturup bunu database'e işledikten sonra frontende göndereceğiz ve app'imiz son halini alacak.

- models.py:

- modelimizi oluşturmaya başlıyoruz. öncelikle bir title oluşturacağız. buraya yapacağımız assignment gelecek. daha sonra bu assignment için bir description alanı oluşturacağız. TextField description için oldukça uygun.
- assignment için bir priority belirlememiz gerekiyor.şimdilik charfield verelim.
- isCompleted ile bir booleanfield oluşturacağız. true ya da false ile görevin tamamlanıp tamamlanmadığını görebileceğiz.
- görevin oluşturma zamanı ve güncellenme zamanını belirteceğiz. burada dikkat etmemiz gereken nokta şu: datetimefield 2 tane olacak fakat içerisine alacağı değer birinde auto_now=true, diğerinde ise auto_now_add=true.
- bu küçük fark oluşturma ve değiştirme tarihini ayrı şekilde bize göstermeye yarayacak.
- priority kısmına geri dönelim. bir tupple ile önceliği yazıya dökeceğiz. böylece standart bir önceliklendirmemiz olacak. priority'nin field optionsuna choices ekleyerek bu tupple'ı seçilebilir hale getirdik.

```py
models.py
from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    PRIORITY = (
        ("1", "High"),
        ("2", "Mid"),
        ("3", "Low"),
    )
    
    priority = models.CharField(max_length=10, choices=PRIORITY)
    isCompleted = models.BooleanField(default=False)

    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
```