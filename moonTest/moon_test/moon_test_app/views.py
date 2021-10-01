from django.http.response import HttpResponseRedirect
from .forms import SignUpForm, SignInForm
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Test, Human, ResultTest
from django.contrib.auth import login
from django.contrib.auth import authenticate


class MainView(View):
    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        return render( request, 'moon_test_app/home.html', context={
            'tests': tests
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()  # Форма на вход
        return render(request, 'moon_test_app/signup.html', context={
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)  # Форма на регистрацию
        # Если данные валидны
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя в бд
            # Если пользователь существует, то логинем этого пользователя 
            if user is not None:
                human = dict()
                human = Human(
                    name = request.POST['username'], 
                    group = request.POST['group']
                )
                human.save()
                login(request, user)
                return HttpResponseRedirect('/')  # Возращение на главную страницу
        return render(request, 'moon_test_app/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()  # Форма на вход
        return render(request, 'moon_test_app/signin.html', context={
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)  # Форма на регистрацию
        # Если данные валидны
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            # Если пользователь существует, то логинем этого пользователя 
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'moon_test_app/signin.html', context={
            'form': form,
        })


class TestDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        test = get_object_or_404(Test, url=slug)
        result_groups = ResultTest().get_result_group(test.id)

        return render(request, 'moon_test_app/test_detail.html', context={
            'test': test,
            'groups': result_groups
        })


class TestQuestionsView(View):
    def get(self, request, slug, *args, **kwargs):
        test = get_object_or_404(Test, url=slug)
        questions = dict()
        question = dict()
        a_true = dict()
        count = 0
        number = 1
        for row in test.questions.split('\n'):
            if row[-1] == '\r':
                row = row[:-1]
            if row == '':
                questions[number] = question
                question = dict()
                count = -1
                number += 1
            else:
                if count == 0:
                    question['q'] = row
                else:
                    if row[0] == '*':
                        row = row[1:]
                        a_true[number] = count
                    if not question.get('a'):
                        question['a'] = dict()
                    question['a'][count] = row
            count += 1

        if question:
            questions[number] = question
            number += 1
        return render(request, 'moon_test_app/test_qa.html', context={
            'questions': questions,
            'a_true': a_true,
            'test': test,
        })
    

class TestResultView(View):
    def get(self, request, *args, **kwargs):
        test = ResultTest()  # Форма на вход
        return render(request, 'moon_test_app/<slug>/test_result.html', context={
            'test': test,
        })
    
    def post(self, request, slug, *args, **kwargs):
        print('---')
        print(request.POST)
	
        # Получаем список ответов пользователя. (При этом удалив username и csrfmiddlewaretoken)
        result = [key for key in sorted(request.POST.values()) if key != '' and key[0].isdigit()]

        # Формируем список правельных ответов
        a_true = list()
        test = get_object_or_404(Test, url=slug)
        count = 0
        number = 1
        for row in test.questions.split('\n'):
            if row[-1] == '\r':
                row = row[:-1]
            if row == '':
                count = -1
                number += 1
            elif row[0] == '*':
                a_true.append(f"{number}-{count}")
            count += 1

        # Кол-во правельных ответов
        n_answer_true = 0
        for answer in result:
            if answer in a_true:
                n_answer_true += 1
        # Процент правильных ответов
        percent_true_answer = round(n_answer_true/len(a_true) * 100, 2)
        
        # Если незарегистрированный пользователь
        if request.POST['username'] == '':
        	result_test = {
        		'test_id': test.id,
        		'result': percent_true_answer,
        	}
        # Если зарегистрированный пользователь
        else:
        	result_test = ResultTest.objects.filter(name=request.POST['username'], test_id=test.id)
        	print(result_test)
        	# Если пользователь ещё не проходил тест, то регистрируем его
        	if not result_test:
        		print('not')
        		group = Human.objects.filter(name=request.POST['username'])
        		# Пользователь не указал свою группу
        		if not group:
        			group = 'Аноним'
        		# Пользователь указал свою группу
        		else:
        			group = group[0].group
        		result_test = ResultTest(
        			name=request.POST['username'],
        			test_id=test.id,
        			group=group,
        			result=percent_true_answer,
        		)
        	# Пользователь уже проходил тест
        	else:
        		print('yes')
        		result_test = result_test[0]
        		result_test.result = percent_true_answer
        	
        	# Если десятичние числа равны 0, то приводим к int
        	if result_test.result == int(result_test.result):
        		result_test.result = int(result_test.result)
        	result_test.save()
        return render(request, 'moon_test_app/test_result.html', context={
            'test': test,
            'result_test': result_test,
            'all_result_test': ResultTest().get_result_group(test.id)
        }) 
        
