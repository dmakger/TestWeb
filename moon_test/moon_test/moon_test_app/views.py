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


def get_result_group(test_id):
    test_results = ResultTest.objects.filter(test_id=test_id)

    # Делим всех по группам
    groups = dict()
    for obj in test_results:
        if obj.group not in groups:
            groups[obj.group] = {
                'amount': 0,
                'result': 0
            }
        groups[obj.group]['amount'] += 1
        groups[obj.group]['result'] += obj.result

    # Узнаем среднее арифметическое, т.е result
    for group in groups:
        groups[group]['result'] = round(groups[group]['result'] / groups[group]['amount'], 2)
    # Получаем отсортированный список кортежей по result
    sorted_groups = sorted(groups.items(), key=lambda x: x[1]['result'], reverse=True)
    
    # Формируем список словарей группы
    result_groups = list()
    count = 1
    for group in sorted_groups:
        result_groups.append({
            'number': count,
            'name_group': group[0],
            'number_of_users': group[1]['amount'],
            'result': group[1]['result']
        })
        count += 1
    return result_groups


class TestDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        test = get_object_or_404(Test, url=slug)
        result_groups = get_result_group(test.id)

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
        print('---')
        print(questions)
        print(a_true)
        print('---')
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
        # result = [key for key in sorted(request.POST.keys()) if key[0].isdigit()]
        result = [key for key in sorted(request.POST.values()) if key[0].isdigit()]
        print("Ответы пользователя: ", result)

        # Формируем список правельных ответов
        test = get_object_or_404(Test, url=slug)
        a_true = list()
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
        print("Правильные ответы: ", a_true)

        n_answer_true = 0
        for answer in result:
            if answer in a_true:
                n_answer_true += 1
        print("Кол-во правильных ответов: ", n_answer_true)
        percent_true_answer = round(n_answer_true/len(a_true) * 100, 2)
        print("В процентном соотношении: ", percent_true_answer)
        print('---')

        
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
        #     # Если новый результат лучше прежнего, обновляем данные
        #     if percent_true_answer > result_test.result:
        #         result_test.result = percent_true_answer

        # Если десятичние числа равны 0, то приводим к int
        if result_test.result == int(result_test.result):
            result_test.result = int(result_test.result)
        print(result_test)
        result_test.save()
        return render(request, 'moon_test_app/test_result.html', context={
            'test': test,
            'result_test': result_test,
            'all_result_test': get_result_group(test.id)
        }) 
        
