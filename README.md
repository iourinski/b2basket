# b2basket
This is a script that matches categories in two files, where the benchmark file is a csv file like: 

id;Код позиции;Код категории;Ур. 01;Ур. 02;Ур. 03;Ур. 04;Ур. 05;Ур. 06;Иерархия;Код позиции произв.;Производитель;Показывать в WEB;Страна произв.;Наличие фото;Короткое наименование;Длинное наименование;Длинное описание;Регистрационное имя;Гарантия;Бренд;Модель;Серия;Группа атрибутов;Имя;Значение;Ед. изм.;Наличие ШК;Наличие изм.;ШК1;ШК2;ШК3;ШК4;ШК5;ШК6;ШК7;ШК8;ШК9;ШК10;Ширина;Длина;Высота;Ед. изм.;Вес;Ед. изм.;Наличие доп. атр.
1;-20141;20102190301;Строительство и ремонт;Инструменты;Оснастка для электроинструмента;Для фрезеров;Фрезы по дереву для фрезера;Фреза по дереву для фрезера;МВидео мастер иерархия;380,100,11;;0;IT;0;Фреза по дереву для фрезера CMT 380,100,11;Фреза по дереву для фрезера CMT 380,100,11;;Фреза HW для DOMINO-FESTOOL 10x28x49 Z=2 S=M6x0,75 RH;0;CMT;;;;;;;1;1;664252026548;;;;;;;;;;36000;36000;105000;см;00570;кг;0

So the categories (of different levels of detail) are in columns 4-9, the file to be matched is an xml file with tags categoryId, parentId. The matching is either done for the most detailed category (fairly long time) or by building  hierarchy tree (faster, but the parent the error on the top makes the whole match meaningless). 

The match is done using word2vec model (every category is represented by a vector and matches are determined on basis of cosine value between two vectors). The model itself if very large (> 500M) so it should be downloaded separately.

The w2v model is downloaded from https://nlpub.ru/Russian_Distributional_Thesaurus (the smallest one). In order to work the script needs gensim and numpy packages installed. 

The script is run as for example python xml_steam_paser -b good_items.scv -c /Users/dmitri/Documents/b2basket/run_yandex_yml_18413.xml -o output.xml where 

where -b file with "good categories", -c file to match and -o resulting file (original file with extra tag "matchedCategory" added to each item).
