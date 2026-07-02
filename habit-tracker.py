import os
import json
from datetime import datetime, timedelta

class HabitTracker:
    def __init__(self, filename="habit_data.json"):
        """
        Inisialisasi sistem pelacak kebiasaan.
        Menentukan file penyimpanan dan memuat data yang ada.
        """
        self.filename = filename
        self.habits = self.load_data()

    def load_data(self):
        """Memuat data kebiasaan dari file JSON."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ File data rusak. Membuat database baru...")
                return {}
        return {}

    def save_data(self):
        """Menyimpan data kebiasaan ke dalam file JSON."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.habits, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Gagal menyimpan data: {e}")

    def clear_screen(self):
        """Membersihkan layar terminal agar tampilan tetap rapi."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self):
        """Menampilkan header aplikasi yang estetis."""
        self.clear_screen()
        print("=" * 55)
        print("   SISTEM PELACAK KEBIASAAN HARIAN (HABIT TRACKER)   ")
        print("=" * 55)

    def add_habit(self):
        """Menambahkan kebiasaan baru ke dalam daftar."""
        self.show_header()
        print("[ Tambah Kebiasaan Baru ]\n")
        name = input("Masukkan nama kebiasaan baru: ").strip()
        
        if not name:
            print("\n❌ Nama kebiasaan tidak boleh kosong!")
            input("\nTekan Enter untuk kembali...")
            return

        if name in self.habits:
            print("\n⚠️ Kebiasaan ini sudah ada dalam daftar!")
            input("\nTekan Enter untuk kembali...")
            return

        description = input("Masukkan deskripsi singkat: ").strip()
        
        self.habits[name] = {
            "deskripsi": description,
            "tanggal_dibuat": datetime.now().strftime("%Y-%m-%d"),
            "riwayat_log": [], # Menyimpan tanggal-tanggal saat kebiasaan diselesaikan
            "streak_saat_ini": 0,
            "streak_tertinggi": 0
        }
        self.save_data()
        print(f"\n✅ Kebiasaan '{name}' berhasil ditambahkan!")
        input("\nTekan Enter untuk kembali...")

    def log_habit(self):
        """Mencatat kemajuan (log) kebiasaan untuk hari ini."""
        self.show_header()
        print("[ Catat Progress Harian ]\n")
        
        if not self.habits:
            print("Belum ada kebiasaan yang terdaftar. Silakan tambah kebiasaan terlebih dahulu.")
            input("\nTekan Enter untuk kembali...")
            return

        print("Daftar Kebiasaan Anda:")
        habit_list = list(self.habits.keys())
        for idx, name in enumerate(habit_list, 1):
            print(f"{idx}. {name}")

        try:
            pilihan = int(input("\nPilih nomor kebiasaan yang sudah selesai hari ini: "))
            if pilihan < 1 or pilihan > len(habit_list):
                raise ValueError
        except ValueError:
            print("\n❌ Pilihan tidak valid!")
            input("\nTekan Enter untuk kembali...")
            return

        selected_habit = habit_list[pilihan - 1]
        today_str = datetime.now().strftime("%Y-%m-%d")

        # Cek apakah sudah dicatat hari ini
        if today_str in self.habits[selected_habit]["riwayat_log"]:
            print(f"\n⚠️ Anda sudah mencatat kemajuan untuk '{selected_habit}' hari ini!")
        else:
            self.habits[selected_habit]["riwayat_log"].append(today_str)
            self.update_streaks(selected_habit)
            self.save_data()
            print(f"\n🎉 Bagus sekali! Kemajuan untuk '{selected_habit}' telah dicatat.")
            print(f"🔥 Streak saat ini: {self.habits[selected_habit]['streak_saat_ini']} hari!")
            
        input("\nTekan Enter untuk kembali...")

    def update_streaks(self, name):
        """Menghitung dan memperbarui jumlah streak harian berturut-turut."""
        history = sorted(self.habits[name]["riwayat_log"])
        if not history:
            return

        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in history]
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Cari tahu apakah log terakhir adalah hari ini atau kemarin
        last_date = dates[-1]
        if last_date != today and last_date != yesterday:
            # Streak terputus jika log terakhir lebih dari kemarin
            self.habits[name]["streak_saat_ini"] = 1
        else:
            # Hitung mundur dari log terakhir untuk menghitung runtutan hari
            streak = 1
            current_check = last_date
            
            # Iterasi riwayat dari belakang
            for d in reversed(dates[:-1]):
                if current_check - d == timedelta(days=1):
                    streak += 1
                    current_check = d
                elif current_check - d > timedelta(days=1):
                    break # Terputus
                    
            self.habits[name]["streak_saat_ini"] = streak

        # Perbarui rekor streak tertinggi jika terlampaui
        if self.habits[name]["streak_saat_ini"] > self.habits[name]["streak_tertinggi"]:
            self.habits[name]["streak_tertinggi"] = self.habits[name]["streak_saat_ini"]

    def view_statistics(self):
        """Menampilkan daftar kebiasaan beserta statistik streak-nya."""
        self.show_header()
        print("[ Status & Statistik Kebiasaan ]\n")
        
        if not self.habits:
            print("Belum ada data untuk ditampilkan.")
            input("\nTekan Enter untuk kembali...")
            return

        for name, info in self.habits.items():
            print(f"📌 Kebiasaan: {name}")
            print(f"   💬 Deskripsi : {info['deskripsi'] or '-'}")
            print(f"   📅 Sejak     : {info['tanggal_dibuat']}")
            print(f"   🔥 Streak    : {info['streak_saat_ini']} hari (Rekor: {info['streak_tertinggi']} hari)")
            total_days = len(info['riwayat_log'])
            print(f"   📊 Total Selesai: {total_days} kali")
            print("-" * 50)

        input("\nTekan Enter untuk kembali...")

    def delete_habit(self):
        """Menghapus kebiasaan dari sistem."""
        self.show_header()
        print("[ Hapus Kebiasaan ]\n")
        
        if not self.habits:
            print("Tidak ada kebiasaan yang bisa dihapus.")
            input("\nTekan Enter untuk kembali...")
            return

        print("Daftar Kebiasaan Anda:")
        habit_list = list(self.habits.keys())
        for idx, name in enumerate(habit_list, 1):
            print(f"{idx}. {name}")

        try:
            pilihan = int(input("\nPilih nomor kebiasaan yang ingin dihapus: "))
            if pilihan < 1 or pilihan > len(habit_list):
                raise ValueError
        except ValueError:
            print("\n❌ Pilihan tidak valid!")
            input("\nTekan Enter untuk kembali...")
            return

        selected_habit = habit_list[pilihan - 1]
        confirm = input(f"Apakah Anda yakin ingin menghapus '{selected_habit}'? (y/n): ").strip().lower()

        if confirm == 'y':
            del self.habits[selected_habit]
            self.save_data()
            print(f"\n🗑️ Kebiasaan '{selected_habit}' berhasil dihapus.")
        else:
            print("\nPenghapusan dibatalkan.")
            
        input("\nTekan Enter untuk kembali...")

    def run(self):
        """Menu utama aplikasi."""
        while True:
            self.show_header()
            print("1. Tambah Kebiasaan Baru")
            print("2. Catat Progress Harian")
            print("3. Lihat Status & Statistik")
            print("4. Hapus Kebiasaan")
            print("5. Keluar Aplikasi")
            print("=" * 55)
            
            pilihan = input("Pilih menu (1-5): ").strip()
            
            if pilihan == '1':
                self.add_habit()
            elif pilihan == '2':
                self.log_habit()
            elif pilihan == '3':
                self.view_statistics()
            elif pilihan == '4':
                self.delete_habit()
            elif pilihan == '5':
                self.show_header()
                print("\nTerima kasih telah menggunakan Habit Tracker! Tetap produktif! 💪\n")
                break
            else:
                print("\n❌ Pilihan tidak valid! Silakan coba lagi.")
                input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    tracker = HabitTracker()
    tracker.run()