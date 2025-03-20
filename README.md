#Aplikacja CRUD z wykorzystaniem wzorca Fabryki

## Opis projektu
Celem tego projektu jest implementacja aplikacji zarządzającej danymi w formatach JSON, CSV oraz XML przy wykorzystaniu wzorca projektowego Fabryka. Aplikacja pozwala na wykonywanie operacji CRUD (Create, Read, Update, Delete) na wybranym zbiorze danych, które mogą być ładowane i zapisywane w różnych formatach plików.

## Funkcjonalności
- Obsługa formatów danych: JSON, CSV oraz XML.
- Operacje CRUD:
   - Dodawanie nowych rekordów do zbioru danych.
   - Odczyt istniejących danych.
   - Aktualizacja rekordów w zbiorze.
   - Usuwanie danych.
- Dynamiczny wybór formatu danych: Aplikacja automatycznie wybiera odpowiednią implementację na podstawie wybranego formatu.

## Wzorzec Fabryki
Wzorzec Fabryka umożliwia tworzenie instancji odpowiednich klas w zależności od formatu pliku (JSON, CSV lub XML), zapewniając elastyczność i przejrzystość kodu.