# Erdőszimuláció Szörny AI-val 

## Hallgató
Nagy Csaba 

---

## Feladat leírása
A program egy egyszerű, játékos Python-alkalmazás, amely egy
procedurálisan generált erdőt jelenít meg. A felhasználó egy kék körrel
irányítható játékost mozgat a pályán, miközben egy piros szörny egy
állapotgép (FSM) alapján reagál a környezetére:

- járőrözik, ha nem látja a játékost,
- üldözi, ha a játékos a látókörébe kerül,
- visszatér a kiindulópontra, ha elveszíti a célpontot.

A fák L-System jellegű módszerrel generálódnak, így minden új erdő
egyedi.  
A játékosnak HP-ja van, a szörny üldözés közben gyorsul, a látótáv köre
pulzál, és a program a túlélési időt is méri.  
Játék végén az eredmény bekerül a `ncs_log.txt` naplófájlba.

A grafikus megjelenítés Tkinter Canvas alapú, a teljes logika külön
modulban (ncs_game.py) található.

---

## Modulok és a modulokban használt függvények

### **main.py**
A program belépési pontja:
- Tk ablak létrehozása (`Tk()`)
- az alkalmazás indítása (`NCSErdoAlkalmazas`)
- fő eseményciklus (`root.mainloop()`)

### **ncs_game.py** 
Használt modulok:
- **random**
  - `random.random()`
  - `random.randint()`
  - `random.choice()`
- **math**
  - `sqrt()`
  - `radians()`
- **time**
  - `time.time()`
- **tkinter**
  - `Canvas`, `Frame`, `Label`, `Button`

Saját függvény:
- **`ncs_erdogeneralas()`**  
  L-System jellegű fák generálása, procedurális erdő előállítása.

---

## Osztályok

### **NCSJátékos**
A játékos pozícióját, sebességét és mozgását kezeli.  
Metódus:  
- `mozog(dx, dy, szelesseg, magassag)` – pályahatárok ellenőrzésével.

### **NCSSzornyFSM**
A szörny mesterséges intelligenciája, Finite State Machine alapon.  
Állapotok:
- járőr  
- üldözés  
- visszatérés  

A szörny üldözés közben fokozatosan gyorsul.  
Metódusok:
- `tavolsag(px, py)`
- `frissit(jatekos, szelesseg, magassag, tuleles_mp)`

### **NCSLSystemFa**
Egy faág-struktúrát generál, L-System jellegű szabályokkal.  
Metódus:
- `szegmensek()` – visszaadja az ágak koordinátáit.

### **NCSErdoAlkalmazas**
A grafikus alkalmazás főosztálya:  
- Canvas rajzolás (erdő, játékos, szörny, látótáv)  
- billentyűkezelés  
- HP- és időmérés  
- logfájl írása  
- játékciklus frissítése  

---

## Kapcsolódás a szakdolgozathoz

Ez a beadandó témájában is illeszkedik a szakdolgozatomhoz, amely az
**algoritmikus tartalomgenerálás és a viselkedésmodellezés**
Python–C# környezetben történő vizsgálatával foglalkozik.

A projekt gyakorlatias demonstrációt ad két kulcsterületre:
- **procedurális generálás** (L-System erdő),
- **AI viselkedésmodellezés** (szörny – FSM).

A szakdolgozatban használt elméleti és modellezési módszerek (PCG, FSM,
állapotváltozások, reakciók) itt kisebb, interaktív formában jelennek
meg, ezért a program egyfajta Python-oldali mini mintaprojektként is
szolgál a dolgozat gyakorlati részéhez.
