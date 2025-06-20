from tkinter import ttk
import tkinter as tk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess

def get_gpu_info():
    try:
        result = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=name,utilization.gpu,temperature.gpu', '--format=csv,noheader,nounits'],
            encoding='utf-8'
        )
        name, usage, temp = result.strip().split(', ')
        return {
            'name': name,
            'usage': float(usage),
            'temp': temp
        }
    except Exception:
        return None

GPU_AVAILABLE = get_gpu_info() is not None

class TaskManagerGraph(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#191919")
        self.title("Task Manager Layout")
        self.geometry("1300x750")
        self.attributes("-alpha", 0.9)

        INFOBOX_WIDTH = 185
        INFOBOX_HEIGHT = 210
        
        
        # CPU infokast
        self.cpu_info_frame = tk.Frame(self, width=INFOBOX_WIDTH, height=INFOBOX_HEIGHT, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.cpu_info_frame.place(x=10, y=10)
        self.cpu_info_frame.pack_propagate(0)

        tk.Label(self.cpu_info_frame, text="CPU", bg="#202020", fg="#EEEEEE", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

        füüsilised = psutil.cpu_count(logical=False)
        loogilised = psutil.cpu_count(logical=True)
        taktsagedus = psutil.cpu_freq().current

        tk.Label(self.cpu_info_frame, fg="#EEEEEE",
                text=f"{füüsilised} füüsilist tuuma\n{loogilised} loogilist lõime\n{taktsagedus:.0f} MHz",
                bg="#202020").pack(anchor="w", padx=10)

        
        # GPU infokast
        self.gpu_info_frame = tk.Frame(self, width=INFOBOX_WIDTH, height=INFOBOX_HEIGHT, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.gpu_info_frame.place(x=10, y=220)
        self.gpu_info_frame.pack_propagate(0)
        tk.Label(self.gpu_info_frame, text="GPU", bg="#202020", fg="#EEEEEE", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        if GPU_AVAILABLE:
            gpu = get_gpu_info()
            gpu_name = gpu['name'] if gpu else "Pole tuvastatud"
        else:
            gpu_name = "Pole saadaval"
        tk.Label(self.gpu_info_frame, text=gpu_name, fg="#EEEEEE", bg="#202020").pack(anchor="w", padx=10)
        
        
        # RAM infokast
        self.ram_info_frame = tk.Frame(self, width=INFOBOX_WIDTH, height=INFOBOX_HEIGHT, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.ram_info_frame.place(x=10, y=430)
        self.ram_info_frame.pack_propagate(0)
        ram = psutil.virtual_memory()
        ram_total = ram.total // (1024**2)
        tk.Label(self.ram_info_frame, text="RAM", bg="#202020", fg="#EEEEEE", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        tk.Label(self.ram_info_frame, text=f"{ram_total} MB", fg="#EEEEEE", bg="#202020").pack(anchor="w", padx=10)


        # disk infokast
        self.disk_info_frame = tk.Frame(self, width=INFOBOX_WIDTH, height=INFOBOX_HEIGHT, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.disk_info_frame.place(x=10, y=640)
        self.disk_info_frame.pack_propagate(0)
        tk.Label(self.disk_info_frame, text="KÕVAKETTAD", bg="#202020", fg="#EEEEEE", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        self.disk_label = tk.Label(self.disk_info_frame, fg="#EEEEEE", bg="#202020", justify="left")
        self.disk_label.pack(anchor="w", padx=0)



        self.graph_frame_width = 550
        self.graph_frame_height = 200
        # CPU kast
        self.cpu_frame = tk.Frame(self, width=self.graph_frame_width, height=self.graph_frame_height, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.cpu_frame.place(x=200, y=10)
        tk.Label(self.cpu_frame, text="CPU", bg="#202020", fg="#EEEEEE", font=("Arial", 12, "bold")).pack(anchor="nw", padx=10, pady=5)
        self.cpu_info = tk.Label(self.cpu_frame, text="", bg="#202020", fg="#EEEEEE", font=("Arial", 10))
        self.cpu_info.pack(anchor="nw", padx=10, pady=(0, 5))

        self.fig_cpu, self.ax_cpu = plt.subplots(figsize=(5, 1.2))
        self.fig_cpu.patch.set_facecolor("#202020")
        self.ax_cpu.tick_params(axis='both', colors='#EEEEEE')
        self.ax_cpu.set_xlim(0, 50)
        self.ax_cpu.set_ylim(0, 100)
        self.ax_cpu.set_title("CPU Usage (%)", color="#EEEEEE")
        self.ax_cpu.set_facecolor((0, 0, 0, 0.2))
        self.x_data = list(range(50))
        self.y_cpu = [0] * 50
        self.line_cpu, = self.ax_cpu.plot(self.x_data, self.y_cpu, "#A1A1A1")
        self.fill_cpu = self.ax_cpu.fill_between(self.x_data, self.y_cpu, color='#A1A1A1', alpha=0.3)
        self.fig_cpu.tight_layout()
        self.canvas_cpu = FigureCanvasTkAgg(self.fig_cpu, master=self.cpu_frame)
        self.canvas_cpu.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))


        # GPU kast
        self.gpu_frame = tk.Frame(self, width=self.graph_frame_width, height=self.graph_frame_height, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.gpu_frame.place(x=200, y=20 + self.graph_frame_height)
        tk.Label(self.gpu_frame, text="GPU", bg="#202020", fg="#EEEEEE", font=("Arial", 12, "bold")).pack(anchor="nw", padx=10, pady=5)
        self.gpu_info = tk.Label(self.gpu_frame, text="", bg="#202020", fg="#EEEEEE", font=("Arial", 10))
        self.gpu_info.pack(anchor="nw", padx=10, pady=(0, 5))

        self.fig_gpu, self.ax_gpu = plt.subplots(figsize=(5, 1.2))
        self.fig_gpu.patch.set_facecolor("#202020")
        self.ax_gpu.tick_params(axis='both', colors='#EEEEEE')
        self.ax_gpu.set_xlim(0, 50)
        self.ax_gpu.set_ylim(0, 100)
        self.ax_gpu.set_title("GPU Usage (%)", color="#EEEEEE")
        self.ax_gpu.set_facecolor((0, 0, 0, 0.2))
        self.y_gpu = [0] * 50
        self.line_gpu, = self.ax_gpu.plot(self.x_data, self.y_gpu, "#D695BD")
        self.fill_gpu = self.ax_gpu.fill_between(self.x_data, self.y_gpu, color="#D695BD", alpha=0.3)
        self.fig_gpu.tight_layout()
        self.canvas_gpu = FigureCanvasTkAgg(self.fig_gpu, master=self.gpu_frame)
        self.canvas_gpu.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))


        # RAM kast
        self.ram_frame = tk.Frame(self, width=self.graph_frame_width, height=self.graph_frame_height, bg="#202020", highlightbackground="black", highlightthickness=1)
        self.ram_frame.place(x=200, y=30 + 2 * self.graph_frame_height)
        tk.Label(self.ram_frame, text="RAM", bg="#202020", fg="#EEEEEE", font=("Arial", 12, "bold")).pack(anchor="nw", padx=10, pady=5)
        self.ram_info = tk.Label(self.ram_frame, text="", bg="#202020", fg="#EEEEEE", font=("Arial", 10))
        self.ram_info.pack(anchor="nw", padx=10, pady=(0, 5))

        self.fig_ram, self.ax_ram = plt.subplots(figsize=(5, 1.4))
        self.fig_ram.patch.set_facecolor("#202020")
        self.ax_ram.tick_params(axis='both', colors='#EEEEEE')
        self.ax_ram.set_xlim(0, 50)
        self.ax_ram.set_ylim(0, 100)
        self.ax_ram.set_title("RAM Usage (%)", color="#EEEEEE")
        self.ax_ram.set_xlabel("Time", color="#EEEEEE")
        self.ax_ram.set_facecolor((0, 0, 0, 0.2))
        self.y_ram = [0] * 50
        self.line_ram, = self.ax_ram.plot(self.x_data, self.y_ram, "#2D8F9C")
        self.fill_ram = self.ax_ram.fill_between(self.x_data, self.y_ram, color='#2D8F9C', alpha=0.3)
        self.fig_ram.tight_layout()
        self.canvas_ram = FigureCanvasTkAgg(self.fig_ram, master=self.ram_frame)
        self.canvas_ram.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))


        #kõvakettad kast
        self.frame_parem = tk.Frame(self, width=560, height=300, bg="#202020")
        self.frame_parem.place(x=200, y=30 + 3.05 * self.graph_frame_height)

        self.labelid = []
        self.progressid = []
        self.partitsioonid = psutil.disk_partitions()
        for part in self.partitsioonid:
            lbl = tk.Label(self.frame_parem, text=f"{part.device} ({part.mountpoint}): 0%", bg="#202020", fg="#EEEEEE", font=("Arial", 10))
            lbl.pack(anchor="w")
            pb = ttk.Progressbar(self.frame_parem, orient="horizontal", length=522, mode="determinate", maximum=100, style="green.Horizontal.TProgressbar")
            pb.pack(anchor="w", pady=(0, 10))
            self.labelid.append(lbl)
            self.progressid.append(pb)
            style = ttk.Style()
            style.theme_use('default')
            style.configure("green.Horizontal.TProgressbar", troughcolor="#161616", background="#C783FF")

        self.uuenda_ketaste_info()
        
        
        # Parem ruut: protsesside nimekiri
        self.right_frame = tk.Frame(self, width=300, height=700, bg="#202020")
        self.right_frame.place(x=780, y=10)
        tk.Label(self.right_frame, text="Protsessid", bg="#202020", fg="#EEEEEE", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=2)
        self.process_listbox = tk.Listbox(self.right_frame, width=40, height=40, bg="#202020", fg="#EEEEEE", bd=0, highlightthickness=0, font=("Arial", 10))
        self.process_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.update_graphs()
        self.update_process_list()




    def uuenda_ketaste_info(self):
        info_text = ""
        for i, part in enumerate(self.partitsioonid):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                protsent = usage.percent
                vabaks = usage.free // (1024 ** 3)
                kogus = usage.total // (1024 ** 3)
                info_text += f"{part.device}: {vabaks} GB vaba / {kogus} GB ({protsent:.1f}%)\n"
                self.labelid[i].config(text=f"{part.device} ({part.mountpoint}): {protsent}%")
                self.progressid[i]["value"] = protsent
            except PermissionError:
                self.labelid[i].config(text=f"{part.device} ({part.mountpoint}): pole ligipääsu")
                self.progressid[i]["value"] = 0
        self.disk_label.config(text=info_text)
        self.after(2000, self.uuenda_ketaste_info)

    def update_graphs(self):
        
        # cPU        
        cpu_usage = psutil.cpu_percent()
        self.y_cpu.append(cpu_usage)
        self.y_cpu.pop(0)
        self.line_cpu.set_ydata(self.y_cpu)
        self.fill_cpu.remove()
        self.fill_cpu = self.ax_cpu.fill_between(self.x_data, self.y_cpu, color='#A1A1A1', alpha=0.3)
        self.canvas_cpu.draw()
        self.cpu_info.config(text=f"Kasutus: {cpu_usage:.1f}%\nTuumasid: {psutil.cpu_count(logical=True)}")


        # gPU
        gpu_info = get_gpu_info() if GPU_AVAILABLE else None
        if gpu_info:
            gpu_load = gpu_info['usage']
            gpu_name = gpu_info['name']
            gpu_temp = gpu_info['temp']
        else:
            gpu_load = 0
            gpu_name = "Pole saadaval"
            gpu_temp = "-"

        self.y_gpu.append(gpu_load)
        self.y_gpu.pop(0)
        self.line_gpu.set_ydata(self.y_gpu)
        self.fill_gpu.remove()
        self.fill_gpu = self.ax_gpu.fill_between(self.x_data, self.y_gpu, color='#D695BD', alpha=0.3)
        self.canvas_gpu.draw()
        self.gpu_info.config(text=f"Nimi: {gpu_name}\nKasutus: {gpu_load:.1f}%\nTemp: {gpu_temp}°C")


        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used = ram.used // (1024**2)
        ram_total = ram.total // (1024**2)
        self.y_ram.append(ram_percent)
        self.y_ram.pop(0)
        self.line_ram.set_ydata(self.y_ram)
        self.fill_ram.remove()
        self.fill_ram = self.ax_ram.fill_between(self.x_data, self.y_ram, color='#2D8F9C', alpha=0.3)
        self.canvas_ram.draw()
        self.ram_info.config(text=f"Kasutus: {ram_percent:.1f}%\n{ram_used} / {ram_total} MB")

        self.after(1000, self.update_graphs)

    def update_process_list(self):
        self.process_listbox.delete(0, tk.END)
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
        for proc in processes[:30]:
            try:
                info = proc.info
                logical_cpus = psutil.cpu_count(logical=True)
                normalized_percent = info['cpu_percent'] / logical_cpus
                display = f"{info['pid']:>5} {info['name'][:20]:<20} {normalized_percent:>5.1f}%"
                self.process_listbox.insert(tk.END, display)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.after(2000, self.update_process_list)

if __name__ == "__main__":
    app = TaskManagerGraph()
    app.mainloop()
