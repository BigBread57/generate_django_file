from django.utils.translation import gettext_lazy as _
from drf_nova_router.api_router import ApiRouter
from rest_framework.routers import APIRootView

from {{path_to_app}}.api.views import (
    {{Answer}}ViewSet,
)


class {{AppName}}APIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = _('Приложение')
    name = _({{app_name}})


router = ApiRouter()

router.APIRootView = {{AppName}}APIRootView
router.register('question', QuestionViewSet, 'question')
router.register('answer', AnswerViewSet, 'answer')
router.register('quiz', QuizViewSet, 'quiz')
router.register('quiz-key', QuizKeyViewSet, 'quiz-key')
router.register('quiz-key-element', QuizKeyElementViewSet, 'quiz-key-element')
router.register('quiz-step', QuizStepViewSet, 'quiz-step')
router.register('recommendation', RecommendationViewSet, 'recommendation')
