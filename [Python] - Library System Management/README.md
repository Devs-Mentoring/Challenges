# Zarządzanie Systemem Bibliotecznym

## Opis Zadania: 
Twoim zadaniem jest stworzenie systemu do zarządzania biblioteką. System powinien zawierać co najmniej trzy klasy: Book, Reader i Library.

## Klasy

### Book

Klasa `Book` powinna zawierać szczegóły dotyczące książki, takie jak tytuł, autor, wydawca, rok wydania, status dostępności oraz ilość dostępnych egzemplarzy. Książka powinna być unikalna, a system powinien obsługiwać błędy związane z próbą dodania książki, która już istnieje.

### Reader

Klasa `Reader` powinna zawierać informacje o czytelnikach, takie jak imię, nazwisko, numer czytelnika, wypożyczone książki oraz historię wypożyczeń. Czytelnik powinien być unikalny, a system powinien obsługiwać błędy związane z próbą dodania czytelnika, który już istnieje. Dodatkowo, czytelnicy powinni mieć możliwość rezerwacji książek, które są aktualnie niedostępne.

### Library

Klasa `Library` powinna zawierać metody umożliwiające zarządzanie książkami i czytelnikami, takie jak dodawanie nowych książek/czytelników, wyszukiwanie książek/czytelników, wypożyczanie książek czytelnikom, przyjmowanie zwrotów książek, obsługa rezerwacji oraz śledzenie historii wypożyczeń. Biblioteka powinna również monitorować daty zwrotu i informować czytelników o zbliżających się terminach zwrotu. Jeśli książka nie zostanie zwrócona na czas, system powinien nałożyć karę na czytelnika.

## Wymagania

### Struktury danych

Zastosuj stosowne struktury danych do przechowywania informacji o książkach i czytelnikach.

### Rezerwacje

Czytelnicy powinni mieć możliwość rezerwacji książek, które są aktualnie niedostępne. Gdy książka stanie się dostępna, czytelnik, który zarezerwował tę książkę, powinien otrzymać powiadomienie.

### Historia wypożyczeń

System powinien przechowywać historię wypożyczeń dla każdego czytelnika. Dla każdego wypożyczenia, historia powinna zawierać datę wypożyczenia, datę zwrotu i tytuł książki.

### Opóźnienia w zwrotach

System powinien monitorować daty zwrotu i informować czytelników o zbliżających się terminach zwrotu. Jeśli książka nie zostanie zwrócona na czas, system powinien nałożyć karę na czytelnika.

### Obsługa błędów

System powinien obsługiwać błędy związane z próbą wypożyczenia książki, która jest już wypożyczona, dodania książki/czytelnika, który już istnieje, itp.

### Testy jednostkowe

Przygotuj zestaw testów jednostkowych dla swojego systemu.

## Dostarczanie rozwiązania

Do dostarczenia rozwiązania należy wykonać następujące kroki:

1. Zforkować projekt do swojego konta na GitHubie.
2. Oprogramowanie należy napisać w języku Python, a pliki umieścić w folderze o nazwie "src".
3. Wymagane pliki konfiguracyjne, jak np. requirements.txt, powinny być umieszczone w folderze projektu bezpośrednio.
4. W folderze "tests" należy umieścić testy jednostkowe dla swojego rozwiązania.
5. Po zakończeniu pracy należy wysłać swoje zmiany na GitHub poprzez push.
6. Następnie należy utworzyć Pull Request ze swojego forka do projektu głównego.
