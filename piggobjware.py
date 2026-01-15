import time
import json
import struct
import psutil
import ctypes
import win32gui
import win32con
import traceback
import win32process
import requests
import tkinter as tk
import pygame
import pygame
import win32api
import win32con
import win32gui
import threading

import math

from ctypes import wintypes

OFFSETS_URL = "https://robloxoffsets.com/offsets.json"
resp = requests.get(OFFSETS_URL)
OFFSETS = resp.json()

# --- INITIALIZATION CHECKS ---
try:
    libc = ctypes.CDLL("ntdll.dll")
    libc.NtSetTimerResolution(5000, 1, ctypes.byref(ctypes.c_ulong()))
except:
    print("Could not set high-precision timer.")



class Piggobjware:



    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

# Part B: Add this new function inside the class
def on_closing(self):
    self.is_running = False
    pygame.quit()
    self.root.destroy()
    import os
    os._exit(0)
    
    def __init__(self, mem):
        self.mem = mem
        self.root = tk.Tk()
        self.root.title("Piggobjware External")
        self.root.geometry("450x550")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#121216") # Deep dark purple-grey
        
        # --- Pixel/8-Bit Style Config ---
        self.font_main = ("Courier", 12, "bold")
        self.font_pixel = ("Consolas", 10)
        self.accent_color = "#9d74ff" # Purple accent from your image
        
        # --- Variables ---
        self.aimbot_enabled = tk.BooleanVar(value=True)
        self.fov_radius = tk.IntVar(value=150)
        self.smoothness = tk.DoubleVar(value=0.20)
        self.target_part = tk.StringVar(value="Head")
        self.is_running = True
        self.target_cache = None

        self.setup_ui()
        
        # Start Threads
        threading.Thread(target=self.logic_engine, daemon=True).start()
        threading.Thread(target=self.memory_worker, daemon=True).start()
        
        self.root.mainloop()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1a20", height=40)
        header.pack(fill="x")
        tk.Label(header, text="PIGGOBJWARE | AIM", bg="#1a1a20", fg="white", font=self.font_main).pack(side="left", padx=10)
        tk.Label(header, text="Visual  Config  Menu", bg="#1a1a20", fg="#888", font=self.font_pixel).pack(side="right", padx=10)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#121216", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Main Settings Section (Top Left)
        settings_box = tk.LabelFrame(main_frame, text=" Main Settings ", bg="#121216", fg=self.accent_color, font=self.font_pixel, bd=1, relief="solid")
        settings_box.place(x=0, y=0, width=200, height=180)

        tk.Checkbutton(settings_box, text="Aimbot", variable=self.aimbot_enabled, bg="#121216", fg="white", 
                       selectcolor="#1a1a20", activebackground="#121216", font=self.font_pixel).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(settings_box, text=f"Fov Size", bg="#121216", fg="#aaa", font=self.font_pixel).pack(anchor="w", padx=10)
        tk.Scale(settings_box, from_=10, to=600, variable=self.fov_radius, orient="horizontal", 
                 bg="#121216", fg="white", highlightthickness=0, troughcolor="#1a1a20").pack(fill="x", padx=10)

        # Mouse Settings Section (Bottom)
        mouse_box = tk.LabelFrame(main_frame, text=" Mouse Settings ", bg="#121216", fg=self.accent_color, font=self.font_pixel, bd=1, relief="solid")
        mouse_box.place(x=0, y=200, width=410, height=150)

        tk.Label(mouse_box, text="Smoothness Amount", bg="#121216", fg="#aaa", font=self.font_pixel).pack(anchor="w", padx=10, pady=(10,0))
        tk.Scale(mouse_box, from_=0.01, to=1.0, resolution=0.01, variable=self.smoothness, orient="horizontal", 
                 bg="#121216", fg="white", highlightthickness=0, troughcolor="#1a1a20").pack(fill="x", padx=10)

        # Status Bar
        status_bar = tk.Frame(self.root, bg="#1a1a20", height=25)
        status_bar.pack(fill="x", side="bottom")
        tk.Label(status_bar, text="[RUNNING] MOUSE 5 TO LOCK", bg="#1a1a20", fg=self.accent_color, font=self.font_pixel).pack(side="left", padx=10)

    def memory_worker(self):
        sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        center = (sw // 2, sh // 2)
        while self.is_running:
            try:
                # Scans the 26+ players in your lobby
                players = self.mem.get_player_coordinates() 
                best_t = None
                min_d = float('inf')
                
                for p in players:
                    # Logic targets 'head_pos' as requested
                    screen_pos = self.mem.world_to_screen(p['head_pos'])
                    if screen_pos.x != -1:
                        dist = math.sqrt((screen_pos.x - center[0])**2 + (screen_pos.y - center[1])**2)
                        if dist < min_d and dist < self.fov_radius.get():
                            min_d = dist
                            best_t = screen_pos
                self.target_cache = best_t
            except: pass
            time.sleep(0.01)

    def logic_engine(self):
        pygame.init()
        sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        center = (sw // 2, sh // 2)
        
        # Transparent Overlay for FOV
        screen = pygame.display.set_mode((sw, sh), pygame.NOFRAME)
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 255), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 0x0001 | 0x0002)

        rem_x, rem_y = 0.0, 0.0
        while self.is_running:
            for event in pygame.event.get(): pass
            screen.fill((255, 0, 255))
            
            # Draw FOV Circle (Purple accent color)
            pygame.draw.circle(screen, (157, 116, 255), center, self.fov_radius.get(), 1)
            
            if self.aimbot_enabled.get() and self.target_cache and win32api.GetAsyncKeyState(0x06) < 0:
                dx, dy = self.target_cache.x - center[0], self.target_cache.y - center[1]
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist > 0:
                    # Exponential Smoothing Logic
                    speed = min((dist ** 1.1) * (self.smoothness.get() / 20), 45.0)
                    move_x = (dx / dist) * speed + rem_x
                    move_y = (dy / dist) * speed + rem_y
                    
                    ix, iy = int(move_x), int(move_y)
                    rem_x, rem_y = move_x - ix, move_y - iy
                    
                    if ix != 0 or iy != 0:
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, ix, iy, 0, 0)
            else: rem_x = rem_y = 0.0

            pygame.display.update()
            time.sleep(0.001)
            


def move_mouse_to_target(target_x, target_y, screen_width, screen_height, smoothing=0.3):
    # Calculate screen center
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Calculate the relative distance to the target
    rel_x = int(target_x - center_x)
    rel_y = int(target_y - center_y)

    # Apply smoothing (multiply distance by a factor < 1)
    # This moves the mouse partially toward the target each frame
    move_x = int(rel_x * smoothing)
    move_y = int(rel_y * smoothing)

    # Send relative movement to Windows
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, move_x, move_y, 0, 0)



class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("th32Usage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(wintypes.DWORD)),
        ("th32ModuleID", wintypes.DWORD),
        ("th32Threads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260)
    ]

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("th32ModuleID", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("GlblcntUsage", wintypes.DWORD),
        ("ProccntUsage", wintypes.DWORD),
        ("modBaseAddr", ctypes.POINTER(wintypes.BYTE)),
        ("modBaseSize", wintypes.DWORD),
        ("hModule", wintypes.HMODULE),
        ("szModule", ctypes.c_char * 256),
        ("szExePath", ctypes.c_char * 260)
    ]

class vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class robloxmemory:
    def __init__(self):
        if not self.find_roblox_process():
            raise Exception("failed to find roblox process.")
        self.initialize_game_data()

    def find_roblox_process(self):
        hwnd, pid = self.find_window_by_exe("RobloxPlayerBeta.exe")
        if pid:
            self.hwnd = hwnd
            self.process_id = pid
        else:
            pid = self.get_process_id_by_psutil("RobloxPlayerBeta.exe")
            if not pid:
                return False
            self.process_id = pid
            hwnd, _ = self.find_window_by_exe("RobloxPlayerBeta.exe")
            self.hwnd = hwnd if hwnd else None
        self.process_handle = ctypes.windll.kernel32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self.process_id)
        if not self.process_handle:
            return False
        self.base_address = self.get_module_address("RobloxPlayerBeta.exe")
        if not self.base_address:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            return False
        return True

    def find_window_by_exe(self, exe_name):
        matches = []
        def enum_proc(hwnd, _):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    p = psutil.Process(pid)
                    pname = (p.name() or "").lower()
                    target = exe_name.lower()
                    target_noexe = target[:-4] if target.endswith(".exe") else target
                    if pname == target or pname == target_noexe:
                        matches.append((hwnd, pid))
                except Exception:
                    pass
                return True
            except Exception:
                return True
        try:
            win32gui.EnumWindows(enum_proc, None)
        except Exception:
            pass
        if matches:
            for hwnd, pid in matches:
                title = win32gui.GetWindowText(hwnd)
                if title:
                    return hwnd, pid
            return matches[0]
        return None, None

    def get_process_id_by_psutil(self, process_name):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        return proc.info['pid']
                except Exception:
                    continue
            return None
        except Exception:
            return None

    def get_module_address(self, module_name):
        if not getattr(self, 'process_handle', None):
            return None
        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x8 | 0x10, self.process_id)
        if snapshot == -1:
            return None
        module_entry = MODULEENTRY32()
        module_entry.dwSize = ctypes.sizeof(MODULEENTRY32)
        if ctypes.windll.kernel32.Module32First(snapshot, ctypes.byref(module_entry)):
            while True:
                try:
                    name = module_entry.szModule.decode().lower()
                except Exception:
                    name = ""
                if module_name.lower() == name:
                    ctypes.windll.kernel32.CloseHandle(snapshot)
                    return ctypes.addressof(module_entry.modBaseAddr.contents)
                if not ctypes.windll.kernel32.Module32Next(snapshot, ctypes.byref(module_entry)):
                    break
        ctypes.windll.kernel32.CloseHandle(snapshot)
        return None

    def read_memory(self, address, size):
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        result = ctypes.windll.kernel32.ReadProcessMemory(self.process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read))
        if result and bytes_read.value > 0:
            return buffer.raw[:bytes_read.value]
        return None

    def read_ptr(self, address):
        data = self.read_memory(address, 8)
        if data:
            return int.from_bytes(data, byteorder='little')
        return None

    def read_int(self, address):
        data = self.read_memory(address, 4)
        if data:
            return int.from_bytes(data, byteorder='little', signed=True)
        return None

    def read_int64(self, address):
        data = self.read_memory(address, 8)
        if data:
            return struct.unpack('q', data)[0]
        return None

    def read_float(self, address):
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('f', data)[0]
        return None

    def read_string(self, address):
        if not address:
            return ""
        str_length = self.read_int(address + 0x18)
        if not str_length or str_length <= 0 or str_length > 1000:
            return ""
        if str_length >= 16:
            address = self.read_ptr(address)
            if not address:
                return ""
        result = ""
        offset = 0
        while offset < str_length:
            char_data = self.read_memory(address + offset, 1)
            if not char_data:
                break
            char_val = char_data[0]
            if char_val == 0:
                break
            result += chr(char_val)
            offset += 1
        return result

    def initialize_game_data(self):
        try:
            fake_data_model = self.read_ptr(self.base_address + int(OFFSETS["FakeDataModelPointer"], 16))
            if not fake_data_model or fake_data_model == 0xFFFFFFFF:
                return
            data_model_pointer = self.read_ptr(fake_data_model + int(OFFSETS["FakeDataModelToDataModel"], 16))
            if not data_model_pointer or data_model_pointer == 0xFFFFFFFF:
                return
            retry_count = 0
            data_model_name = ""
            while retry_count < 30:
                name_ptr = self.read_ptr(data_model_pointer + int(OFFSETS["Name"], 16)) if data_model_pointer else None
                data_model_name = self.read_string(name_ptr) if name_ptr else ""
                if data_model_name == "Ugc":
                    break
                time.sleep(1)
                retry_count += 1
                fake_data_model = self.read_ptr(self.base_address + int(OFFSETS["FakeDataModelPointer"], 16))
                if fake_data_model:
                    data_model_pointer = self.read_ptr(fake_data_model + int(OFFSETS["FakeDataModelToDataModel"], 16))
            if data_model_name != "Ugc":
                return
            self.data_model = data_model_pointer
            self.visual_engine = self.read_ptr(self.base_address + int(OFFSETS["VisualEnginePointer"], 16))
            if not self.visual_engine or self.visual_engine == 0xFFFFFFFF:
                self.visual_engine = None
                return
            self.workspace = self.find_first_child_which_is_a(self.data_model, "Workspace") if self.data_model else None
            self.players = self.find_first_child_which_is_a(self.data_model, "Players") if self.data_model else None
            if self.workspace:
                self.camera = self.find_first_child_which_is_a(self.workspace, "Camera")
            else:
                self.camera = None
            if self.players:
                local_player_ptr = self.read_ptr(self.players + int(OFFSETS["LocalPlayer"], 16)) if self.players else None
                if local_player_ptr:
                    self.local_player = local_player_ptr
                else:
                    self.local_player = None
            else:
                self.local_player = None
        except Exception:
            pass

    def get_children(self, parent_address):
        children = []
        if not parent_address:
            return children
        children_ptr = self.read_ptr(parent_address + int(OFFSETS["Children"], 16))
        if not children_ptr:
            return children
        children_end = self.read_ptr(children_ptr + int(OFFSETS["ChildrenEnd"], 16))
        current_child = self.read_ptr(children_ptr)
        while current_child < children_end:
            child_ptr = self.read_ptr(current_child)
            if child_ptr:
                children.append(child_ptr)
            current_child += 0x10
        return children

    def get_instance_name(self, address):
        if not address:
            return ""
        name_ptr = self.read_ptr(address + int(OFFSETS["Name"], 16))
        return self.read_string(name_ptr) if name_ptr else ""

    def get_instance_class(self, address):
        if not address:
            return ""
        class_descriptor = self.read_ptr(address + int(OFFSETS["ClassDescriptor"], 16))
        if class_descriptor:
            class_name_ptr = self.read_ptr(class_descriptor + int(OFFSETS["ClassDescriptorToClassName"], 16))
            return self.read_string(class_name_ptr) if class_name_ptr else ""
        return ""

    def find_first_child_which_is_a(self, parent_address, class_name):
        children = self.get_children(parent_address)
        for child in children:
            if self.get_instance_class(child) == class_name:
                return child
        return None

    def find_first_child_by_name(self, parent_address, name):
        children = self.get_children(parent_address)
        for child in children:
            if self.get_instance_name(child) == name:
                return child
        return None

    def read_matrix4(self, address):
        data = self.read_memory(address, 64)
        if data:
            matrix = []
            for i in range(16):
                matrix.append(struct.unpack('f', data[i*4:(i+1)*4])[0])
            return matrix
        return None

    def get_team(self, player_ptr):
        if not player_ptr:
            return None
        team_ptr = self.read_ptr(player_ptr + int(OFFSETS.get("Team", "0x0"), 16))
        if not team_ptr:
            return None
        return team_ptr

    def get_player_coordinates(self):
        if not getattr(self, 'players', None) or not getattr(self, 'local_player', None):
            return []
        coordinates = []
        player_instances = self.get_children(self.players)
        for player_ptr in player_instances:
            if not player_ptr:
                continue
            if player_ptr == self.local_player:
                continue
            player_name = self.get_instance_name(player_ptr)
            if not player_name:
                continue
            character_ptr = self.read_ptr(player_ptr + int(OFFSETS["ModelInstance"], 16))
            if not character_ptr:
                continue
            if self.get_instance_class(character_ptr) != "Model":
                continue
            humanoid_root_part = self.find_first_child_by_name(character_ptr, "HumanoidRootPart")
            if not humanoid_root_part:
                continue
            if self.get_instance_class(humanoid_root_part) != "Part":
                continue
            primitive = self.read_ptr(humanoid_root_part + int(OFFSETS["Primitive"], 16))
            if not primitive:
                continue
            position_data = self.read_memory(primitive + int(OFFSETS["Position"], 16), 12)
            if not position_data:
                continue
            x, y, z = struct.unpack('fff', position_data)
            position = vec3(x, y, z)
            size_data = self.read_memory(primitive + int(OFFSETS["PartSize"], 16), 12)
            if size_data:
                sx, sy, sz = struct.unpack('fff', size_data)
                player_size = vec3(sx, sy, sz)
            else:
                player_size = vec3(2.0, 5.0, 1.0)
            head_part = self.find_first_child_by_name(character_ptr, "Head")
            head_pos = None
            if head_part:
                head_primitive = self.read_ptr(head_part + int(OFFSETS["Primitive"], 16))
                if head_primitive:
                    head_position_data = self.read_memory(head_primitive + int(OFFSETS["Position"], 16), 12)
                    if head_position_data:
                        hx, hy, hz = struct.unpack('fff', head_position_data)
                        head_pos = vec3(hx, hy, hz)
            if not head_pos:
                head_pos = vec3(position.x, position.y + player_size.y / 2 + 1.0, position.z)
            humanoid = self.find_first_child_which_is_a(character_ptr, "Humanoid")
            health = None
            max_health = None
            if humanoid:
                health_addr = humanoid + int(OFFSETS["Health"], 16)
                max_health_addr = humanoid + int(OFFSETS["MaxHealth"], 16)
                health = self.read_float(health_addr)
                max_health = self.read_float(max_health_addr)
            coordinates.append({
                "player_name": player_name,
                "root_pos": position,
                "head_pos": head_pos,
                "player_size": player_size,
                "player_ptr": player_ptr,
                "character_ptr": character_ptr,
                "humanoid_root_part_ptr": humanoid_root_part,
                "health": health,
                "max_health": max_health
            })
        return coordinates

    def get_window_viewport(self):
        if not getattr(self, 'hwnd', None):
            return vec2(1920, 1080)
        try:
            left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
            width = float(right - left)
            height = float(bottom - top)
            if width <= 0 or height <= 0:
                rect = win32gui.GetWindowRect(self.hwnd)
                width = float(rect[2] - rect[0])
                height = float(rect[3] - rect[1])
            return vec2(width, height)
        except Exception:
            return vec2(1920, 1080)

    def world_to_screen(self, pos):
        if not getattr(self, 'visual_engine', None):
            return vec2(-1, -1)
        try:
            view_matrix = self.read_matrix4(self.visual_engine + int(OFFSETS["viewmatrix"], 16))
            if not view_matrix:
                return vec2(-1, -1)
            qx = (pos.x * view_matrix[0]) + (pos.y * view_matrix[1]) + (pos.z * view_matrix[2]) + view_matrix[3]
            qy = (pos.x * view_matrix[4]) + (pos.y * view_matrix[5]) + (pos.z * view_matrix[6]) + view_matrix[7]
            qz = (pos.x * view_matrix[8]) + (pos.y * view_matrix[9]) + (pos.z * view_matrix[10]) + view_matrix[11]
            qw = (pos.x * view_matrix[12]) + (pos.y * view_matrix[13]) + (pos.z * view_matrix[14]) + view_matrix[15]
            if qw < 0.1:
                return vec2(-1, -1)
            ndc_x = qx / qw
            ndc_y = qy / qw
            viewport = self.get_window_viewport()
            width = viewport.x
            height = viewport.y
            x = (width / 2.0) * (1.0 + ndc_x)
            y = (height / 2.0) * (1.0 - ndc_y)
            if x < 0 or x > width or y < 0 or y > height:
                return vec2(-1, -1)
            return vec2(x, y)
        except Exception:
            return vec2(-1, -1)

    def get_place_id(self):
        if not getattr(self, 'data_model', None):
            return None
        try:
            place_id = self.read_int64(self.data_model + int(OFFSETS["PlaceId"], 16))
            return place_id if place_id else None
        except Exception:
            return None

    """
    def print_game_info(self):
        player_coords = self.get_player_coordinates()
        print(f"found {len(player_coords)} player instances [humanoids]")
        for p in player_coords:
            root_pos = p["root_pos"]
            health_info = f"health: {p['health']:.1f}/{p['max_health']:.1f}" if p['health'] is not None and p['max_health'] is not None else "health: Unknown"
            print(f"got pos : {p['player_name']}: ({root_pos.x:.2f}, {root_pos.y:.2f}, {root_pos.z:.2f}) | {health_info}")
    """


    def print_game_info(self):
        player_coords = self.get_player_coordinates()
        viewport = self.get_window_viewport() # Get resolution for context
        print(f"found {len(player_coords)} player instances [humanoids]")
        print(f"Current Viewport: {viewport.x}x{viewport.y}")
        print("-" * 30)

        for p in player_coords:
            root_pos = p["root_pos"]
            
            # --- ADDED: Convert World Position to Screen Position ---
            screen_pos = self.world_to_screen(root_pos)
            if screen_pos.x != -1:
                screen_info = f"Screen XY: ({screen_pos.x:.1f}, {screen_pos.y:.1f})"
            else:
                screen_info = "Screen XY: Off-Screen/Behind"
            # -------------------------------------------------------

            health_info = f"health: {p['health']:.1f}/{p['max_health']:.1f}" if p['health'] is not None and p['max_health'] is not None else "health: Unknown"
            
            # Updated print statement to include screen info
            print(f"Name: {p['player_name']}")
            print(f"  > World XYZ: ({root_pos.x:.2f}, {root_pos.y:.2f}, {root_pos.z:.2f})")
            print(f"  > {screen_info}")
            print(f"  > {health_info}")
            print("-" * 10)


# Force high-precision Windows timers
libc = ctypes.CDLL("ntdll.dll")
libc.NtSetTimerResolution(5000, 1, ctypes.byref(ctypes.c_ulong()))

# --- [PASTE YOUR robloxmemory CLASS HERE] ---

class Piggobjware:
    def __init__(self, mem):
        self.mem = mem
        self.root = tk.Tk()
        self.root.title("Piggobjware External")
        self.root.geometry("450x550")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#121216") # Deep dark purple-grey
        
        # --- Pixel/8-Bit Style Config ---
        self.font_main = ("Courier", 12, "bold")
        self.font_pixel = ("Consolas", 10)
        self.accent_color = "#9d74ff" # Purple accent from your image
        
        # --- Variables ---
        self.aimbot_enabled = tk.BooleanVar(value=True)
        self.fov_radius = tk.IntVar(value=150)
        self.smoothness = tk.DoubleVar(value=0.20)
        self.target_part = tk.StringVar(value="Head")
        self.is_running = True
        self.target_cache = None

        self.setup_ui()
        
        # Start Threads
        threading.Thread(target=self.logic_engine, daemon=True).start()
        threading.Thread(target=self.memory_worker, daemon=True).start()
        
        self.root.mainloop()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1a20", height=40)
        header.pack(fill="x")
        tk.Label(header, text="PIGGOBJWARE | AIM", bg="#1a1a20", fg="white", font=self.font_main).pack(side="left", padx=10)
        tk.Label(header, text="Visual  Config  Menu", bg="#1a1a20", fg="#888", font=self.font_pixel).pack(side="right", padx=10)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#121216", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Main Settings Section (Top Left)
        settings_box = tk.LabelFrame(main_frame, text=" Main Settings ", bg="#121216", fg=self.accent_color, font=self.font_pixel, bd=1, relief="solid")
        settings_box.place(x=0, y=0, width=200, height=180)

        tk.Checkbutton(settings_box, text="Aimbot", variable=self.aimbot_enabled, bg="#121216", fg="white", 
                       selectcolor="#1a1a20", activebackground="#121216", font=self.font_pixel).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(settings_box, text=f"Fov Size", bg="#121216", fg="#aaa", font=self.font_pixel).pack(anchor="w", padx=10)
        tk.Scale(settings_box, from_=10, to=600, variable=self.fov_radius, orient="horizontal", 
                 bg="#121216", fg="white", highlightthickness=0, troughcolor="#1a1a20").pack(fill="x", padx=10)

        # Mouse Settings Section (Bottom)
        mouse_box = tk.LabelFrame(main_frame, text=" Mouse Settings ", bg="#121216", fg=self.accent_color, font=self.font_pixel, bd=1, relief="solid")
        mouse_box.place(x=0, y=200, width=410, height=150)

        tk.Label(mouse_box, text="Smoothness Amount", bg="#121216", fg="#aaa", font=self.font_pixel).pack(anchor="w", padx=10, pady=(10,0))
        tk.Scale(mouse_box, from_=0.01, to=1.0, resolution=0.01, variable=self.smoothness, orient="horizontal", 
                 bg="#121216", fg="white", highlightthickness=0, troughcolor="#1a1a20").pack(fill="x", padx=10)

        # Status Bar
        status_bar = tk.Frame(self.root, bg="#1a1a20", height=25)
        status_bar.pack(fill="x", side="bottom")
        tk.Label(status_bar, text="[RUNNING] MOUSE 5 TO LOCK", bg="#1a1a20", fg=self.accent_color, font=self.font_pixel).pack(side="left", padx=10)

    def memory_worker(self):
        sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        center = (sw // 2, sh // 2)
        while self.is_running:
            try:
                # Scans the 26+ players in your lobby
                players = self.mem.get_player_coordinates() 
                best_t = None
                min_d = float('inf')
                
                for p in players:
                    # Logic targets 'head_pos' as requested
                    screen_pos = self.mem.world_to_screen(p['head_pos'])
                    if screen_pos.x != -1:
                        dist = math.sqrt((screen_pos.x - center[0])**2 + (screen_pos.y - center[1])**2)
                        if dist < min_d and dist < self.fov_radius.get():
                            min_d = dist
                            best_t = screen_pos
                self.target_cache = best_t
            except: pass
            time.sleep(0.01)

    def logic_engine(self):
        pygame.init()
        sw, sh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        center = (sw // 2, sh // 2)
        
        # Transparent Overlay for FOV
        screen = pygame.display.set_mode((sw, sh), pygame.NOFRAME)
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 255), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 0x0001 | 0x0002)

        rem_x, rem_y = 0.0, 0.0
        while self.is_running:
            for event in pygame.event.get(): pass
            screen.fill((255, 0, 255))
            
            # Draw FOV Circle (Purple accent color)
            pygame.draw.circle(screen, (157, 116, 255), center, self.fov_radius.get(), 1)
            
            if self.aimbot_enabled.get() and self.target_cache and win32api.GetAsyncKeyState(0x06) < 0:
                dx, dy = self.target_cache.x - center[0], self.target_cache.y - center[1]
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist > 0:
                    # Exponential Smoothing Logic
                    speed = min((dist ** 1.1) * (self.smoothness.get() / 20), 45.0)
                    move_x = (dx / dist) * speed + rem_x
                    move_y = (dy / dist) * speed + rem_y
                    
                    ix, iy = int(move_x), int(move_y)
                    rem_x, rem_y = move_x - ix, move_y - iy
                    
                    if ix != 0 or iy != 0:
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, ix, iy, 0, 0)
            else: rem_x = rem_y = 0.0

            pygame.display.update()
            time.sleep(0.001)

# --- Entry ---
if __name__ == "__main__":
    mem = robloxmemory() # Initialize your class
    Piggobjware(mem)
    pass