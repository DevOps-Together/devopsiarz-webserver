# Prosty serwer HTTP napisany przez programistę Javy bez doświadczenia w pythnie 😃

Poniżej widzisz mój pseudo issue tracker, jako że nie chcę zaspamić emaili współkursantów tworząc issues do wszystkiego. 
## Minimalna funkcjonalność:

### Backlog:
- 
### Do testów:
- 
### Działająca:
- Plik html powinna nam wyświetlić przeglądarka jako html
- Inne pliki na serwerze powinno listować
- Jak w katalogu jest plik `index.html`, wtedy zamiast listingu, niech przeglądarka wyświetli jego zawartość.

## Dodatkowa funkcjonalność:
- Pliki nie-html obsługiwane z rozpoznawaniem mimetype. Np. obrazki wyświetlane jako obrazki przez przeglądarkę.
- Pobieranie dla plików większych niż określony rozmiar i/lub o określonych rozszerzeniach i/lub mimetype. (Przeglądarka sama decyduje co zrobić z plikiem zależnie od mimetype)
- Lista plików index z prostym regexem/globem.

### Backlog:
-
### Do testów:
- 
### Działająca:
- Określanie lokalizacji wypisania logów.
- Autentykacja użytkowników metodą http basic auth.

## Lista życzeń
- Możliwość włączenia/wyłączenia wypisywania logów do pliku
- Możliwość włączenia/wyłączenia wypisywania logów na stdout
- Wypisywanie logów do pliku i na stdout mogą być równocześnie włączone

## Bugi:
- 

## Tech debt:
- Wypadało by dodać logowanie w request handlerach, zwłaszcza przy odrzucaniu i akceptowaniu credentiali użytkownika.

## Dokumentacja

[`docs/config.explained.md`](docs/config.explained.md) - zawiera przykładową zawartość config.json z objaśnieniami.  
[`docs/running.md`](docs/running.md) - wyjaśnia jak uruchomić program.  
[`docs/contribute.md`](docs/contribute.md) - wyjaśnia co zrobić jeśli chcesz coś dorzucić do tego podprojektu.