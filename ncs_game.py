# -*- coding: utf-8 -*-

from tkinter import Frame, Canvas, Button, Label, Tk
import math
import random
import time


class NCSJátékos:
    def __init__(self, x: float, y: float, sebesseg: float = 5) -> None:
        self.x = x
        self.y = y
        self.sebesseg = sebesseg
        self.meret = 12

    def mozog(self, dx: int, dy: int, szelesseg: int, magassag: int) -> None:
        nx = self.x + dx * self.sebesseg
        ny = self.y + dy * self.sebesseg
        if 0 < nx < szelesseg:
            self.x = nx
        if 0 < ny < magassag:
            self.y = ny


class NCSSzornyFSM:
    def __init__(self, x: float, y: float) -> None:
        self.kezdo_x = x
        self.kezdo_y = y
        self.x = x
        self.y = y
        self.meret = 14
        self.allapot = "járőr"
        self.jaror_irany = 1
        self.latotav = 120
        self.uldozes_alap = 3.0
        self.uldozes_seb = 3.0
        self.jaror_seb = 2.0
        self.vissza_seb = 2.0

    def tavolsag(self, px: float, py: float) -> float:
        return math.sqrt((self.x - px) ** 2 + (self.y - py) ** 2)

    def frissit(
        self,
        jatekos: "NCSJátékos",
        szelesseg: int,
        magassag: int,
        tuleles_mp: float,
    ) -> None:
        d = self.tavolsag(jatekos.x, jatekos.y)

        if self.allapot == "járőr":
            self.uldozes_seb = self.uldozes_alap
            if d < self.latotav:
                self.allapot = "üldözés"
            else:
                self.x += self.jaror_irany * self.jaror_seb
                if self.x < 40 or self.x > szelesseg - 40:
                    self.jaror_irany *= -1

        elif self.allapot == "üldözés":
            self.uldozes_seb = self.uldozes_alap + 0.02 * tuleles_mp
            if d > self.latotav * 1.4:
                self.allapot = "visszatérés"
            else:
                dx = jatekos.x - self.x
                dy = jatekos.y - self.y
                h = math.sqrt(dx * dx + dy * dy) or 1.0
                self.x += self.uldozes_seb * dx / h
                self.y += self.uldozes_seb * dy / h

        elif self.allapot == "visszatérés":
            dx = self.kezdo_x - self.x
            dy = self.kezdo_y - self.y
            d0 = math.sqrt(dx * dx + dy * dy)

            if d0 < 2:
                self.x = self.kezdo_x
                self.y = self.kezdo_y
                self.allapot = "járőr"
            else:
                self.x += self.vissza_seb * dx / d0
                self.y += self.vissza_seb * dy / d0


class NCSLSystemFa:
    def __init__(self, sx: float, sy: float, hossz: float, szog: float, melyseg: int):
        self.sx = sx
        self.sy = sy
        self.hossz = hossz
        self.szog = szog
        self.melyseg = melyseg

    def szegmensek(self) -> list[tuple[float, float, float, float]]:
        verem: list[tuple[float, float, float, float, int]] = [
            (self.sx, self.sy, self.hossz, self.szog, self.melyseg)
        ]
        lista: list[tuple[float, float, float, float]] = []

        while verem:
            x, y, hossz, szog, melyseg = verem.pop()
            if melyseg == 0 or hossz < 5:
                continue

            rad = math.radians(szog)
            x2 = x + math.cos(rad) * hossz
            y2 = y - math.sin(rad) * hossz

            lista.append((x, y, x2, y2))

            uj_hossz = hossz * (0.6 + random.random() * 0.1)
            delta = 20 + random.randint(-5, 5)

            verem.append((x2, y2, uj_hossz, szog + delta, melyseg - 1))
            verem.append((x2, y2, uj_hossz, szog - delta, melyseg - 1))

        return lista


def ncs_erdogeneralas(
    szelesseg: int, magassag: int, famenny: int = 7
) -> list[list[tuple[float, float, float, float]]]:
    erdo: list[list[tuple[float, float, float, float]]] = []
    for _ in range(famenny):
        x = random.randint(40, szelesseg - 40)
        y = random.randint(magassag // 2, magassag - 20)
        hossz = random.randint(40, 70)
        melyseg = random.choice([3, 4, 5])
        fa = NCSLSystemFa(x, y, hossz, 90, melyseg)
        erdo.append(fa.szegmensek())
    return erdo


class NCSErdoAlkalmazas(Frame):
    def __init__(self, master: Tk) -> None:
        super().__init__(master)

        self.master = master
        self.master.title("NCS – Erdőszimuláció Szörny FSM-mel")

        self.szelesseg = 640
        self.magassag = 480
        self.pack()

        self.canvas = Canvas(
            self,
            width=self.szelesseg,
            height=self.magassag,
            bg="#101820",
        )
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.status = Label(
            self,
            text="Szörny állapota: járőr | Idő: 0 mp | HP: 100",
        )
        self.status.grid(row=1, column=0, sticky="w")

        gomb_uj = Button(self, text="Új erdő", command=self.erdouj)
        gomb_uj.grid(row=1, column=1)

        gomb_kilep = Button(self, text="Kilépés", command=self.master.destroy)
        gomb_kilep.grid(row=1, column=2)

        self.jatekos = NCSJátékos(self.szelesseg // 2, self.magassag - 60)
        self.szorny = NCSSzornyFSM(self.szelesseg // 2, self.magassag // 2)

        self.fak = ncs_erdogeneralas(self.szelesseg, self.magassag)

        self.nyomott: set[str] = set()
        master.bind("<KeyPress>", self.lenyo)
        master.bind("<KeyRelease>", self.felenged)

        self.fut = True
        self.kezdido = time.time()
        self.tuleles_mp = 0.0
        self.hp = 100

        self.fociklus()

    def erdouj(self) -> None:
        self.fak = ncs_erdogeneralas(self.szelesseg, self.magassag)
        self.jatekos = NCSJátékos(self.szelesseg // 2, self.magassag - 60)
        self.szorny = NCSSzornyFSM(self.szelesseg // 2, self.magassag // 2)
        self.kezdido = time.time()
        self.tuleles_mp = 0.0
        self.hp = 100
        if not self.fut:
            self.fut = True
            self.fociklus()

    def lenyo(self, e) -> None:
        self.nyomott.add(e.keysym)

    def felenged(self, e) -> None:
        self.nyomott.discard(e.keysym)

    def jatekos_input(self) -> None:
        dx = 0
        dy = 0
        if "a" in self.nyomott or "Left" in self.nyomott:
            dx -= 1
        if "d" in self.nyomott or "Right" in self.nyomott:
            dx += 1
        if "w" in self.nyomott or "Up" in self.nyomott:
            dy -= 1
        if "s" in self.nyomott or "Down" in self.nyomott:
            dy += 1
        if dx or dy:
            self.jatekos.mozog(dx, dy, self.szelesseg, self.magassag)

    def utkozes_van(self) -> bool:
        dx = self.jatekos.x - self.szorny.x
        dy = self.jatekos.y - self.szorny.y
        d = math.sqrt(dx * dx + dy * dy)
        return d < (self.jatekos.meret + self.szorny.meret)

    def jatek_vege(self) -> None:
        self.canvas.create_text(
            self.szelesseg // 2,
            self.magassag // 2,
            text="Játék vége – a szörny elkapott",
            fill="white",
            font=("Arial", 16, "bold"),
        )
        try:
            with open("ncs_log.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"Túlélési idő: {int(self.tuleles_mp)} mp, HP: {self.hp}\n"
                )
        except OSError:
            # ha nem sikerül a fájlírás (pl. jogosultság), a játék ettől még fusson tovább
            pass

    def fociklus(self) -> None:
        if not self.fut:
            return

        self.jatekos_input()
        self.tuleles_mp = time.time() - self.kezdido

        self.szorny.frissit(
            self.jatekos,
            self.szelesseg,
            self.magassag,
            self.tuleles_mp,
        )

        if self.utkozes_van():
            self.hp -= 25
            if self.hp <= 0:
                self.hp = 0
                self.fut = False
                self.ujrarajzol()
                self.status.config(
                    text=(
                        f"Szörny állapota: {self.szorny.allapot} | "
                        f"Idő: {int(self.tuleles_mp)} mp | HP: {self.hp}"
                    )
                )
                self.jatek_vege()
                return

        self.ujrarajzol()
        self.status.config(
            text=(
                f"Szörny állapota: {self.szorny.allapot} | "
                f"Idő: {int(self.tuleles_mp)} mp | HP: {self.hp}"
            )
        )
        self.after(33, self.fociklus)

    def ujrarajzol(self) -> None:
        self.canvas.delete("all")

        for fa in self.fak:
            for x1, y1, x2, y2 in fa:
                if random.random() > 0.15:
                    szin = "#3fa34d"
                else:
                    szin = "#6b4f2d"
                self.canvas.create_line(x1, y1, x2, y2, fill=szin, width=2)

        self.canvas.create_oval(
            self.jatekos.x - self.jatekos.meret,
            self.jatekos.y - self.jatekos.meret,
            self.jatekos.x + self.jatekos.meret,
            self.jatekos.y + self.jatekos.meret,
            fill="#4f8cff",
            outline="",
        )

        szin = "#b82525"
        if self.szorny.allapot == "üldözés":
            szin = "#ff4444"
        elif self.szorny.allapot == "visszatérés":
            szin = "#ff9966"

        self.canvas.create_oval(
            self.szorny.x - self.szorny.meret,
            self.szorny.y - self.szorny.meret,
            self.szorny.x + self.szorny.meret,
            self.szorny.y + self.szorny.meret,
            fill=szin,
            outline="",
        )

        pulzus = (math.sin(time.time() * 2.0) + 1.0) / 2.0
        ertek = int(80 + pulzus * 120)
        lat_szin = f"#{ertek:02x}{ertek:02x}{ertek:02x}"

        self.canvas.create_oval(
            self.szorny.x - self.szorny.latotav,
            self.szorny.y - self.szorny.latotav,
            self.szorny.x + self.szorny.latotav,
            self.szorny.y + self.szorny.latotav,
            outline=lat_szin,
        )
