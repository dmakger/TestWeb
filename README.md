# TestWeb

## Запуск Проекта
Чтобы запустить проект, нам нужно запустить виртуальную машину.  
Для этого надо перейти в moon_test/ и прописать команду:
``` bash
source myvenv/bin/activate
```
У вас должна появиться плашка слева **(myvenv)**  
![image](https://user-images.githubusercontent.com/81534024/115144668-8db4cc80-a056-11eb-8cec-7a0180a8d5e4.png)
 
 
 Далее спускаемся еще ниже, а именно в moon_test. 
 Здесь у нас есть файл **manage.py**, его нам как раз и надо запустить.
 Делаем это следующим образом:
 ``` bash
python3 manage.py runserver
```
Вот так должно получится:
![image](https://user-images.githubusercontent.com/81534024/115144754-17649a00-a057-11eb-99eb-9b8233be68f5.png)


Теперь вбиваем в браузере **http://127.0.0.1:8000/** и смотрим на результат:
![image](https://user-images.githubusercontent.com/81534024/115144858-9659d280-a057-11eb-8722-386ef2f34b1b.png)


После завершения работы нажмите <kbd>Ctrl</kbd>+<kbd>C</kbd>, чтобы выключить сервер.  
После этого выключаем виртуальную машину. Для этого введите:
``` bash
deactivate
```

На этом всё.
