from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Prefetch
from django.db.models import Q

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from .models import Salones, Student, Materias, Calificacion
from .forms import CalificacionForm, LoginForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

######### Seccion de menu / index / login #########
def intro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'menu.html')
    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')

class MyLogoutView(LogoutView):
    next_page = 'index'


######### Seccion de salones #########
class SalonesListView(ListView):
    
    model = Salones
    template_name = 'salones_list.html'
    context_object_name = 'salones'

    def get_queryset(self):
        return Salones.objects.all().order_by('grado')

class SalonesCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'adminacad.add_salones'
    model = Salones
    template_name = 'salones_form.html'
    fields = ['salon', 'grado', 'profesor']
    success_url = reverse_lazy('salones_list')

    def handle_no_permission(self):
        message = 'Importante'
        context = {'message': message}
        return render(self.request, 'sinacceso.html', context)

class SalonesDetailView(DetailView):
    model = Salones
    template_name = 'salones_detail.html'
    context_object_name = 'salones'
    success_url = reverse_lazy('salones_list')

class SalonesUpdateView(UpdateView):
    model = Salones
    template_name = 'salones_form.html'
    fields = ['salon', 'grado', 'profesor']
    success_url = reverse_lazy('salones_list')

class SalonesDeleteView(DeleteView):
    model = Salones
    template_name = 'salones_confirm_delete.html'
    success_url = reverse_lazy('salones_list')


######### Seccion de students #########
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student_list.html'
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Student.objects.filter(Q(nombre_est__icontains=query) | Q(apellido_est__icontains=query)| Q(identificacion__icontains=query))
        else:
            return Student.objects.all().order_by('identificacion')


class StudentCreateView(LoginRequiredMixin,CreateView):
    model = Student
    fields = ['nombre_est', 'apellido_est', 'salon', 'identificacion', 'grado']
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'
    context_object_name = 'student'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['nombre_est', 'apellido_est', 'salon', 'identificacion']
    template_name = 'student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('student_list')


######### Seccion de materias #########
class MateriasListView(ListView):
    model = Materias
    template_name = 'materias_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Materias.objects.filter(Q(nombre_materia__icontains=query) | Q(clave_materia__icontains=query))
        else:
            return Materias.objects.all().order_by('grado')

class MateriasCreateView(CreateView):
    model = Materias
    fields = ['nombre_materia', 'clave_materia', 'grado']
    template_name = 'materias_form.html'
    success_url = reverse_lazy('materias_list')

class MateriasUpdateView(UpdateView):
    model = Materias
    fields = ['nombre_materia', 'clave_materia', 'grado']
    template_name = 'materias_form.html'
    success_url = reverse_lazy('materias_list')

class MateriasDeleteView(DeleteView):
    model = Materias
    template_name = 'materias_confirm_delete.html'
    success_url = reverse_lazy('materias_list')

######### Seccion de calificaciones #########
def calificacion_list(request):
    calificaciones = Calificacion.objects.all()
    return render(request, 'calificacion_list.html', {'calificaciones': calificaciones})

def calificacion_detail(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    return render(request, 'calificacion_detail.html', {'calificacion': calificacion})

def calificacion_new(request):
    if request.method == "POST":
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save()
            return redirect('materias_list')
    else:
        materia_pk = request.GET.get('materia')
        estudiante_pk = request.GET.get('estudiante')
        form = CalificacionForm(initial={'materia': materia_pk, 'identificacion': estudiante_pk})
    return render(request, 'calificacion_new.html', {'form': form})

def calificacion_edit(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == "POST":
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.save()
            return redirect('studentmateria', materia_clave=calificacion.materia.clave_materia)

    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificacion_edit.html', {'form': form})

def calificacion_delete(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    calificacion.delete()
    return redirect('calificacion_list')

def studentmateria(request, materia_clave, ):
    # Find the Materias object with the given clave_materia
    materia = Materias.objects.get(clave_materia=materia_clave)

    # Retrieve the nombre_materia value from the Materias object
    nombre_materia = materia.nombre_materia

    # Retrieve the students associated with the given Materias object
    #students = materia.grado.students.prefetch_related('calificacion_set').all()
    students = materia.grado.students.prefetch_related(
        Prefetch('calificacion_set', queryset=Calificacion.objects.only('calif_1B', 'calif_2B', 'calif_3B', 'calif_4B', 'calif_5B'))
    ).all()

    # Render the template with the list of students and their calificaciones
    return render(request, 'studentmateria.html', {'materia': materia, 'nombre_materia': nombre_materia, 'students': students})
