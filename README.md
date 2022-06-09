# Simple webserver by java programmer who is using python for the first time

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

### Backlog:
- Pliki nie-html obsługiwane z rozpoznawaniem mimetype. Np. obrazki wyświetlane jako obrazki przez przeglądarkę.
- Pobieranie dla plików większych niż określony rozmiar i/lub o określonych rozszerzeniach i/lub mimetype.
- Lista plików index z prostym regexem/globem.

### Do testów:
- Autentykacja użytkowników metodą http basic auth.

### Działająca:
- Określanie lokalizacji wypisania logów.

## Lista życzeń
- Możliwość włączenia/wyłączenia wypisywania logów do pliku
- Możliwość włączenia/wyłączenia wypisywania logów na stdout
- Wypisywanie logów do pliku i na stdout mogą być równocześnie włączone

## Bugi:
- Obrazki są wyświetlane jako tekst w przeglądarce (prawdopodobnie mimetype ustawiony na text/html)

## Tech debt:
- Wypadało by dodać logowanie w request handlerach, zwłaszcza przy odrzucaniu i akceptowaniu credentiali użytkownika.

## Dokumentacja

[`docs/config.explained.md`](docs/config.explained.md) - zawiera przykładową zawartość config.json z objaśnieniami.  
[`docs/running.md`](docs/running.md) - wyjaśnia jak uruchomić program.  
[`docs/contribute.md`](docs/contribute.md) - wyjaśnia co zrobić jeśli chcesz coś dorzucić do tego podprojektu.