# YOTA
Автоматическое продление бесплатной скорости на 64 kbit/s (везде по-разному. В Ставропольском крае, например, 128 kbit/s)

Где-то в конце 2020 года Yota изменила алгоритм продления бесплатного доступа на минимальной скорости. Все написанные до этого скрипты перестали работать

Настроил периодический запуск раз в минуту на роутере Zyxel Keenetic

--
UPD by sadnix (sadnix@gmail.com):

Updated yota.py script for exec with python2.x (verified with python2.7).

On Debian10 installed pkg dependencies for python2.x (verified with python2.7):

# apt install python-requests
# apt install python-tz
# apt install python-pathlib

