INSERT INTO public.courses ("name",code) VALUES
	 ('Прикладная информатика','09.03.03'),
	 ('Психолого-педагогическое образование','44.03.02'),
	 ('Туризм ','43.03.02'),
	 ('Юриспруденция ','40.03.01'),
	 ('Бизнес-информатика','38.03.05'),
	 ('Государственное и муниципальное управление','38.03.04'),
	 ('Экономика ','38.03.01');
INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (4,1),
	 (6,1),
	 (8,1),
	 (9,1),
	 (10,1),
	 (13,1),
	 (1,2),
	 (4,2),
	 (6,2),
	 (8,2);
INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (9,2),
	 (10,2),
	 (1,3),
	 (1,4),
	 (1,7),
	 (1,8),
	 (1,9),
	 (1,10),
	 (1,11),
	 (1,12);
INSERT INTO public.courses_modules (course_id,module_id) VALUES
	 (1,13),
	 (1,1),
	 (1,14);
INSERT INTO public.exercise (title,"order",another_data,theme_id,type_id) VALUES
	 ('Применение глагола',0,'{"content": [{"type": "text", "data": "Глагол to be играет важную роль в английской грамматике. Точнее сказать, роли: это и самостоятельный глагол, и вспомогательный, и глагол-связка. Без глагола to be не получится построить предложения в пассивном залоге и во временах группы Continuous. Кроме того, to be входит в состав некоторых конструкций и фразовых глаголов."}]}',1,5),
	 ('Произношение глагола',1,'{"content": [{"type": "text", "data": "Глагол to be имеет разные формы произношения в зависимости от времени и лица: в настоящем времени это am [æm], is [ɪz] и are [ɑ:]; в прошедшем — was [wɒz] и were [wɜː]; а в прошедшем совершенном времени добавляется форма been [biːn]."}]}',1,5),
	 ('Прослушайте запись',2,'{"path": "./media/audio/"}',1,3),
	 ('______ you our new teacher? ',3,'{"success_answer": "are"}',1,1),
	 ('I ____ a student.',4,'{"answers": ["am", "is", "have", "go"], "success_answer": "am"}',1,2);
INSERT INTO public.exercise_type ("name") VALUES
	 ('Недостающее слово'),
	 ('Правильный вариант'),
	 ('Аудио'),
	 ('О чем говорится в тексте'),
	 ('Теория');
INSERT INTO public.langs ("name",short_name) VALUES
	 ('Английский','🇬🇧'),
	 ('Французский','🇨🇵'),
	 ('Немецкий','🇩🇪');
INSERT INTO public.modules ("name",lang_id) VALUES
	 ('Beginner (A1)',2),
	 ('Pre-Intermediate (A2)',2),
	 ('Intermediate (B1)',2),
	 ('Upper-Intermediate (B2)',2),
	 ('Advanced (C1)',2),
	 ('Уровень А1 (Anfänger)',1),
	 ('Уровень А2 (Grundlagen)',1),
	 ('Уровень В1 (Aufbau 1)
',1),
	 ('Уровень B2 (Aufbau 2)',1),
	 ('Уровень С1 (Fortgeschrittene 1)',1);
INSERT INTO public.modules ("name",lang_id) VALUES
	 ('Уровень С2 (Fortgeschrittene 2)',1),
	 ('Модуль 1',3),
	 ('Модуль 2',3);
INSERT INTO public.roles (id,"name") VALUES
	 (1,'Ученик'),
	 (2,'Преподаватель'),
	 (3,'Администратор');
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Глагол to be',0,1),
	 ('Типы предложений',0,1),
	 ('Артикли',0,1),
	 ('Описательный оборот there is/are',0,1),
	 ('Порядок слов в вопросительных предложениях',0,2),
	 ('Притяжательные местоимения mine, his, hers, its, yours, ours, theirs

',0,2),
	 ('Предлоги времени in, on, at

',0,2),
	 ('Something/anything/nothing

',0,2),
	 ('Глаголы состояния

',0,3),
	 ('Придаточные определительные предложения с that/who/which/where

',0,3);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Герундий',0,3),
	 ('Модальные глаголы have to, must, should, may, might

',0,3),
	 ('Нулевой артикль

',0,4),
	 ('Предположения с модальными глаголами can’t, might, must

',0,4),
	 ('Квантификаторы a little/little, a few/few, plenty of/a lot of, all, every, both, no/none, most

',0,4),
	 ('Косвенные вопросы

',0,4),
	 ('Модальные глаголы в прошедшем времени

',0,5),
	 ('Условные предложения смешанного типа

',0,5),
	 ('Обратный порядок слов в предложении

',0,5),
	 ('Каузативные глаголы get/have

',0,5);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Алфавит (Alphabet)',0,7),
	 ('Существительные и артикли (Nomen und Artikel)',0,7),
	 ('Личные местоимения (Personalpronomen)',0,7),
	 ('Глаголы: настоящее время (Verben: Präsens)',0,7),
	 ('Настоящее время (Präsens)',0,8),
	 ('Совершенное время (Perfekt)',0,8),
	 ('Сравнительные союзы (Vergleichssätze)',0,8),
	 ('Повелительное наклонение (Imperativ)',0,8),
	 ('Глаголы с предлогами (Verben mit Präpositionen)',0,9),
	 ('Условные предложения (Bedingungssätze)',0,9);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Прошедшее время (Perfekt, Präteritum)',0,9),
	 ('Косвенная речь (Indirekte Rede)',0,9),
	 ('Пассивный залог (Passiv)',0,10),
	 ('Относительные предложения (Relativsätze)',0,10),
	 ('Способы выражения будущего времени (Futurformen)',0,10),
	 ('Немецкие падежи (Nominativ, Genitiv, Dativ, Akkusativ)',0,10),
	 ('Герундий и инверсия (Gerundium und Inversion)',0,11),
	 ('Причастные конструкции (Die Partizipialkonstruktionen)',0,11),
	 ('Инфинитивные конструкции (Die Infinitivkonstruktionen)',0,11),
	 ('Различные виды придаточных предложений (Die verschiedenen Arten von Nebensätzen)',0,11);
INSERT INTO public.themes ("name","order",module_id) VALUES
	 ('Степени сравнения (Die Steigerungsformen)',0,12),
	 ('Различные виды сравнений (Komparationen)',0,12),
	 ('Сложные предлоги и союзы (Zusammengesetzte Präpositionen und Konjunktionen)',0,12),
	 ('Различные виды прямой речи (Indirekte Rede)',0,12);
