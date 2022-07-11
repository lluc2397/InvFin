from config import celery_app
from django.apps import apps


from apps.empresas.models import Company
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.escritos.models import Term


@celery_app.task()
def post_promotion():
    pass


# @celery_app.task()
def clean_journeys():
    for user_journey_model in ['User', 'Visiteur']:
        model = apps.get_model(app_label='seo', model_name=f'{user_journey_model}Journey')
        for journey in model.objects.filter(parsed=False):
            path = journey.current_path
            splited_path = path.split('/')
            if len(splited_path) > 3:
                
                splited_path = splited_path[-3:-1]
                if splited_path[1].startswith('?utm'):
                    info = splited_path[0]
                else:
                    info = splited_path[1]

                if 'screener/analisis-de' in path:
                    journey_model = 'CompanyVisited'
                    try:
                        model_visited = Company.objects.get(ticker=info)
                    except:
                        continue

                elif '/p/' in path:
                    journey_model = 'PublicBlogVisited'
                    try:
                        model_visited = PublicBlog.objects.get(slug=info)
                    except:
                        continue

                elif '/question/' in path:
                    journey_model = 'QuestionVisited'
                    try:
                        model_visited = Question.objects.get(slug=info)
                    except:
                        continue

                elif 'definicion' in path:
                    journey_model = 'TermVisited'
                    try:
                        model_visited = Term.objects.get(slug=info)
                    except:
                        continue
                else:
                    continue

                apps.get_model(
                    app_label='seo', 
                    model_name=f'{user_journey_model}{journey_model}'
                ).objects.create(
                    user=journey.user,
                    visit=journey,
                    model_visited=model_visited,
                    date=journey.date
                )
                
                journey.parsed = True
                journey.save(update_fields=['parsed'])
