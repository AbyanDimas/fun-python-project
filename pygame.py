import curses
from random import randint
import os
import subprocess

def pusatkan_terminal():
    """
    Fungsi ini memposisikan terminal di tengah layar dan mengatur ukurannya.
    Spesifik untuk macOS.
    """
    # Ubah ukuran terminal menjadi 24 baris dan 80 kolom
    os.system('printf "\e[8;24;80t"')
    
    # Gunakan osascript untuk memposisikan terminal di tengah layar (khusus macOS)
    script = '''
    tell application "Terminal"
        set bounds of front window to {100, 100, 900, 700}
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

def layar_awal(stdscr):
    """
    Menampilkan layar awal yang meminta pemain untuk memilih mode permainan.
    """
    sh, sw = stdscr.getmaxyx()
    stdscr.addstr(sh // 2 - 1, sw // 2 - len("Tekan 's' untuk memulai permainan mode normal") // 2, "Tekan 's' untuk memulai permainan mode normal")
    stdscr.addstr(sh // 2 + 1, sw // 2 - len("Tekan 'g' untuk memulai permainan mode baik (tidak game over)") // 2, "Tekan 'g' untuk memulai permainan mode baik (tidak game over)")
    stdscr.refresh()

    mode = "normal"
    while True:
        key = stdscr.getch()
        if key == ord('s'):
            mode = "normal"
            break
        elif key == ord('g'):
            mode = "baik"
            break
    return mode

def layar_game_over(stdscr, skor):
    """
    Menampilkan layar game over dan meminta pemain untuk memilih apakah akan mengulangi permainan atau keluar.
    """
    sh, sw = stdscr.getmaxyx()
    stdscr.addstr(sh // 2, sw // 2 - len(f"Permainan Berakhir! Skor Anda: {skor}. Tekan 'r' untuk mengulangi atau 'q' untuk keluar") // 2, f"Permainan Berakhir! Skor Anda: {skor}. Tekan 'r' untuk mengulangi atau 'q' untuk keluar")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('r'):
            return True
        elif key == ord('q'):
            return False

def permainan(stdscr, mode):
    """
    Mengimplementasikan logika permainan ular.
    """
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    key = curses.KEY_RIGHT
    ular = [
        [sh // 2, sw // 2],
        [sh // 2, (sw // 2) - 1],
        [sh // 2, (sw // 2) - 2]
    ]
    makanan = [sh // 2, sw // 2 + 5]

    w.addch(makanan[0], makanan[1], curses.ACS_PI)

    skor = 0

    while True:
        next_key = w.getch()
        
        # Cegah ular berbalik ke arah yang berlawanan
        if next_key == curses.KEY_DOWN and key != curses.KEY_UP:
            key = next_key
        elif next_key == curses.KEY_UP and key != curses.KEY_DOWN:
            key = next_key
        elif next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT:
            key = next_key
        elif next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT:
            key = next_key

        kepala = ular[0]
        kepala_baru = [kepala[0], kepala[1]]

        if key == curses.KEY_DOWN:
            kepala_baru[0] += 1
        if key == curses.KEY_UP:
            kepala_baru[0] -= 1
        if key == curses.KEY_LEFT:
            kepala_baru[1] -= 1
        if key == curses.KEY_RIGHT:
            kepala_baru[1] += 1

        ular.insert(0, kepala_baru)

        if ular[0] == makanan:
            skor += 1
            makanan = None
            while makanan is None:
                nm = [
                    randint(1, sh - 1),
                    randint(1, sw - 1)
                ]
                makanan = nm if nm not in ular else None
            w.addch(makanan[0], makanan[1], curses.ACS_PI)
        else:
            ekor = ular.pop()
            w.addch(ekor[0], ekor[1], ' ')

        if mode == "normal":
            if (
                ular[0][0] in [0, sh] or
                ular[0][1] in [0, sw] or
                ular[0] in ular[1:]
            ):
                return skor
        elif mode == "baik":
            if ular[0][0] == 0:
                ular[0][0] = sh - 1
            elif ular[0][0] == sh:
                ular[0][0] = 1
            if ular[0][1] == 0:
                ular[0][1] = sw - 1
            elif ular[0][1] == sw:
                ular[0][1] = 1

        w.addch(ular[0][0], ular[0][1], curses.ACS_CKBOARD)

def main(stdscr):
    """
    Fungsi utama yang mengontrol alur permainan, termasuk memilih mode permainan, menjalankan permainan, dan menangani game over.
    """
    pusatkan_terminal()
    
    while True:
        stdscr.clear()
        mode = layar_awal(stdscr)
        skor = permainan(stdscr, mode)
        stdscr.clear()
        ulangi = layar_game_over(stdscr, skor)
        if not ulangi:
            break

curses.wrapper(main)
