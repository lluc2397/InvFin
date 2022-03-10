from django.shortcuts import render,redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import (
	ListView,
	View,
	DetailView,
	CreateView,
	UpdateView)

from apps.general.models import Tag
from apps.general.tasks import prepare_notifications_task

from .models import (
    Question,
    Answer
)

from .forms import (
	CreateQuestionForm
)

class QuestionsView(ListView):
	model = Question
	template_name = 'preguntas_respuestas/inicio.html'
	context_object_name = "questions"
	ordering = ['-created_at']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["meta_desc"] = 'Haz una pregunta o responde a la comunidad para conseguir premios increíbles'
		context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
		context["meta_title"] = 'Resuelve tus dudas o ayuda a otros'
		context["meta_url"] = '/preguntas/'
		return context


class QuestionDetailsView(DetailView):
	model = Question
	template_name = 'preguntas_respuestas/details.html'
	context_object_name = "object"
	slug_field = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		model = self.get_object()
		model.total_views += 1
		model.save()
		return context



class CreateQuestionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	form_class = CreateQuestionForm
	template_name = 'preguntas_respuestas/forms/create_question.html'
	success_message = 'Pregunta creada'

	def get_context_data(self, **kwargs):
		context = super(CreateQuestionView, self).get_context_data(**kwargs)
		return context

	def get_initial(self, *args, **kwargs):
		initial = super(CreateQuestionView, self).get_initial(**kwargs)
		initial['title'] = '¿Cuál es tu pregunta?'
		initial['content'] = 'Explica tu duda con todo lujo de detalles'
		return initial

	def form_valid(self, form):
		
		form.instance.author = self.request.user
		tags = self.request.POST['tags'].split(',')
		selfanswer = self.request.POST['selfanswereditor']
		modelo = form.save()
		modelo.add_tags(tags)
		if selfanswer !='':
			modelo.add_answer(selfanswer)
			modelo.is_answered = True
			modelo.has_accepted_answer = True
		
		prepare_notifications_task.delay(modelo, 4)
		return super().form_valid(form)
	
	def form_invalid(self, form):
		return super().form_invalid(form)


class UpdateQuestionView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Question
	template_name = 'preguntas_respuestas/forms/update_question.html'
	context_object_name = "question"
	slug_field = 'slug'

	fields = ['content']
	success_message = 'Pregunta actualizada'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def test_func(self):
		valid = False
		if self.get_object().author == self.request.user:
			valid = True
		elif self.request.user.is_superuser:
			valid = True
		return valid

	def handle_no_permission(self):
		return redirect("preguntas_respuestas:list_questions")


@login_required
def create_answer_view(request, slug):
	if request.method == 'POST':
		question = Question.objects.get(slug = slug)
		answer = Answer.objects.create(
		content = request.POST['content'],
		author = request.user,	
		question_related = question
		)
		question.is_answered = True
		question.save()
		messages.success(request, 'Gracias por tu respuesta')
		return redirect(question.get_absolute_url())


@login_required
def accept_answer(request, question_id, answer_id):
	question = Question.objects.get(id = question_id)
	if request.user == question.author and question.has_accepted_answer == False:
		answer = Answer.objects.get(id = answer_id)
		if question.is_answered == False:
			question.is_answered = True
		
		question.has_accepted_answer = True
		question.save()
		answer.is_accepted = True
		answer.save()
		answer.author.update_reputation(2)
		messages.success(request, 'Gracias por tu ayuda')
	return redirect(question.get_absolute_url())