import os
import sys
import time
import platform
import socket
import hashlib
import random
import subprocess
import ctypes
import getpass
import uuid
import re
import webbrowser
import urllib.request
import tempfile
import threading

_WALLPAPER_BASE_URL = None

_first_run = True

system = platform.system()
print(f"Detected OS: {system}")  # Должно вывести "Linux"



if os.name == "nt":
    os.system("")


W1 = "\033[97m"
W2 = "\033[37m"
W3 = "\033[90m"
DARK = "\033[38;5;237m"
GRAY = "\033[38;5;245m"
GRAY_DARK = "\033[38;5;240m"
BOLD = "\033[1m"
RESET = "\033[0m"

# --- Сначала определяем gradient_text ---
def gradient_text(text, brightness=1.0):
    result = ""
    length = max(len(text), 1)
    for i, char in enumerate(text):
        if char == " ":
            result += char
            continue
        ratio = i / length
        value = int((255 - ratio * 255) * brightness)
        value = max(0, min(255, value))
        result += f"\033[38;2;{value};{value};{value}m" + char
    return result + RESET

# --- Потом print_header ---
def print_header(animated=False):
    l1 = "..."
    ...
    for line in lines:
        if animated:
            print(f"{BOLD}{gradient_text(line)}{RESET}", flush=True)
            time.sleep(0.12)
        else:
            print(f"{BOLD}{gradient_text(line)}{RESET}")


def print_header(animated=False):
    l1 = " ████████╗██╗   ██╗███╗   ██╗██████╗     ████████╗██╗   ██╗███╗   ██╗██████╗     ██╗  ██╗██████╗  ██████╗ ██╗  ██╗"
    l2 = " ╚══██╔══╝██║   ██║████╗  ██║██╔════╝    ╚══██╔══╝██║   ██║████╗  ██║██╔════╝    ██║  ██║██╔══██╗██╔═══██╗██║ ██╔╝"
    l3 = "    ██║   ██║   ██║██╔██╗ ██║██║  ███╗      ██║   ██║   ██║██╔██╗ ██║██║  ███╗   ███████║██║  ██║██║   ██║█████═╝"
    l4 = "    ██║   ██║   ██║██║╚██╗██║██║   ██║      ██║   ██║   ██║██║╚██╗██║██║   ██║   ██╔══██║██║  ██║██║   ██║██╔═██╗"
    l5 = "    ██║   ╚██████╔╝██║ ╚████║╚██████╔╝      ██║   ╚██████╔╝██║ ╚████║╚██████╔╝   ██║  ██║╚██████╔╝╚██████╔██║  ██║"
    l6 = "    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝"

    lines = [l1, l2, l3, l4, l5, l6]

    for idx, line in enumerate(lines):
        if animated and idx > 0:
            time.sleep(0.05)  # задержка между строками
        print(f"{BOLD}{gradient_text(line)}{RESET}")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def loading(text, amount=12):
    frames = [
        "⠋", "⠙", "⠹", "⠸", "⠼",
        "⠴", "⠦", "⠧", "⠇", "⠏"
    ]

    for i in range(amount):
        print(
            f"\r{GRAY}[{frames[i % len(frames)]}]{RESET} "
            f"{gradient_text(text)}",
            end="",
            flush=True
        )
        time.sleep(0.07)

    print(
        f"\r{W1}[✓]{RESET} "
        f"{gradient_text(text)}"
    )


def line():
    print(
        f"{DARK}"
        + "─" * 106
        + f"{RESET}"
    )


def result(label, value):
    print(
        f"{GRAY}{label:<20}{RESET}"
        f"{gradient_text(str(value))}"
    )


def fn_01_veyon():
    loading("Starting Veyon bypass")
    print()

    result("BYPASS", "VEYON")
    result("Status", "BYPASSED")
    result("Platform", platform.system())
    result("Architecture", platform.machine())

    print()
    print(f"{W1}[+]{RESET} Veyon bypass restarted.")

    # Реальная логика: отложенное выключение и отмена
    system = platform.system()
    try:
        import subprocess
        if system == "Linux":
            print(f"{W1}[!]{RESET} Scheduling shutdown in 1 minute...")
            subprocess.Popen("shutdown -h +1", shell=True)
            time.sleep(10)  # даём время на остановку Veyon
            print(f"{W1}[!]{RESET} Cancelling shutdown...")
            subprocess.Popen("shutdown -c", shell=True)
            print(f"{W2}[✓]{RESET} Shutdown cancelled. Veyon service should be stopped.")
        elif system == "Windows":
            print(f"{W1}[!]{RESET} Scheduling shutdown in 60 seconds...")
            subprocess.Popen("shutdown /s /t 60", shell=True)
            time.sleep(10)
            print(f"{W1}[!]{RESET} Cancelling shutdown...")
            subprocess.Popen("shutdown /a", shell=True)
            print(f"{W2}[✓]{RESET} Shutdown cancelled. Veyon service should be stopped.")
        else:
            print(f"{W3}[!]{RESET} Shutdown not supported on this OS.")
    except Exception as e:
        print(f"{W3}[!]{RESET} Error: {e}")

    print()
    print(f"{W1}[+]{RESET} Veyon bypass completed.")


def set_wallpaper(image_path):
    system = platform.system()
    try:
        if system == "Windows":
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            return True
        elif system == "Linux":
            import subprocess
            uri = "file://" + os.path.abspath(image_path)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri], check=True)
            return True
        else:
            print(f"{W3}[!] Wallpaper setting not supported on {system}")
            return False
    except Exception as e:
        print(f"{W3}[!] Error setting wallpaper: {e}")
        return False

def download_wallpaper(filename, base_url):
    url = base_url.rstrip('/') + '/' + filename + '.png'
    try:
        fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(fd)
        urllib.request.urlretrieve(url, temp_path)
        return temp_path
    except Exception as e:
        print(f"{W3}[!] Download error: {e}")
        return None

def schedule_wallpaper(image_path, delay_minutes):
    def apply():
        time.sleep(delay_minutes * 60)
        if set_wallpaper(image_path):
            print(f"\n{W1}[+] Wallpaper applied as scheduled.")
        else:
            print(f"\n{W3}[!] Failed to apply scheduled wallpaper.")
    thread = threading.Thread(target=apply, daemon=True)
    thread.start()

def fn_02_wallpapers():
    loading("Loading Wallpapers")
    print()

    wallpapers = {
        "1": {"display": "TungTungHook", "url": "https://raw.githubusercontent.com/tth-bio/tungtung1/main/tungtunghook.jpg"},
        "2": {"display": "Utug", "url": "https://raw.githubusercontent.com/tth-bio/tungtung1/main/utug.jpg"},
        "3": {"display": "mr robot", "url": "https://raw.githubusercontent.com/tth-bio/tungtung1/main/mrrobot.jpg"}
    }

    print(f"{GRAY}Available wallpapers:{RESET}")
    for key, wp in wallpapers.items():
        print(f"  {key}. {gradient_text(wp['display'])}")

    choice = input(f"\n{W1}[TungTungHook]{W2} Select wallpaper number: {RESET}").strip()
    if choice not in wallpapers:
        print(f"{W3}[!] Invalid choice.")
        return

    selected = wallpapers[choice]
    url = selected['url']
    display_name = selected['display']

    print(f"\n{GRAY}Set wallpaper:{RESET}")
    print("  1. Now")
    print("  2. After N minutes")
    time_choice = input(f"{W1}[TungTungHook]{W2} Choose option (1 or 2): {RESET}").strip()

    if time_choice == "1":
        delay_minutes = 0
    elif time_choice == "2":
        try:
            delay_minutes = int(input(f"{W2}Enter minutes: {RESET}").strip())
            if delay_minutes <= 0:
                print(f"{W3}[!] Minutes must be positive.")
                return
        except ValueError:
            print(f"{W3}[!] Enter a valid number.")
            return
    else:
        print(f"{W3}[!] Invalid option.")
        return

    print(f"{GRAY}[*] Downloading {display_name}...{RESET}")
    try:
        fd, temp_path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        urllib.request.urlretrieve(url, temp_path)
        image_path = temp_path
    except Exception as e:
        print(f"{W3}[!] Download error: {e}")
        return

    print(f"{W1}[+] File downloaded: {image_path}")

    if delay_minutes == 0:
        if set_wallpaper(image_path):
            print(f"{W1}[+] Wallpaper {display_name} applied.")
        else:
            print(f"{W3}[!] Failed to apply wallpaper.")
    else:
        print(f"{W1}[+] Wallpaper will be applied in {delay_minutes} minute(s).")
        schedule_wallpaper(image_path, delay_minutes)

    print()
    print(f"{W1}[+] Operation completed.")


def fn_03_porthack():
    loading("Starting Porthack")
    print()

    system = platform.system()

    if system == "Linux":
        try:
            import subprocess
            # Используем ss для прослушивающих портов
            output = subprocess.check_output("ss -tulpn", shell=True, text=True)
            lines = output.splitlines()
            print(f"{GRAY}[LISTENING PORTS]{RESET}")
            for line in lines[1:]:  # пропускаем заголовок
                parts = line.split()
                if len(parts) >= 5:
                    state = parts[0]
                    recv_q = parts[1]
                    send_q = parts[2]
                    local = parts[4]
                    # Показываем только прослушивающие
                    if "LISTEN" in state:
                        print(f"   {GRAY_DARK}├─{RESET} {gradient_text(local)} {W2}→{RESET} {gradient_text(state)}")
        except Exception as e:
            print(f"{W3}[!]{RESET} Error: {e}")
    elif system == "Windows":
        try:
            import subprocess
            output = subprocess.check_output("netstat -an", shell=True, text=True, encoding='cp866')
            lines = output.splitlines()
            print(f"{GRAY}[ACTIVE CONNECTIONS]{RESET}")
            for line in lines[3:]:
                if "LISTENING" in line or "ESTABLISHED" in line:
                    print(f"   {GRAY_DARK}├─{RESET} {gradient_text(line.strip())}")
        except:
            print("Could not retrieve ports.")
    else:
        print("Port scanning not implemented for this OS.")

    print()
    print(f"{W1}[+]{RESET} Local demonstration completed.")


def fn_04_misc():
    loading("Starting UAC bypass")
    print()

    system = platform.system()

    if system == "Windows":
        try:
            # 1. Закрываем все окна cmd
            print(f"{W1}[!]{RESET} Closing all console windows...")
            os.system("taskkill /F /IM cmd.exe 2>nul")
            time.sleep(1)

            # 2. Проверяем, есть ли уже права администратора
            if ctypes.windll.shell32.IsUserAnAdmin():
                print(f"{W2}[✓]{RESET} Already running as admin.")
            else:
                # 3. Запускаем cmd с правами администратора, окно сразу сворачивается
                print(f"{W1}[!]{RESET} Requesting admin privileges...")
                ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",                      # запрос UAC
                    "cmd.exe",                    # программа
                    "/k title Yandex browser",    # заголовок окна
                    None,
                    6                             # SW_MINIMIZE – окно свернуто в панель
                )
                print(f"{W2}[✓]{RESET} Admin CMD requested. UAC dialog should appear with title 'Yandex browser'.")
                print(f"{W2}[✓]{RESET} The console will start minimized in taskbar.")
                time.sleep(2)

        except Exception as e:
            print(f"{W3}[!]{RESET} UAC error: {e}")

    else:
        # Linux / МОС
        try:
            print(f"{W1}[!]{RESET} Closing all terminal windows...")
            os.system("pkill -f 'gnome-terminal|konsole|xterm' 2>/dev/null")
            time.sleep(1)

            print(f"{W1}[!]{RESET} Requesting sudo privileges...")
            subprocess.run("sudo -v", shell=True, check=False)

            # Запускаем xterm свернутым (иконка в панели)
            subprocess.Popen(
                "xterm -iconic -e bash &",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"{W2}[✓]{RESET} Hidden terminal launched (minimized).")
        except Exception as e:
            print(f"{W3}[!]{RESET} Linux error: {e}")

    print()
    print(f"{W1}[+]{RESET} UAC operation completed.")

def fn_05_screamer():
    loading("Open TungTungHook website...")
    print()

    try:
        import webbrowser
        webbrowser.open("https://TungTungHook.cc")
        print(f"{W1}[+]{RESET} Website opened in your default browser.")
    except Exception as e:
        print(f"{W3}[!]{RESET} Could not open browser: {e}")

    print()
    print(f"{W1}[+]{RESET} TungTungHook website opened.")


def fn_06_noise():
    loading("Generating turtle")
    print()

    try:
        import turtle
        import random

        # Настройка экрана
        screen = turtle.Screen()
        screen.bgcolor("black")
        screen.title("TungTungHook - Italian Brainrot")
        screen.setup(width=1100, height=500)
        screen.tracer(0)

        t = turtle.Turtle()
        t.speed(0)
        t.penup()

        colors = ["#ff0040", "#ff6600", "#ffcc00", "#00ff66", "#00ccff", "#9900ff", "#ff00ff", "#00ffff"]
        text = "TungTungHook"
        font_size = 70
        x_start = -500
        y_start = -20

        # Рисуем буквы с разными цветами и белой тенью
        for i, char in enumerate(text):
            # Основная буква
            t.goto(x_start + i * (font_size * 0.7), y_start)
            t.pendown()
            t.pencolor(colors[i % len(colors)])
            t.write(char, font=("Arial Black", font_size, "bold"))
            t.penup()

            # Тень (смещённая белая копия)
            t.goto(x_start + i * (font_size * 0.7) + 4, y_start - 4)
            t.pendown()
            t.pencolor("white")
            t.write(char, font=("Arial Black", font_size, "bold"))
            t.penup()

        # Звёзды вокруг
        star_positions = [(-480, 120), (-200, 150), (100, -80), (350, 130), (450, -120), (-300, -120)]
        for x, y in star_positions:
            t.goto(x, y)
            t.pendown()
            t.pencolor(random.choice(colors))
            t.begin_fill()
            for _ in range(5):
                t.forward(15)
                t.right(144)
            t.end_fill()
            t.penup()

        # Вращающиеся линии (эффект неона)
        t.goto(0, -180)
        t.pendown()
        t.pencolor("#ff00ff")
        for _ in range(36):
            t.forward(400)
            t.backward(400)
            t.left(10)

        screen.update()
        turtle.done()

        print(f"{W1}[+]{RESET} TungTungHook drawn successfully!")

    except Exception as e:
        print(f"{W3}[!]{RESET} Turtle error: {e}")

    print()
    print(f"{W1}[+]{RESET} Opened.")

def fn_07_butterfly():
    loading("Scanning users")
    print()

    system = platform.system()
    arch = platform.machine()
    hostname = socket.gethostname()

    result("OS", system)
    result("Architecture", arch)
    result("Hostname", hostname)

    import getpass
    current_user = getpass.getuser()
    result("Current user", current_user)

    # Проверка администратора в зависимости от ОС
    is_admin = False
    if system == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            is_admin = False
    else:
        # Linux, macOS, МОС
        try:
            is_admin = os.geteuid() == 0
        except AttributeError:
            is_admin = False

    result("Administrator", "Yes" if is_admin else "No")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "127.0.0.1"
    result("Local IP", local_ip)

    import uuid
    mac_int = uuid.getnode()
    mac_hex = ':'.join(('{:02x}'.format((mac_int >> i) & 0xff) for i in range(40, -1, -8)))
    result("MAC Address", mac_hex)

    print()
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    # ---------- Получаем список пользователей и их детали ----------
    print(f"{GRAY}[*] User accounts on this machine:{RESET}")
    users = []

    if system == "Windows":
        try:
            import subprocess
            # Получаем список пользователей через net user
            output = subprocess.check_output("net user", shell=True, text=True, encoding='cp866')
            lines = output.splitlines()
            user_list = []
            for line in lines:
                parts = line.split()
                for part in parts:
                    if len(part) > 1 and not any(c in part for c in '.-_'):
                        if part not in ['User', 'accounts', '----', 'Success']:
                            user_list.append(part)
            # Для каждого пользователя получаем детали
            for username in user_list[:10]:
                try:
                    detail = subprocess.check_output(f"net user {username}", shell=True, text=True, encoding='cp866')
                    home = ""
                    last_login = ""
                    is_admin_flag = False
                    for dline in detail.splitlines():
                        if "Домашний каталог" in dline or "Home directory" in dline:
                            home = dline.split(":")[-1].strip()
                        if "Последний вход" in dline or "Last logon" in dline:
                            last_login = dline.split(":")[-1].strip()
                        if "Администратор" in dline or "Administrator" in dline:
                            if "Да" in dline or "Yes" in dline:
                                is_admin_flag = True
                    # Проверяем активен ли сейчас
                    active = "Inactive"
                    try:
                        who = subprocess.check_output("query user", shell=True, text=True, encoding='cp866')
                        if username in who:
                            active = "Active (logged in)"
                    except:
                        pass
                    users.append({
                        "name": username,
                        "admin": "Yes" if is_admin_flag else "No",
                        "home": home if home else "N/A",
                        "last_login": last_login if last_login else "Never",
                        "active": active
                    })
                except:
                    users.append({
                        "name": username,
                        "admin": "Unknown",
                        "home": "N/A",
                        "last_login": "Unknown",
                        "active": "Unknown"
                    })
        except Exception as e:
            users = [{"name": f"(Error: {e})", "admin": "", "home": "", "last_login": "", "active": ""}]
    else:
        # Linux / МОС / macOS
        try:
            import subprocess
            with open('/etc/passwd', 'r') as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    parts = line.split(':')
                    if len(parts) >= 7:
                        username = parts[0]
                        try:
                            uid = int(parts[2])
                            # В Linux пользователи обычно имеют UID >= 1000
                            if uid >= 1000:
                                home = parts[5]
                                # Проверяем администратора (группы sudo/wheel/admin)
                                is_admin_flag = False
                                try:
                                    groups = subprocess.check_output(f"groups {username}", shell=True, text=True)
                                    if "sudo" in groups or "wheel" in groups or "admin" in groups:
                                        is_admin_flag = True
                                except:
                                    pass
                                # Последний вход
                                last_login = "Never"
                                try:
                                    lastlog = subprocess.check_output(f"lastlog -u {username}", shell=True, text=True)
                                    lines = lastlog.splitlines()
                                    if len(lines) > 1:
                                        last_login = " ".join(lines[1].split()[3:])
                                except:
                                    pass
                                # Активен сейчас?
                                active = "Inactive"
                                try:
                                    who = subprocess.check_output("who", shell=True, text=True)
                                    if username in who:
                                        active = "Active (logged in)"
                                except:
                                    pass
                                users.append({
                                    "name": username,
                                    "admin": "Yes" if is_admin_flag else "No",
                                    "home": home if home else "N/A",
                                    "last_login": last_login if last_login else "Never",
                                    "active": active
                                })
                        except:
                            pass
        except Exception as e:
            users = [{"name": f"(Error: {e})", "admin": "", "home": "", "last_login": "", "active": ""}]

    # ---------- Вывод карточек пользователей ----------
    if users and users[0]["name"] != "(Could not retrieve)":
        for idx, user in enumerate(users[:15]):
            print()
            print(f"   {GRAY_DARK}╭─ User:{RESET} {gradient_text(user['name'])}")
            print(f"   {GRAY_DARK}│{RESET}  Administrator: {gradient_text(user['admin'])}")
            print(f"   {GRAY_DARK}│{RESET}  Home: {gradient_text(user['home'])}")
            print(f"   {GRAY_DARK}│{RESET}  Last login: {gradient_text(user['last_login'])}")
            print(f"   {GRAY_DARK}│{RESET}  Status: {gradient_text(user['active'])}")
            print(f"   {GRAY_DARK}╰─{RESET}")
    else:
        print(f"   {GRAY}Could not retrieve user details.{RESET}")

    print()
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    # ---------- ARP-таблица (соседи) ----------
    print(f"{GRAY}[*] ARP table (active devices in local network):{RESET}")
    arp_data = []
    try:
        import subprocess
        import re
        if system == "Windows":
            output = subprocess.check_output("arp -a", shell=True, text=True, encoding='cp866')
            pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2})')
        else:
            output = subprocess.check_output("arp -n", shell=True, text=True)
            pattern = re.compile(r'\(?(\d+\.\d+\.\d+\.\d+)\)?\s+at\s+([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})')

        for line in output.splitlines():
            match = pattern.search(line)
            if match:
                ip = match.group(1)
                mac = match.group(2)
                if mac.lower() not in ('ff-ff-ff-ff-ff-ff', 'ff:ff:ff:ff:ff:ff'):
                    arp_data.append((ip, mac))
    except:
        arp_data = []

    if arp_data:
        for ip, mac in arp_data[:20]:
            print(f"   {GRAY_DARK}├─{RESET} IP {gradient_text(ip)} {GRAY_DARK}→{RESET} MAC {gradient_text(mac)}")
    else:
        print(f"   {GRAY}No ARP entries found.{RESET}")

    print()
    print(f"{W1}[+]{RESET} Users and network scan completed.")


def fn_08_errors():
    loading("Running Error Diagnostics")
    print()

    system = platform.system()
    error_messages = [
        "Critical error: Memory access violation at 0x00000000",
        "System crash: Kernel panic - not syncing",
        "Fatal exception: Segmentation fault in process 1234",
        "DLL injection failed: Access denied",
        "Registry error: Cannot open key HKEY_LOCAL_MACHINE\\SYSTEM",
        "Network connection lost: Timeout for 192.168.1.1",
        "Disk failure: Bad sector detected on /dev/sda1",
        "CPU overheating: Temperature 95°C, system halted",
        "Power surge detected: Shutting down to protect hardware",
        "USB device malfunction: Device not recognized",
        "File system corruption: NTFS error code 0x00000024",
        "Service 'Veyon' stopped unexpectedly",
        "Application hang: TungTungHook.exe not responding",
        "Windows update error: 0x80070002",
        "Display driver stopped responding and has recovered"
    ]

    if system == "Windows":
        try:
            import tkinter as tk
            import random
            import threading
            import ctypes

            # Звук ошибки
            ctypes.windll.user32.MessageBeep(0x10)

            # Получаем размер экрана
            root = tk.Tk()
            root.withdraw()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.destroy()

            windows = []

            for i in range(15):
                x = random.randint(0, screen_width - 400)
                y = random.randint(0, screen_height - 150)

                win = tk.Tk()
                win.title(f"TUNGTUNGHOOK ON TOP - Error {i+1}")
                win.geometry(f"400x150+{x}+{y}")
                win.resizable(False, False)
                win.attributes('-topmost', True)

                label = tk.Label(win, text=error_messages[i], wraplength=380,
                                 fg="red", font=("Arial", 10, "bold"))
                label.pack(pady=20)

                btn = tk.Button(win, text="OK", command=win.destroy, width=10)
                btn.pack(pady=10)

                windows.append(win)

            # Запускаем каждое окно в отдельном потоке
            def run_window(win):
                win.mainloop()

            for win in windows:
                t = threading.Thread(target=run_window, args=(win,), daemon=True)
                t.start()

            time.sleep(0.5)

        except Exception as e:
            print(f"{W3}[!]{RESET} Error showing windows: {e}")
            # Fallback через стандартный MessageBox
            import ctypes
            for i, msg in enumerate(error_messages[:15]):
                ctypes.windll.user32.MessageBoxW(None, msg, f"TUNGTUNGHOOK ON TOP - Error {i+1}", 0x10)
                time.sleep(0.1)

    elif system == "Linux":
        try:
            import subprocess
            import random
            import re

            # Определяем разрешение экрана
            output = subprocess.check_output("xrandr --current | grep '*' | head -1", shell=True, text=True)
            match = re.search(r'(\d+)x(\d+)', output)
            if match:
                screen_width = int(match.group(1))
                screen_height = int(match.group(2))
            else:
                screen_width = 1920
                screen_height = 1080

            # Звук ошибки
            try:
                subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/dialog-error.oga"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass

            for i in range(15):
                x = random.randint(0, screen_width - 400)
                y = random.randint(0, screen_height - 150)
                title = f"TUNGTUNGHOOK ON TOP - Error {i+1}"
                text = error_messages[i]
                subprocess.Popen(
                    ["zenity", "--error", "--title", title, "--text", text,
                     "--width=400", "--height=150", "--geometry", f"400x150+{x}+{y}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                time.sleep(0.05)

        except Exception as e:
            print(f"{W3}[!]{RESET} Error showing windows: {e}")
            # Fallback через notify-send
            for i, msg in enumerate(error_messages[:15]):
                subprocess.Popen(["notify-send", f"TUNGTUNGHOOK ON TOP - Error {i+1}", msg, "-u", "critical"])
                time.sleep(0.1)

    else:
        # Для других ОС — вывод в консоль
        for i, msg in enumerate(error_messages[:15]):
            print(f"{W3}[ERROR {i+1}]{RESET} {gradient_text('TUNGTUNGHOOK ON TOP → ' + msg)}")

    print()
    print(f"{W1}[✓]{RESET} Error spamming completed.")


def fn_09_cpp():
    loading("Starting C++ Module")

    result("Language", "C++")
    result("Standard", "C++17")
    result("Compiler", "MSVC / GCC")
    result("Status", "READY")

    print()
    print(
        f"{GRAY}Example:{RESET}"
    )

    code = [
        "#include <iostream>",
        "",
        "int main() {",
        '    std::cout << "TungTungHook";',
        "    return 0;",
        "}"
    ]

    for row in code:
        print(
            f"{GRAY_DARK}│{RESET} "
            f"{gradient_text(row)}"
        )


def fn_10_lua():
    loading("Starting Lua Module")

    result("Language", "Lua")
    result("Version", "5.x")
    result("Runtime", "READY")

    print()

    code = [
        'local name = "TungTungHook"',
        'print(name)',
        "",
        "for i = 1, 5 do",
        "    print(i)",
        "end"
    ]

    for row in code:
        print(
            f"{GRAY_DARK}│{RESET} "
            f"{gradient_text(row)}"
        )


def fn_11_python():
    loading("Starting Network Scanner")
    print()

    system = platform.system()
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("Network Scan Report")
    report_lines.append(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"OS: {system}")
    report_lines.append("=" * 60)
    report_lines.append("")

    # ---------- 1. Информация о текущем компьютере ----------
    print(f"{GRAY}[*] Gathering local machine info...{RESET}")
    report_lines.append("[LOCAL MACHINE]")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"
    mac_int = uuid.getnode()
    mac_hex = ':'.join(('{:02x}'.format((mac_int >> i) & 0xff) for i in range(40, -1, -8)))
    print(f"{GRAY}Hostname:{RESET} {gradient_text(hostname)}")
    print(f"{GRAY}IP:{RESET} {gradient_text(local_ip)}")
    print(f"{GRAY}MAC:{RESET} {gradient_text(mac_hex)}")
    report_lines.append(f"Hostname: {hostname}")
    report_lines.append(f"IP: {local_ip}")
    report_lines.append(f"MAC: {mac_hex}")

    # ---------- 2. Сканирование портов на localhost ----------
    print(f"\n{GRAY}[*] Scanning localhost (127.0.0.1) for open ports...{RESET}")
    report_lines.append("\n[LOCALHOST PORT SCAN]")
    local_ports = scan_common_ports("127.0.0.1")
    if local_ports:
        print(f"{W1}[+] Open ports on localhost:{RESET}")
        for port, service, vuln in local_ports:
            vuln_tag = f" {W1}[!]{RESET}" if vuln else ""
            print(f"   {GRAY_DARK}├─{RESET} Port {gradient_text(str(port))} {W3}OPEN{RESET} -> {gradient_text(service)}{vuln_tag}")
            report_lines.append(f"Port {port}: OPEN - {service}" + (" (VULNERABLE)" if vuln else ""))
    else:
        print(f"{GRAY}No open ports found on localhost.{RESET}")
        report_lines.append("No open ports found on localhost.")

    # ---------- 3. Сканирование локальной сети (ARP) ----------
    print(f"\n{GRAY}[*] Scanning local network for active devices...{RESET}")
    report_lines.append("\n[ACTIVE NETWORK DEVICES]")
    arp_devices = get_arp_devices(system)
    if arp_devices:
        print(f"{W1}[+] Found {len(arp_devices)} active devices in local network.{RESET}")
        report_lines.append(f"Total devices found: {len(arp_devices)}")
        for idx, (ip, mac, hostname) in enumerate(arp_devices, 1):
            # Пропускаем localhost (уже отсканирован)
            if ip == "127.0.0.1" or ip.startswith("127."):
                continue
            print()
            print(f"   {GRAY_DARK}╭─ Device #{idx}{RESET}")
            print(f"   {GRAY_DARK}│{RESET}  IP: {gradient_text(ip)}")
            print(f"   {GRAY_DARK}│{RESET}  MAC: {gradient_text(mac)}")
            print(f"   {GRAY_DARK}│{RESET}  Hostname: {gradient_text(hostname)}")
            report_lines.append(f"Device #{idx}: IP={ip}, MAC={mac}, Hostname={hostname}")

            # Сканируем порты для этого устройства
            ports = scan_common_ports(ip)
            if ports:
                print(f"   {GRAY_DARK}│{RESET}  Open ports:")
                for port, service, vuln in ports:
                    vuln_tag = f" {W1}[!]{RESET}" if vuln else ""
                    print(f"   {GRAY_DARK}│{RESET}    {gradient_text(str(port))} -> {gradient_text(service)}{vuln_tag}")
                    report_lines.append(f"  Port {port}: OPEN - {service}" + (" (VULNERABLE)" if vuln else ""))
            else:
                print(f"   {GRAY_DARK}│{RESET}  Open ports: {gradient_text('none')}")
                report_lines.append("  No open ports found.")
            print(f"   {GRAY_DARK}╰─{RESET}")
    else:
        print(f"{W3}[!] No ARP entries found. Is the network active?{RESET}")
        report_lines.append("No ARP entries found.")

    # ---------- 4. Сохранение отчёта ----------
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop):
            desktop = os.path.expanduser("~")
        filename = f"network_scan_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(desktop, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        print(f"\n{W1}[+]{RESET} Report saved to: {gradient_text(filepath)}")
    except Exception as e:
        print(f"{W3}[!] Could not save report: {e}")

    print()
    print(f"{DARK}" + "─" * 106 + f"{RESET}")
    print(f"{W1}[+]{RESET} Network scan completed.")


# Вспомогательные функции для сканера (добавьте их выше или внутрь)

def scan_common_ports(target_ip):
    """Сканирует популярные порты на заданном IP и возвращает список (port, service, is_vulnerable)"""
    ports_to_scan = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        111: "RPCbind",
        135: "MS RPC",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        6379: "Redis",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt",
        3000: "Node.js",
        5000: "Flask",
        8000: "Web-Alt"
    }
    vulnerable_ports = {
        21: True,   # FTP уязвим
        23: True,   # Telnet небезопасен
        445: True,  # SMB (EternalBlue)
        3389: True, # RDP (BlueKeep)
        3306: True, # MySQL (дефолтные креды)
        5900: True, # VNC (дефолтный пароль)
        6379: True, # Redis (неаутентифицированный)
        27017: True # MongoDB (неаутентифицированный)
    }
    open_ports = []
    for port, service in ports_to_scan.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                is_vuln = vulnerable_ports.get(port, False)
                open_ports.append((port, service, is_vuln))
            sock.close()
        except:
            pass
    return open_ports

def get_arp_devices(system):
    """Возвращает список (ip, mac, hostname) из ARP-таблицы"""
    arp_data = []
    try:
        if system == "Windows":
            output = subprocess.check_output("arp -a", shell=True, text=True, encoding='cp866')
            pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2}-[0-9a-fA-F]{2})')
        else:
            output = subprocess.check_output("arp -n", shell=True, text=True)
            pattern = re.compile(r'\(?(\d+\.\d+\.\d+\.\d+)\)?\s+at\s+([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})')

        for line in output.splitlines():
            match = pattern.search(line)
            if match:
                ip = match.group(1)
                mac = match.group(2)
                if mac.lower() not in ('ff-ff-ff-ff-ff-ff', 'ff:ff:ff:ff:ff:ff', '00-00-00-00-00-00', '00:00:00:00:00:00'):
                    hostname = "Unknown"
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        pass
                    arp_data.append((ip, mac, hostname))
    except:
        pass
    return arp_data


def fn_12_all_nets():
    loading("Starting All NETS")
    print()

    system = platform.system()

    if system == "Linux":
        try:
            import subprocess
            import re
            # Получаем список интерфейсов и IP
            output = subprocess.check_output("ip addr show", shell=True, text=True)
            interfaces = re.findall(r'^\d+: (\w+):', output, re.MULTILINE)
            for iface in interfaces:
                print(f"{GRAY}[INTERFACE]{RESET} {gradient_text(iface)}")
                # Получаем IP для интерфейса
                ip_output = subprocess.check_output(f"ip addr show {iface}", shell=True, text=True)
                ips = re.findall(r'inet (\d+\.\d+\.\d+\.\d+/\d+)', ip_output)
                for ip in ips:
                    print(f"   {GRAY_DARK}├─{RESET} IP: {gradient_text(ip)}")
                # MAC
                mac = re.search(r'link/ether ([0-9a-f:]+)', ip_output)
                if mac:
                    print(f"   {GRAY_DARK}├─{RESET} MAC: {gradient_text(mac.group(1))}")
                # Состояние
                state = re.search(r'state (\w+)', ip_output)
                if state:
                    print(f"   {GRAY_DARK}├─{RESET} State: {gradient_text(state.group(1))}")
            # Шлюз по умолчанию
            route = subprocess.check_output("ip route show default", shell=True, text=True)
            gateway = re.search(r'via (\d+\.\d+\.\d+\.\d+)', route)
            if gateway:
                print(f"{GRAY}[GATEWAY]{RESET} {gradient_text(gateway.group(1))}")
        except Exception as e:
            print(f"{W3}[!]{RESET} Error: {e}")
    elif system == "Windows":
        try:
            import subprocess
            output = subprocess.check_output("ipconfig /all", shell=True, text=True, encoding='cp866')
            print(gradient_text(output[:1000]))  # краткий вывод
        except:
            print("Could not retrieve network info.")
    else:
        print("Network info not available for this OS.")

    print()
    print(f"{W1}[+]{RESET} Network information loaded.")


def fn_13_how_to_use():
    loading("Loading Manual")

    print()

    instructions = [
        "Select a number of function from 1 to 16.",
        "The selected function will start.",
        "Wait for the function to finish.",
        "Press ENTER to return to menu.",
        "Use Q to exit.",

        "Remember sahur never sleeps..."
    ]

    for instruction in instructions:
        print(
            f"{GRAY}[→]{RESET} "
            f"{gradient_text(instruction)}"
        )


def fn_14_py_syntax():
    loading("Opening Python Syntax Manual")
    print()
    # Разделитель (без вызова line())
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    print(f" {W1}╭─{RESET} {gradient_text('PYTHON BASIC SYNTAX')}")
    print(f" {W1}│{RESET}")

    examples = [
        ("Variables", [
            "name = 'TungTungHook'",
            "age = 25",
            "scores = [10, 20, 30]",
            "config = {'host': 'localhost', 'port': 8080}"
        ]),
        ("Conditionals", [
            "if age >= 18:",
            "    print('Adult')",
            "elif age >= 13:",
            "    print('Teen')",
            "else:",
            "    print('Child')"
        ]),
        ("Loops", [
            "for i in range(5):",
            "    print(i)",
            "",
            "while age > 0:",
            "    age -= 1"
        ]),
        ("Functions", [
            "def hello(name):",
            "    return f'Hello, {name}'",
            "",
            "print(hello('TungTungHook'))"
        ]),
        ("Input / Output", [
            "name = input('Enter name: ')",
            "print(f'Welcome, {name}')"
        ]),
        ("Imports", [
            "import math",
            "print(math.sqrt(16))"
        ])
    ]

    for title, code_lines in examples:  # переменная code_lines, а не line
        print(f" {W1}│{RESET} {gradient_text(f'─── {title} ───')}")
        for code_line in code_lines:   # переменная code_line
            print(f" {W1}│{RESET}   {gradient_text(code_line)}")
        print()

    print(f" {W1}│{RESET}")
    print(f" {W1}╰─{RESET} {gradient_text('📖 Full documentation (RU): https://docs.python.org/ru/3/')}")
    print()
    # Ещё один разделитель
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    print(f"{W1}[+]{RESET} Python syntax manual loaded.")


def fn_15_lua_helper():
    loading("Opening Lua helper Manual")
    print()
    # Разделитель (без вызова line())
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    print(f" {W1}╭─{RESET} {gradient_text('LUA BASIC SYNTAX')}")
    print(f" {W1}│{RESET}")

    examples = [
        ("Variables & Types", [
            "local name = 'TungTungHook'",
            "local age = 25",
            "local is_ready = true",
            "local pi = 3.1415"
        ]),
        ("Tables (arrays / dicts)", [
            "local scores = {10, 20, 30}",
            "local config = {host='localhost', port=8080}",
            "print(scores[1])      -- 10",
            "print(config.host)    -- localhost"
        ]),
        ("Conditionals", [
            "if age >= 18 then",
            "    print('Adult')",
            "elseif age >= 13 then",
            "    print('Teen')",
            "else",
            "    print('Child')",
            "end"
        ]),
        ("Loops", [
            "for i = 1, 5 do",
            "    print(i)",
            "end",
            "",
            "local i = 1",
            "while i <= 5 do",
            "    print(i)",
            "    i = i + 1",
            "end"
        ]),
        ("Functions", [
            "function hello(name)",
            "    return 'Hello, ' .. name",
            "end",
            "",
            "print(hello('TungTungHook'))"
        ]),
        ("Standard libraries", [
            "table.insert(scores, 40)",
            "string.format('Value: %d', age)",
            "math.random(1, 10)",
            "io.write('Enter name: ')"
        ])
    ]

    for title, code_lines in examples:  # переменная code_lines
        print(f" {W1}│{RESET} {gradient_text(f'─── {title} ───')}")
        for code_line in code_lines:   # переменная code_line
            print(f" {W1}│{RESET}   {gradient_text(code_line)}")
        print()

    print(f" {W1}│{RESET}")
    print(f" {W1}╰─{RESET} {gradient_text('📖 Full documentation (RU): https://www.lua.org/manual/5.3/ru/')}")
    print()
    # Ещё один разделитель
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    print(f"{W1}[+]{RESET} Lua helper manual loaded.")


def fn_16_reverse_eng():
    loading("Opening Reverse Engineering Manual")
    print()

    # Разделитель без вызова line()
    print(f"{DARK}" + "─" * 106 + f"{RESET}")

    system = platform.system()
    arch = platform.machine()
    hostname = socket.gethostname()
    processor = platform.processor()
    python_ver = platform.python_version()

    print(f" {W1}╭─{RESET} {gradient_text('SYSTEM INFORMATION')}")
    print(f" {W1}│{RESET}")
    print(f" {W1}│{RESET}   {GRAY}OS:{RESET} {gradient_text(system)}")
    print(f" {W1}│{RESET}   {GRAY}Architecture:{RESET} {gradient_text(arch)}")
    print(f" {W1}│{RESET}   {GRAY}Hostname:{RESET} {gradient_text(hostname)}")
    print(f" {W1}│{RESET}   {GRAY}Processor:{RESET} {gradient_text(processor if processor else 'Unknown')}")
    print(f" {W1}│{RESET}   {GRAY}Python Version:{RESET} {gradient_text(python_ver)}")
    print(f" {W1}│{RESET}")

    # Сетевая информация
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "127.0.0.1"
    print(f" {W1}│{RESET}   {GRAY}Local IP:{RESET} {gradient_text(local_ip)}")

    # MAC-адрес
    import uuid
    mac_int = uuid.getnode()
    mac_hex = ':'.join(('{:02x}'.format((mac_int >> i) & 0xff) for i in range(40, -1, -8)))
    print(f" {W1}│{RESET}   {GRAY}MAC Address:{RESET} {gradient_text(mac_hex)}")

    # Информация о пользователе
    import getpass
    current_user = getpass.getuser()
    print(f" {W1}│{RESET}   {GRAY}Current User:{RESET} {gradient_text(current_user)}")

    # Права администратора
    is_admin = False
    if system == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            is_admin = False
    else:
        try:
            is_admin = os.geteuid() == 0
        except AttributeError:
            is_admin = False
    print(f" {W1}│{RESET}   {GRAY}Administrator:{RESET} {gradient_text('Yes' if is_admin else 'No')}")

    # Объём оперативной памяти (через os, без psutil)
    try:
        if system == "Windows":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            memoryStatus = MEMORYSTATUSEX()
            memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus)):
                total_ram = memoryStatus.ullTotalPhys // (1024**3)
                avail_ram = memoryStatus.ullAvailPhys // (1024**3)
            else:
                total_ram = avail_ram = "Unknown"
        else:
            # Linux: читаем /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        total_ram = int(line.split()[1]) // (1024**2)  # в ГБ
                    if line.startswith('MemAvailable:'):
                        avail_ram = int(line.split()[1]) // (1024**2)
            total_ram = total_ram if 'total_ram' in locals() else "Unknown"
            avail_ram = avail_ram if 'avail_ram' in locals() else "Unknown"
    except:
        total_ram = "Unknown"
        avail_ram = "Unknown"

    print(f" {W1}│{RESET}   {GRAY}Total RAM:{RESET} {gradient_text(f'{total_ram} GB')}")
    print(f" {W1}│{RESET}   {GRAY}Available RAM:{RESET} {gradient_text(f'{avail_ram} GB')}")

    print(f" {W1}│{RESET}")
    print(f" {W1}╰─{RESET} {gradient_text('REVERSE ENGINEERING MANUAL')}")
    print()

    # Reverse Engineering Manual
    manual = [
        "1. Debugging Tools:",
        "   - Windows: x64dbg, WinDbg, IDA Pro, Ghidra",
        "   - Linux: GDB, Radare2, ltrace, strace",
        "   - macOS: LLDB, Hopper, Ghidra",
        "",
        "2. Disassemblers:",
        "   - Ghidra (free, by NSA)",
        "   - IDA Pro (commercial, advanced)",
        "   - Radare2 (open-source, command-line)",
        "",
        "3. Common Techniques:",
        "   - Static analysis: read assembly, identify functions",
        "   - Dynamic analysis: run in debugger, set breakpoints",
        "   - Patching: modify binary to change behavior",
        "   - Hooking: intercept API calls (e.g., using Detours, Frida)",
        "",
        "4. Useful Commands (Linux):",
        "   - strace -p PID   (trace syscalls)",
        "   - ltrace -p PID   (trace library calls)",
        "   - objdump -d binary   (disassemble)",
        "   - strings binary   (extract strings)",
        "",
        "5. Windows Specific:",
        "   - Process Explorer, Process Monitor",
        "   - API Monitor for Windows API tracing",
        "   - .NET: dnSpy, ILSpy",
        "",
        "6. Anti-debugging Tricks:",
        "   - IsDebuggerPresent() (Windows)",
        "   - ptrace() check (Linux)",
        "   - Timing checks",
        "   - Obfuscation, packing, encryption",
        "",
        "7. Useful Resources:",
        "   - https://www.ghidra-sre.org/",
        "   - https://rada.re/n/ (Radare2)",
        "   - https://frida.re/ (dynamic instrumentation)",
        "   - https://github.com/NationalSecurityAgency/ghidra",
        "",
        "8. Practice:",
        "   - CrackMe challenges (e.g., from crackmes.one)",
        "   - Reverse engineering games, malware analysis",
        "   - CTF competitions (pwn, rev categories)"
    ]

    for line_text in manual:
        print(f" {GRAY}│{RESET} {gradient_text(line_text)}")

    print()
    print(f"{DARK}" + "─" * 106 + f"{RESET}")
    print(f"{W1}[+]{RESET} Analysis finished.")


FUNCTIONS = {
    "1": fn_01_veyon,
    "2": fn_02_wallpapers,
    "3": fn_03_porthack,
    "4": fn_04_misc,
    "5": fn_05_screamer,
    "6": fn_06_noise,
    "7": fn_07_butterfly,
    "8": fn_08_errors,
    "9": fn_09_cpp,
    "10": fn_10_lua,
    "11": fn_11_python,
    "12": fn_12_all_nets,
    "13": fn_13_how_to_use,
    "14": fn_14_py_syntax,
    "15": fn_15_lua_helper,
    "16": fn_16_reverse_eng
}


def render_ui():
    global _first_run

    clear_console()
    print_header(animated=_first_run)
    print()

    col1 = [
        "[1] Veyon",
        "[2] Wallpapers",
        "[3] Porthack",
        "[4] UAC"
    ]

    col2 = [
        "[5] TungTung website",
        "[6] TungTung Turtle",
        "[7] Users",
        "[8] TungTung Errors"
    ]

    col3 = [
        "[9] C++",
        "[10] Lua",
        "[11] Vuln. scan",
        "[12] All NETS/"
    ]

    col4 = [
        "[13] How to use",
        "[14] Py syntax",
        "[15] Lua helper",
        "[16] Reverse eng."
    ]

    WIDTH = 22
    SEP = f" {DARK}│{RESET}  "
    BORDER = f"{DARK}" + "═" * 106 + f"{RESET}"

    h1 = gradient_text(f"{BOLD}{'═══ BYPASSES ═══':<{WIDTH}}")
    h2 = gradient_text(f"{BOLD}{'═══ TOOLS ═══':<{WIDTH}}")
    h3 = gradient_text(f"{BOLD}{'═══ NETWORK ═══':<{WIDTH}}")
    h4 = gradient_text(f"{BOLD}{'═══ MANUALS ═══':<{WIDTH}}")

    header_line = f"  {h1}{SEP}{h2}{SEP}{h3}{SEP}{h4}"

    if _first_run:
        print(header_line, flush=True)
        time.sleep(0.07)
        print(BORDER, flush=True)
        time.sleep(0.07)
    else:
        print(header_line)
        print(BORDER)

    # Строки меню
    for i in range(4):
        c1 = gradient_text(f"{col1[i]:<{WIDTH}}")
        c2 = gradient_text(f"{col2[i]:<{WIDTH}}")
        c3 = gradient_text(f"{col3[i]:<{WIDTH}}")
        c4 = gradient_text(f"{col4[i]:<{WIDTH}}")
        line = f"  {c1}{SEP}{c2}{SEP}{c3}{SEP}{c4}"

        if _first_run:
            print(line, flush=True)
            time.sleep(0.05)  # задержка между строками меню
        else:
            print(line)

    if _first_run:
        time.sleep(0.07)
        print(BORDER, flush=True)
        _first_run = False
    else:
        print(BORDER)


def main():
    render_ui()

    while True:
        try:
            choice = input(
                f"\n{W1}[TungTungHook]"
                f"{W2} Choose tool "
                f"(Or 'q' for quit): {RESET}"
            ).strip()

            if choice.lower() == "q":
                clear_console()
                print(
                    gradient_text(
                        "TungTungHook closed."
                    )
                )
                break

            function = FUNCTIONS.get(choice)

            if function is None:
                print(
                    f"{W3}[!]{RESET} "
                    f"{gradient_text('Unknown function')}"
                )
                time.sleep(1)
                continue

            clear_console()
            print_header()
            print()

            function()

            input(
                f"\n{W3}[ENTER]{RESET} "
                f"Return to menu..."
            )

            render_ui()

        except KeyboardInterrupt:
            print()
            break


if __name__ == "__main__":
    main()