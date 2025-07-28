## запуск в окружении разработчика
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## настройка и запуск gunicorn
1. Создать файл `/etc/systemd/system/gunicorn.service`
2. В файл вставляем следующую конфигурацию:
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=your_linux_user
Group=www-data
WorkingDirectory=/path/to/your/project ; путь к django-проекту
ExecStart=/path/to/gunicorn \ ; путь к исполняемому файлу gunicorn
          --access-logfile - \
          --workers 8 \ ; кол-во процессов django-приложения. Рекомендуется установить значение равное кол-ву ядер cpu
          --bind 127.0.0.1:8000 \
          your_project_name.wsgi:application

[Install]
WantedBy=multi-user.target
```
3. Запуск gunicorn. Выполняем команды:
```
sudo systemctl daemon-reexec
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
4. Проверить статус можно командой `sudo systemctl status gunicorn`. При успешном запуске должна быть строка Active: active (running)

## настройка и запуск nginx
1. Устанавливаем nginx командой `sudo apt install nginx`
2. Создаем файл `/etc/nginx/sites-available/sync77` и вставляем следующее:
```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
3. Выполняем команды:
```
sudo ln -s /etc/nginx/sites-available/sync77 /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

Далее можно зайти в приложение введя в адресную строку браузера localhost/upload и localhost/items 