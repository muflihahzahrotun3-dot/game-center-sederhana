"""
GAME CENTER SEDERHANA (berbasis OOP)
====================================
Berisi 2 game yang dimainkan di terminal:
  1. Tebak Angka
  2. Suit (Batu - Gunting - Kertas)

Konsep OOP: Class & Object, Encapsulation, Property, Inheritance,
Polymorphism, Abstraction, Composition, Magic method, Custom Exception.
"""

import random
from abc import ABC, abstractmethod


# ---------------------------------------------------------------
# Fungsi bantu input
# ---------------------------------------------------------------
def baca(prompt):
    """Membaca input; jika input habis (Ctrl+Z / Ctrl+D) dianggap keluar."""
    try:
        return input(prompt).strip().lower()
    except EOFError:
        raise KeluarGame()


class KeluarGame(Exception):
    """Dipakai untuk keluar dari game kapan saja."""


# ---------------------------------------------------------------
# PEMAIN
# ---------------------------------------------------------------
class Pemain:
    def __init__(self, nama):
        self.nama = nama
        self.__skor = 0                  # private

    @property
    def skor(self):
        return self.__skor

    def tambah_skor(self, poin):
        self.__skor += poin

    def __str__(self):
        return f"{self.nama} (skor: {self.__skor})"


# ---------------------------------------------------------------
# ABSTRACTION: class dasar semua game
# ---------------------------------------------------------------
class Game(ABC):
    judul = "Game"

    def __init__(self, pemain):
        self.pemain = pemain             # composition

    def tampilkan_judul(self):
        print("\n" + "=" * 40)
        print(f"  {self.judul.upper()}")
        print("=" * 40)

    @abstractmethod
    def mainkan(self):
        """Setiap game wajib menuliskan cara bermainnya sendiri."""

    def __str__(self):
        return self.judul


# ---------------------------------------------------------------
# GAME 1: TEBAK ANGKA
# ---------------------------------------------------------------
class TebakAngka(Game):
    judul = "Tebak Angka"

    def __init__(self, pemain, batas_bawah=1, batas_atas=100, kesempatan=7):
        super().__init__(pemain)
        self.batas_bawah = batas_bawah
        self.batas_atas = batas_atas
        self.kesempatan = kesempatan

    def mainkan(self):
        self.tampilkan_judul()
        rahasia = random.randint(self.batas_bawah, self.batas_atas)
        print(f"Tebak angka antara {self.batas_bawah} dan {self.batas_atas}.")
        print(f"Kamu punya {self.kesempatan} kesempatan.\n")

        for sisa in range(self.kesempatan, 0, -1):
            jawaban = baca(f"[Sisa {sisa}] Tebakanmu: ")
            if not jawaban.lstrip("-").isdigit():
                print("  Masukkan angka ya!")
                continue
            tebakan = int(jawaban)

            if tebakan == rahasia:
                poin = sisa * 10
                self.pemain.tambah_skor(poin)
                print(f"  BENAR! Angkanya {rahasia}. +{poin} poin")
                return
            petunjuk = "terlalu kecil" if tebakan < rahasia else "terlalu besar"
            print(f"  Salah, {petunjuk}.")

        print(f"  Kesempatan habis. Angkanya adalah {rahasia}.")


# ---------------------------------------------------------------
# GAME 2: SUIT
# ---------------------------------------------------------------
class Suit(Game):
    judul = "Suit Batu Gunting Kertas"
    PILIHAN = ("batu", "gunting", "kertas")
    MENANG_ATAS = {"batu": "gunting", "gunting": "kertas", "kertas": "batu"}

    @staticmethod
    def normalisasi(teks):
        angka = {"1": "batu", "2": "gunting", "3": "kertas"}
        return angka.get(teks, teks)

    def tentukan_pemenang(self, pemain, komputer):
        if pemain == komputer:
            return "seri"
        return "pemain" if self.MENANG_ATAS[pemain] == komputer else "komputer"

    def mainkan(self):
        self.tampilkan_judul()
        print("Siapa yang lebih dulu menang 2 ronde, dialah juara.")
        print("Pilih: 1 = batu, 2 = gunting, 3 = kertas\n")

        skor_pemain = skor_komputer = 0
        while skor_pemain < 2 and skor_komputer < 2:
            pilihan = self.normalisasi(baca("Pilihanmu: "))
            if pilihan not in self.PILIHAN:
                print("  Pilihan tidak valid.")
                continue

            lawan = random.choice(self.PILIHAN)
            hasil = self.tentukan_pemenang(pilihan, lawan)
            print(f"  Kamu: {pilihan} | Komputer: {lawan}")

            if hasil == "pemain":
                skor_pemain += 1
                print("  Kamu menang ronde ini!")
            elif hasil == "komputer":
                skor_komputer += 1
                print("  Komputer menang ronde ini.")
            else:
                print("  Seri, ulangi.")
            print(f"  Skor ronde -> Kamu {skor_pemain} : {skor_komputer} Komputer\n")

        if skor_pemain > skor_komputer:
            self.pemain.tambah_skor(30)
            print("  SELAMAT, kamu juara! +30 poin")
        else:
            print("  Komputer juara. Coba lagi!")


# ---------------------------------------------------------------
# GAME CENTER (composition: memiliki banyak Game)
# ---------------------------------------------------------------
class GameCenter:
    def __init__(self, pemain):
        self.pemain = pemain
        self.__daftar = {
            "1": TebakAngka(pemain),
            "2": Suit(pemain),
        }

    def menu(self):
        print("\n--- MENU GAME ---")
        for kunci, game in self.__daftar.items():
            print(f"  {kunci}. {game}")           # memakai __str__
        print("  0. Keluar")
        print(f"  {self.pemain}")

    def jalankan(self):
        try:
            while True:
                self.menu()
                pilihan = baca("Pilih game: ")
                if pilihan == "0":
                    break
                game = self.__daftar.get(pilihan)
                if game is None:
                    print("  Menu tidak ada.")
                    continue
                game.mainkan()                    # polymorphism
        except KeluarGame:
            pass
        print(f"\nTerima kasih sudah bermain! Skor akhir {self.pemain}")


def main():
    print("Selamat datang di GAME CENTER!")
    try:
        nama = input("Masukkan namamu: ").strip() or "Pemain"
    except EOFError:
        nama = "Pemain"
    GameCenter(Pemain(nama)).jalankan()


if __name__ == "__main__":
    main()
