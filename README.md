# [Корпус Порошков](https://nlpproject2023.pythonanywhere.com/)
Корпус создан на основе материалов паблика [Порошки](https://vk.com/sandalporoshki).

Размер корпуса составляет **14463** слов.

Порошки (a.k.a. стишки-порошки) — малый поэтический интернет-жанр. Мы собрали тексты 1000 порошков и реализовали поиск по ним:

* поиск по точной форме (в двойных кавычках)
* поиск по лемме или словоформе (без кавычек)
* поиск по части речи (использованы [частеречные теги pymorphy2](https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html))
* возможен комбинированный поиск n-грамм через пробел

Корпус собран в виде таблиц в формате `.csv` и находится в папке /instances. Структура таблиц следующая:

* text_id.csv: содержит поля 'id' (id поста используется как id текста), 'text' (сам текст порошка), 'datetime' (дата и время публикации порошка), 'authors' (ники авторов), 'year_of_creation' (год написания текста, если есть)
* word_id.csv: содержит поля 'id' (уникальный идентификатор слова), 'word' (сама словоформа)
* lemma_id.csv: содержит поля 'id' (уникальный идентификатор леммы), 'lemma' (сама лемма)
* word_to_lemma.csv: содержит поля 'word_id'	(id словоформы), 'lemma_id' (id леммы)
* word_data.csv: содержит поля 'text_id' (id текста),	'lemma'	(лемма), 'tag' (POS-тэг словоформы), 'word_id' (id словоформы),	'text_pos' (позиция словоформы в тексте)
* author_id.csv: 'author_id' (id автора во ВКонтакте), 'author_name' (ник/имя автора)

Сайт опубликован через платформу *pythonanywhere*. 

Воспользоваться корпусом можно по ссылке: https://nlpproject2023.pythonanywhere.com/

Проект подготовлен студентами 3 курса НИУ ВШЭ ФиКЛ: Таисия Тренихина, Ярослав Соколов, Арина Замышевская, Анастасия Добрынина.
