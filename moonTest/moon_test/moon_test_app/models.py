from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField()
    tag = models.CharField(max_length=50)
    difficult = models.FloatField()
    questions = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class ResultTest(models.Model):
    test_id = models.IntegerField()
    name = models.CharField(max_length=200)
    group = models.CharField(max_length=200)
    result = models.FloatField()

    def __str__(self):
        return f"{self.test_id}_{self.name}_{self.group}_{self.result}"
    
    def get_result_group(self, test_id):
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



class Human(models.Model):
    name = models.CharField(max_length=200)
    group = models.CharField(max_length=200)