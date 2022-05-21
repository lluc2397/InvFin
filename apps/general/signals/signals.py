from django.db.models import signals

from apps.public_blog.models import PublicBlog
from apps.preguntas_respuestas.models import Question, Answer, QuesitonComment, AnswerComment
from .handlers import NotificationSystemSignals

# signals.post_save.connect(NotificationSystemSignals.update_destination_metrics, sender=PublicBlog)

# signals.post_save.connect(NotificationSystemSignals.update_destination_metrics, sender=Question)
# signals.post_save.connect(NotificationSystemSignals.update_destination_metrics, sender=Answer)
# signals.post_save.connect(NotificationSystemSignals.update_destination_metrics, sender=QuesitonComment)
# signals.post_save.connect(NotificationSystemSignals.update_destination_metrics, sender=AnswerComment)
