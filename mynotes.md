- python -m venv env
- .\env\Scripts\activate
- pip install django
- pip install python-decouple
- django-admin startproject main .
- py manage.py migrate
- py manage.py runserver
- py manage.py startapp todo

- decouple ile secretkey'i .env dosyasına kaydettik. app'imizi settings.py dosyasına girdik.
- aynı şekilde DEBUG kısmını da .env dosyasına kaydettik ve config('DEBUG') şeklinde settings.py dosyamıza girdik.

```txt
SECRET_KEY =django-insecure-9w#v1j1dzw@k(3f=a=+f6p#+y&1f_dl6e%tn)2j%wq$vikohu$
DEBUG = True
```

```py
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')
```

- app'imizi önce kafamızda tasarlayalım. bir yapılacak iş(title), bu işin tanımı(description), bu işin önceliği(priority), tamamlanıp tamamlanmadığı(isCompleted), bu işin oluşturulma tarihi(created_date) ve işin güncellenme tarihi(updated_date) şeklinde bir şablon oluşturacağız. 
- bu şablonla ilgili bir model oluşturup bunu database'e işledikten sonra frontende göndereceğiz ve app'imiz son halini alacak.

- models.py:

- modelimizi oluşturmaya başlıyoruz. öncelikle bir title oluşturacağız. buraya yapacağımız assignment gelecek. daha sonra bu assignment için bir description alanı oluşturacağız. TextField description için oldukça uygun.
- assignment için bir priority belirlememiz gerekiyor.şimdilik charfield verelim.
- isCompleted ile bir booleanfield oluşturacağız. true ya da false ile görevin tamamlanıp tamamlanmadığını görebileceğiz.
- görevin oluşturma zamanı ve güncellenme zamanını belirteceğiz. burada dikkat etmemiz gereken nokta şu: datetimefield 2 tane olacak fakat içerisine alacağı değer birinde auto_now=true, diğerinde ise auto_now_add=true.
- bu küçük fark oluşturma ve değiştirme tarihini ayrı şekilde bize göstermeye yarayacak.
- priority kısmına geri dönelim. bir tupple ile önceliği yazıya dökeceğiz. böylece standart bir önceliklendirmemiz olacak. priority'nin field optionsuna choices ekleyerek bu tupple'ı seçilebilir hale getirdik.
- str(self) metoduyla da database'de nasıl görmek istediğimizi belirttik. eğer bu işlemi yapmaz ise giriş yapacağımız her item database'de "todo object" olarak görüntülenecek.
- database'e yeni bir giriş yaptığımız için makemigrations ve migrate işlemlerini uyguladık.

```py
# models.py
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

    def __str__(self):
        return self.title
```

- admin.py

- bu oluşturduğumuz tabloyu adminboard'da görmek için register işlemi yapıyoruz. register işlemini de gerçekleştirdikten sonra bir superuser oluşturalım ve database'imizi kontrol edelim.
- python manage.py createsuperuser

```py
from django.contrib import admin
from .models import Todo

# Register your models here.

admin.site.register(Todo)
```


- database tarafında hazırladığımız bu app'i şimdi frontende yansıtmak için view-template-url üçlüsünü kullanacağız. şimdi yapacağımız işlemler aslında tamamen Crud işlemi. bu dört işlem için ayrı ayrı fonksiyonlar yazacağız, hepsi için template'lerini oluşturacağız ve templateleri urlpattern'e ekleyeceğiz.

- views.py:
- öncelikle oluşturduğumuz modeli import edelim. listelemek için function-based bir view oluşturacağız. bizim için öncemli 3 husus var. request, template_name ve context. fonksiyonumuz bir request alacak. bir değişken oluşturacağız ve models'dan gelen Todo objesi içerisindeki bütün verileri bu değişkene aktaracağız.
contextimizi oluşturacağız ve bu dictionary içerisine bu değişkeni yerleştireceğiz. son olarak da fonksiyonumuz bize bir render return edecek. bu render içerisinde - request,template_name ve context olacak.
```py
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    context = {
        'todos' : todos
    }
    return render(request, 'todo_list.html', context)
```

- todo_list.html:
- dosyamızı templates/todo içerisine oluşturduk ve base.html'i extend ettik. block'umuzu(base.html dosyasında content ismine sahipti) oluşturduk. bu block içerisine de 'todo_list' isimli veiw'imizde oluşturduğumuz context'i yerleştirdik(todos).

```html
{% extends 'todo/base.html' %} 
{% block content %}
{{ todos }}
{% endblock content %}
```






