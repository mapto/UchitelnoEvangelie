# Индекс за Учително Евангелие
Проект за създаване на полу-автоматичен индекс за средновековния ръкопис <a href="https://bg.wikipedia.org/wiki/%D0%A3%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D0%BD%D0%BE_%D0%B5%D0%B2%D0%B0%D0%BD%D0%B3%D0%B5%D0%BB%D0%B8%D0%B5">„Учително евангелие“</a> на Константин Преславски.

Извличането от документ не е гладък процес. Наложи ми се да правя експерименти с три различни файлови формата (съответно .DOC, .DOCX и .ODT). Целта на тази паралелна обработка е да видя от кой ще бъде изнесена информацията в най-чист и най-удобен за ползване вид. Тук допускането е, че конверитирането между форматите е лесна стъпка, която може да бъде извършена както с <a href="https://products.office.com/word">Microsoft Word</a>, така и с <a href="https://www.libreoffice.org/discover/writer/">LibreOffice Writer</a>. Резултатът е, че форматът .DOCX е най-добре поддържан - благодарение на библиотеката <a href="https://github.com/python-openxml/python-docx">python-docx</a>.

Веднъж изчистен извлечения текст, ще развия таблицата до необходимата структура и ще го експортирам в необходимия формат (или формати).

Понастоящем, с цел лесна демонстрация, тук е публикувана и примерната глава (в трите файлови формата), която ми изпратихте за проби. Този сайт не може да бъде направен публичен докато тези материали не бъдат премахнати, а сайтът трансформиран така, че да работи с файлове, подадени от потребителя.

# Изтегляне

В <a href="https://github.com/mapto/UchitelnoEvangelie">GitHub</a> се намира актуалната версия на изходния код.

Компилирана версия за Windows може да бъде <a href="https://www.dropbox.com/s/q1hs2ofpmr7c8d5/extractor.exe?dl=0">изтеглена от Dropbox</a>.

# Компилиране

За да бъде използвана програмата, тя не е задължително да бъде компилирана. За компилирането ѝ е необходимо да бъде изтеглен кодът и да има инсталирана версия на <a href="https://www.docker.com/">docker</a>.
За да бъде създаден изпълним файл за Windows, командата, която трябва да изпълните от директорията, където сте свалили кода е:

    docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows

Тази команда ще създаде изпълним файл в поддиректорията dist/windows/

За Linux:

    docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux

Ще създаде изпълним файл в поддиректорията dist/linux/

# Използване

Програмата може да се компилира или да се използва с помощта на актуална версия на python (3.6+).

## Интерпретирана версия

За режим без компилация, трябва първо да бъдат инсталирани необходимите библиотеки. Това става с команадата:

    pip install -r requirements.txt

След това програмата се изпълнява с

    python3 extractor.py

## Компилирана версия

Ако разполагате с компилираната версия, достатъчно е да пуснете (drag&drop) изходен .DOCX файл върху иконката на изпълнимия файл.

Програмата разполага и с команден интерфейс, който може да бъде видян при изпълнение на програмата без параметри. Възможните параметри могат да бъдат видени и в <a href="https://github.com/mapto/UchitelnoEvangelie/blob/master/extractor.py">документацията в кода</a>.

# Авторски права

Този проект се разпространява под <a href="https://mit-license.org/">MIT License</a>.

Използваният типографски шрифт *Cyrillica Ochrid 10U* е „раздаван безплатно“ <a href="https://osvedomitel.bg/2020/02/prof-totomanova/">по думите</a> на представител на притежателите на лиценза от БАН.

За създаването на иконата е използван символът <a href="https://fontawesome.com/icons/book-open?style=solid">open-book</a> от FontAwesome, разпространяван под лиценза <a href="https://creativecommons.org/licenses/by/4.0/">Криейтив комънс признание 4.0 международен вариант</a>.

