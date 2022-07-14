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
    return render(request, 'todo/todo_list.html', context)
```

- todo_list.html:
- dosyamızı templates/todo içerisine oluşturduk ve base.html'i extend ettik. block'umuzu(base.html dosyasında content ismine sahipti) oluşturduk. bu block içerisine de 'todo_list' isimli veiw'imizde oluşturduğumuz context'i yerleştirdik(todos).

```html
{% extends 'todo/base.html' %} 
{% block content %}
{{ todos }}
{% endblock content %}
```

- urls.py
- todo_list viewimizi import ettik ve urlpattern'e link adını vererek girdik.

```py
from .views import todo_list

urlpatterns = [
    path("list/", todo_list, name="list")
]
```

- http://127.0.0.1:8000/list/ adresine girdiğimizde bize querylist olarak eklediğimiz görevleri listeleyecek. tekrar template dosyamıza dönüp bunu biraz daha kullanıcının anlayacağı şekle çevireceğiz. 
- bir for döngüsü kullanarak listeleyeceğiz ve daha güzel bir görüntü ortaya çıkacak. 

```html
{% extends 'todo/base.html' %} 
{% block content %}

<h2>TODO List</h2>
<hr />
<ul>
    {% for todo in todos %}

    <li>{{todo}}</li>
    {% endfor %}
</ul>

{% endblock content %}
``` 

- forms.py:
- database'de bir veri oluşturabilmek için bir form'a ihtiyacımız var. Django'nun bize sağladığı kolaylıklardan biri de database'de oluşturduğumuz bir modeli form olarak kullanmamızı sağlamak. yani sıfırdan form yazmak yerine daha önce oluşturduğumuz model'ı form olarak kullanacağız.
- bir class tanımlıyoruz ve içerisine Meta class'ı ile kullanacağımız model'in ismini ve kullanılacak alanları giriyoruz.

```py
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'
```

- views.py:
- create işlemimizi gerçekleştirelim. form isminde bir değişken oluşturduk ve forms.py'dan import ettiğimiz TodoForm()'u bu değişkene atadık. sırada bir if yapısı kurarak kontrol sağlamamız gerekiyor. create işlemi bir POST methodudur. eğer gelen request POST ise form değişkeni içerisine request.POST ile gelen verileri eşitleyeceğiz. bu kontrol içerisinde bir if döngüsü daha olacak. bu da validation işlemi yani form.is_valid() olacak. eğer form valid ise form.save() ile değişkenimiz yani form son halini alacak. ardından return ile redirect etmek istediğimiz sayfaya götürecek.
- kontroller sağlandıktan sonra ise bize 'form' adını verdiğimiz contexti oluşturacak ve yeni oluşturacağımız template'i render edecek.

```py
from .forms import TodoForm

def todo_create(request):
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('list')
    context = {
        'form' : form
    }
    return render(request, 'todo/todo_add.html',context)

```

- todo_add.html:
- template'imizi oluşturduk. extend ve block işlemlerinden sonra bloğumuzun içerisine method'u POST bir html formu yerleştirdik. formumuzun içerisine django'nun veri girişini sağlaması için gereken csrf_token'i yerleştirdik. daha sonra view'de oluşturduğumuz context olan form'u koyduk ve bir submit inputu oluşturduk.

```html.py
{% extends 'todo/base.html' %} 
{% block content %}

<h2>TODO Add</h2>
<hr />

<form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Add">

</form>

{% endblock content %}

```

- urls.py:
- view'de oluşturduğumuz todo_create'i buraya import ettik ve urlpattern'e yerleştirdik.

- views.py:
- sıradaki işlemimiz update. öncelikle Todo modelimiz içerisinden id'si "id" olan bir obje çekeceğiz ve bunu bir değişkene atayacağız.
- bir form oluşturacağız ve bu formun içine TodoForm()'u koyacağız. fakat TodoForm'un instance'ı az önce oluşturduğumuz değişkene atıyoruz.
- artık yapacağımız işlem create işlemi ile aynı. bir if döngüsü ile create için yaptığımız işlemlerin aynısını burada da yapıyoruz. tek fark request.POST ile instance=todo'yu karşılaştırması. ikisini karşılaştırdıktan sonra instance=todo'dan gelen verilerle override ediyor. tekrar validasyon işlemi ve redirect işleminden sonra fonksiyondan çıkıyor.
- yine ek olarak context'imiz içerisine todo haricinde form'u koyuyoruz.

```py 
def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
        return redirect('list')

    context = {
        'todo': todo,
        'form': form
    }
    return render(request, 'todo/todo_update.html', context)
```

- todo_update.html:
- extend ve block işlemini yaptıktan sonra block içerisine update'ten sonra görmek istediğimiz verileri giriyoruz. örneğin: todo.title ve todo.description.
- update işlemi aynı zamanda bir create işlemidir. yine Post methodu gelecek ve var olanı değiştireceği için todo_add.html içerisindeki html formunu bu template'in içerisine koymamız gerekiyor.
- view kısmında zaten bunu göstermiştik. context todo(title ve description'ı gösteren bölüm) ve form olmak üzere iki öğreye sahipti.

```html.py
{% extends 'todo/base.html' %} 
{% block content %}

<h2>TODO Update</h2>
<hr />

{{ todo.title}}
{{ todo.description}}

<form action="" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Update">

</form>

{% endblock content %}

```

- urls.py:
- view'de oluşturduğumuz todo_update'i buraya import ettik ve urlpatterne yerleştirdik. fakat ufak bir fark var. "update" linki bir id alır. bunu göstermek zorundayız:

```py
from .views import todo_update

urlpatterns = [
    path("update/<int:id>/", todo_update, name="update")
]
```

- views.py:
- delete işlemi gerçekleştireceğiz. update işlemindeki gibi todo değişkeni atadık ve Todo objesi içerisinden id'si "id" olan bir veriyi aldık. if döngüsü ile method eğer 'POST' ise oluşturduğumuz değişkeni delete() dedikten sonra 'list'e redirect ettik.
- context'imize de görmek istediğimiz todo'yu yani yukarıda aldığımız veriyi yerleştirdik.

```py
def todo_delete(request, id):
    todo = Todo.objects.get(id=id)
    if request.method == 'POST':
        todo.delete()
        return redirect('list')
    context = {
        'todo' : todo
    }
    return render(request, 'todo/todo_delete.html', context)
```

- todo_delete.html:

- update htmli kopyaladık ve bazı değişiklikler yaptık. form'u kaldırdık ve yerine bir mesaj ekledik. mesajın sonuna da {{todo}} yazdık. buradaki amaç database'den çektiği title'ı bize getirmek olacak.

```html
{% extends 'todo/base.html' %} 
{% block content %}

<h2>TODO Delete</h2>
<hr />

{{ todo.title}}
{{ todo.description}}

<form action="" method="POST">
    {% csrf_token %}
    <p>Are you sure to delete {{todo}} </p>
    <input type="submit" value="Yes">

</form>

{% endblock content %}
```

- urls.py
- update ile aynı şekilde int:id vererek linkimizi urlpattern'e ekledik.

- şu an app'imizin iskeleti hazır. fakat kullanışlı değil çünkü linklere adres girerek ulaşıyoruz. örneğin home.html'e bir a tag'i ekleyerek istediğimiz zaman homepage'e dönmemizi sağlayalım. ya da list'e gidelim.

```html
<a href = "{% url 'add' %}">Add</a>
<a href = "{% url 'list' %}">List</a>
```

- ya da list'e girdiğimizde tıkladığımız anda update etmesini sağlayacak linkleri bağlayalım. aslında yapacağımız şey for döngüsü içerisine a tagi koymak ve url olarak "{% url 'update' todo.id %}" vermek.

```html
{% extends 'todo/base.html' %} 
{% block content %}

<h2>TODO List</h2>
<hr />
<ul>
    {% for todo in todos %}

        <a href="{% url 'update' todo.id %}">
    <li>{{todo}}</li>
    </a>

    {% endfor %}
</ul>

{% endblock content %}

```

- şimdi update ve list template'inin içerisine delete fonksiyonu ekleyeceğiz.

```html
<a href="{% url 'delete' todo.id %}">Delete</a>
```