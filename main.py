import pandas as pd
import numpy as np
from datetime import datetime
from pynput import keyboard
import os

# Global variables
queue = None
try:
    queue = pd.read_csv('queue.csv')
except FileNotFoundError:
    queue = pd.DataFrame(columns=['Nama', 'Nik', 'gender', 'date', 'diagnosa', 'obat', 'ruangan'])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu():
    clear_screen()
    print("\n=== Sistem Informasi Kesehatan ===")
    print("1. Data Pasien")
    print("2. Jadwal Dokter")
    print("3. Konsul dan Diagnosa")
    print("4. Resep Obat")
    print("5. Pembayaran")
    print("\nPress ESC to exit")

def data_pasien_menu():
    clear_screen()
    print("\n=== Data Pasien ===")
    print("1. Tambah Pasien")
    print("2. Hapus Pasien")
    print("3. Edit Pasien")
    print("4. Lihat Daftar Pasien")
    print("\nPress ESC to return to main menu")

def antrian():
    global queue
    clear_screen()
    print("\n=== Tambah Pasien ===")
    
    def on_press(key):
        if key == keyboard.Key.esc:
            return False
    
    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            if not listener.running:
                return
            
            try:
                Nama = input("Nama (or ESC to cancel): ")
                if any(char.isdigit() for char in Nama):
                    print("Nama tidak boleh berisi angka.")
                    continue
                elif len(Nama) < 3:
                    print("Nama terlalu pendek.")
                    continue

                NIK = input("NIK: ")
                if not NIK.isdigit():
                    print("NIK harus berupa angka.")
                    continue
                elif len(NIK) != 16:
                    print("NIK harus 16 digit.")
                    continue

                gender = input("Gender (F/M): ").upper()
                if gender not in ["F", "M"]:
                    print("Gender harus diisi dengan F atau M (kapital).")
                    continue

                current_time = datetime.now()
                waktu = input("Waktu (MM-DD HH:MM) [default: sekarang]: ") or current_time.strftime("%m-%d %H:%M")

                temp = pd.DataFrame({
                    'Nama': [Nama],
                    'Nik': [NIK],
                    'gender': [gender],
                    'date': [waktu],
                    'diagnosa': [np.nan],
                    'obat': [np.nan],
                    'ruangan': [np.nan]
                })

                queue = pd.concat([queue, temp], ignore_index=True)
                queue.to_csv('queue.csv', index=False)
                print("Antrian diperbarui dan disimpan ke 'queue.csv'.")
                break

            except Exception as e:
                print(f"Error: {e}")
                continue

def handle_data_pasien(key):
    try:
        if key.char == '1':
            antrian()
        elif key.char == '2':
            show_remove_patient()
        elif key.char == '3':
            show_edit_patient()
        elif key.char == '4':
            show_patient_list()
    except AttributeError:
        if key == keyboard.Key.esc:
            return False
    return True

def main(key):
    try:
        if key.char == '1':
            data_pasien_menu()
            with keyboard.Listener(on_press=handle_data_pasien) as listener:
                listener.join()
            show_main_menu()
        elif key.char == '2':
            print("Jadwal Dokter menu - To be implemented")
        elif key.char == '3':
            print("Konsul dan Diagnosa menu - To be implemented")
        elif key.char == '4':
            print("Resep Obat menu - To be implemented")
        elif key.char == '5':
            print("Pembayaran menu - To be implemented")
    except AttributeError:
        if key == keyboard.Key.esc:
            print("Exiting program...")
            return False
    return True

def show_remove_patient():
    clear_screen()
    print("\n=== Hapus Pasien ===")
    print(queue)
    try:
        index_antrian = int(input("Enter index to remove: "))
        queue.drop(index=index_antrian, inplace=True)
        queue.to_csv('queue.csv', index=False)
        print("Patient removed successfully")
    except Exception as e:
        print(f"Error: {e}")

def show_edit_patient():
    clear_screen()
    print("\n=== Edit Pasien ===")
    print(queue)
    try:
        index_x = int(input("Enter row index: "))
        index_y = int(input("Enter column index: "))
        new_value = input("Enter new value: ") or queue.iloc[index_x, index_y]
        queue.iat[index_x, index_y] = new_value
        queue.to_csv('queue.csv', index=False)
        print("Patient data updated successfully")
    except Exception as e:
        print(f"Error: {e}")

def show_patient_list():
    clear_screen()
    print("\n=== Daftar Pasien ===")
    print(queue)
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    show_main_menu()
    with keyboard.Listener(on_press=main) as listener:
        listener.join()