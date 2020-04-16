# Telegram bot + парсер сайта - wildberries.ru

Программа скачивает данные с сайта - [wildberries](https://www.wildberries.ru/) по заданным параметрам и выводит их в телеграм - бот.

## Требования

Должен быть установлен Python3 на Linux или Windows.

#### Установка

##### На Linux

1.Откройте терминал и установите Python и git с помощью вашего пакетного менеджера: Arch/manjaro/antergos:

```pacman -S git python --needed```

Ubuntu/Debian/Deepin/any_apt_based:

 ```apt install git python```

Fedora:

 ```yum install git python```
 
2.Склонируйте репозиторий при помощи git и перейдите в папку:
```
git clone https://github.com/emez3siu/b0mb3r.github.io
cd b0mb3r
```

3.Установите зависимости:

```python -m pip install -r requirements.txt```

4.Запустите ПО:

```python main.py```

5.Если в вашем браузере не открылся веб-интерфейс, перейдите по ссылке в терминале.

##### На Windows

1.Установите Python версии не ниже 3.6, скачав установщик с официального сайта.

2.Установите git для Windows, скачав его отсюда.

3.Откройте командную строку и склонируйте репозиторий при помощи git и перейдите в папку:
```
git clone https://github.com/emez3siu/b0mb3r.github.io
cd b0mb3r
```

4.Установите все необходимые библиотеки и запустите скрипт:
```
python -m pip install -r requirements.txt
python main.py
```

5.Если в вашем браузере не открылся веб-интерфейс, перейдите по ссылке в консоли.

## Запуск

###### Аргументы для запуска в консоле:

* ```--min_price'``` - минимальная цена товара
    * ```python main.py --start_page 1000```

* ```--active_min_price``` - использовать параметр минимальной цены
    * ```python main.py --active_min_price True```


###### Команда для запуска парсера в консоле:

``` bash python main.py ```


### После запуска

Телеграм бот выдаст список товаров по минимально выбранной цене.
