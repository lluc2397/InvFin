from django import forms
from .models import (
    Question,
    Answer
)

class CreateQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = [
            'author',
            'created_at',
            'slug',
            'created_at',
            'updated_at',
            'total_votes',
            'total_views',
            'times_shared',
            'is_answered',
            'has_accepted_answer',
            'tags',
            'category']
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if title.endswith('?') == False:
            raise forms.ValidationError("Añade puntuación a tu pregunta ¿ ?")

        if len(title) < 10:
            raise forms.ValidationError("Formula tu pregunta para que la comunidad pueda ayudarte")
        
        if title == '¿Cuál es tu pregunta?':
            raise forms.ValidationError("Formula tu pregunta para que la comunidad pueda ayudarte")
        return title
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise forms.ValidationError("Detalla precisamente tu pregunta para que la comunidad pueda ayudarte.")
        return content


class CreateAnswerForm(forms.ModelForm):
    content = forms.Textarea()
    class Meta:
        model = Answer
        exclude = [
            'author',
            'created_at',
            'question_related',
            'created_at',
            'is_accepted',
            'total_votes']