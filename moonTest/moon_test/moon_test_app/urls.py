from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import MainView, TestDetailView, TestQuestionsView, SignUpView, SignInView, TestResultView


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('tests/<slug>/', TestDetailView.as_view(), name='test_detail'),
    path('tests/<slug>/test', TestQuestionsView.as_view(), name='test_qa'),
    path('tests/<slug>/result', TestResultView.as_view(), name='test_result')
    # path('tests/<slug>/result', TestResultView.as_view(), )
]