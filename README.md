 Erdőszimuláció szörny AI-val 

Hallgató:
Nagy Csaba 

Feladat leírása:
A program egy egyszerű, játék jellegű Python alkalmazás. A pálya egy
procedurálisan generált erdő, amely minden futtatáskor másképp néz ki.
A játékos egy kék körrel mozoghat a vásznon, miközben egy szörny
(piros kör) a saját állapotai alapján dönt arról, hogy merre mozogjon.
A szörny járőrözhet, üldözheti a játékost, vagy visszatérhet a
kiindulópontra, ha lemarad.

A játékosnak van HP-ja, a szörny üldözés közben gyorsabbá válik,
a túlélési idő folyamatosan mérve van, és a játék befejezésekor az
eredmény belekerül egy ncs_log.txt nevű fájlba.  
A megjelenítés Tkinter Canvas segítségével történik.

Modulok és a használt függvények:

main.py:
- Tkinter ablak létrehozása (Tk)
- Az alkalmazás elindítása (NCSErdoAlkalmazas)
- főciklus (mainloop)

ncs_game.py (saját modul, NCS monogrammal):
Felhasznált modulok:
- random: véletlenszám-generálás (random, randint, choice)
- math: trigonometria és távolságszámítás (sqrt, radians)
- time: túlélési idő mérése (time)
- tkinter: grafikus elemek (Canvas, Frame, Label, Button)

Saját függvény:
- ncs_erdogeneralas(): az erdő L-System jellegű generálásáért felel.

Osztályok:

NCSJátékos:
A játékos pozícióját és mozgását kezeli.

NCSSzornyFSM:
A szörny viselkedését valósítja meg egy egyszerű állapotgéppel
(járőr, üldözés, visszatérés). Üldözés közben fokozatosan gyorsul.

NCSLSystemFa:
Egy-egy faág-struktúrát hoz létre L-Systemhez hasonló módszerrel.

NCSErdoAlkalmazas:
A teljes grafikus alkalmazás főosztálya, amely kezeli a rajzolást,
a billentyűket, a játék logikáját, és a logfájl írását.

Kapcsolódás a szakdolgozathoz:
A beadandó témája részben kapcsolódik a szakdolgozatomhoz, amely az
algoritmikus tartalomgenerálással és a viselkedésmodellezéssel foglalkozik.
A projekt kisebb gyakorlati példát mutat be arra, hogyan lehet Pythonban 
procedurális környezetet és egyszerű AI működést összeállítani.
