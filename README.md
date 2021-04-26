# RU: Pure Python скрипт для обновления аддонов с GitHub

Положить в папку World of Warcraft рядом с Wow.exe

**C:\World Of Warcraft 3.3.5a\\**

Скрипт автоматически забекапит(сохранит) обновляемый аддон в отдельную папку и скачает свежую версию с указанной ветки (master по ум.)

Хранится 3 последних бекапа чтобы не забивать дисковое пространство

**При отсутствии конфиг-файла обновляет только DBM-wowcircle, конфиг repo_config.conf кладём в ту же папку**

При запуске ничего не указывать, просто запустить двойным щелчком или из консоли

```./update_DBM.exe```

Скачать .exe файл можно во вкладке "Releases"

## ОБЯЗАТЕЛЬНО ПЕРЕИМЕНОВАТЬ ПРИМЕР repo_config.conf.sample в repo_config.conf ИНАЧЕ КОНФИГ НЕ БУДЕТ РАБОТАТЬ!

Пример конфиг-файла есть в репозитории, нужно указать через запятую на каждой строке:

```Владелец репозитория, название репозитория, ветка, регулярное выражение для копирования нужных папок(или список папок разделенный | )```

Пример для моего репозитория, много папок DBM-..., регулярное выражение будет DBM-.+

```Barsoomx, DBM-wowcircle, master, DBM-.+```

Пояснение:

Токен `.` соответствует любому символу (кроме терминаторов строк)

`+` повторяет токен `.` от одного до неограниченного числа раз, столько раз, сколько возможно (жадно)

Пример с wildcard (Есть папка Details и папки Details-...)

```Bunny67, Details-WotLK, master, Details.*```

Пояснение:

Токен `.` соответствует любому символу (кроме конца строки)

`*` повторяет токен `.` от нуля до неограниченного числа раз, столько раз, сколько возможно (жадно) 

Пример для двух папок (В ElvUI много аддонов, чтобы не удалить лишнее нужно указать конкретные папки разделяя их | )

```ElvUI-WotLK, ElvUI, master, ElvUI|ElvUI_OptionsUI```

Конфиг-файл поддерживает комментарии, пропуская строки начинающиеся с `#`

```# Bunny67, Details-WotLK, master, Details.*``` - такая строка будет пропущена

# EN: Pure Python updater for GitHub-based AddOns

Place the executable into WoW root folder, near Wow.exe

**C:\World Of Warcraft 3.3.5a\\**

The script will automatically backup (save) the addon being updated to a separate folder and download the latest version from the specified branch (master by default) 

Only the last 3 backups are stored so as not to clog up disk space

** If there is no config file, it updates only DBM-wowcircle, put the repo_config.conf config in the same folder **

Do not specify any arguments at startup, just double click or launch from cmd

```./update_DBM.exe```

You can download standalone executable file in the "Releases" tab 

## IT IS MANDATORY TO RENAME THE EXAMPLE repo_config.conf.sample TO repo_config.conf OTHERWISE THE CONFIG WILL NOT WORK! 

An example of a config file is in the repository, for every repository you need to specify these parameters separated by commas on each line(1 line = 1 repository):

``` Repository owner, repository name, branch, regex to copy the desired folders (or a list of folders separated by |) ```

An example for my repository, many folders named DBM-..., regex would be DBM-.+

```Barsoomx, DBM-wowcircle, master, DBM-.+```

Explanation:

Token `.` matches any character (except for line ending)

`+` matches the previous token between one and unlimited times, as many times as possible (greedy)

An example with wildcard (there is a Details folder AND Details-... folders, hence the need to .* )

```Bunny67, Details-WotLK, master, Details.*```

Explanation:

Token `.` matches any character (except for line ending)

`*` matches the token (.) between zero and unlimited times, as many times as possible (greedy)

An example for two folders (ElvUI has a lot of add-ons, in order not to delete unnecessary folders you need to explicitly specify required folders separating them with | )

```ElvUI-WotLK, ElvUI, master, ElvUI|ElvUI_OptionsUI```

The config file supports comments, skipping lines starting with `#`

```# Bunny67, Details-WotLK, master, Details.*``` - this line will be skipped















# Executable compilation on **Windows**

```bash
python -m pip install -r requirements.txt

python -m pip install pyinstaller

pyinstaller update_DBM.py --onefile -y
```

