from nova_quiz.api.views.answer import AnswerViewSet
from nova_quiz.api.views.question import QuestionViewSet
from nova_quiz.api.views.quiz import QuizViewSet
from nova_quiz.api.views.quiz_key import QuizKeyViewSet
from nova_quiz.api.views.quiz_key_element import QuizKeyElementViewSet
from nova_quiz.api.views.quiz_step import QuizStepViewSet
from nova_quiz.api.views.recommendation import RecommendationViewSet

__all__ = [
    'AnswerViewSet',
    'QuestionViewSet',
    'QuizViewSet',
    'QuizKeyViewSet',
    'QuizKeyElementViewSet',
    'QuizStepViewSet',
    'RecommendationViewSet',
]
