import customtkinter as ctk
import threading
import time
import tkinter as tk

LIMITE_DEFAULT = 1_000_000

# ==============================
# B(n) usando recurrencia
# ==============================

def B(n: int) -> int:
    if n == 0:
        return 100
    if n == 1:
        return 300

    b_prev3 = 0  
    b_prev2 = 100   # B(0)
    b_prev1 = 300   # B(1)
    
    for i in range(2, n + 1):
        
        if(b_prev3 == 0):
            b_actual = 3 * b_prev1 - b_prev2
            b_prev3 = b_prev1
            b_prev1 = b_actual
        else:
            b_actual = 3 * b_prev1 - b_prev3
            b_prev3 = b_prev1
            b_prev1 = b_actual

    return b_prev1

# ==============================
# Muertes
# ==============================

def M(n: int) -> int:
    if n >= 2:
        return B(n - 2)
    return 0

# ==============================
# Población viva total
# ==============================

def P(n: int) -> int:
    if n == 0:
        return 100
    return B(n) + B(n - 1)

# ==============================
# Hora en que se supera el límite
# ==============================

def hora_limite(limite: int) -> int:
    n = 0
    while P(n) <= limite:
        n += 1
    return n

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG      = "#0a0e1a"
CARD    = "#111827"
ACCENT  = "#00e5ff"
GREEN   = "#10b981"
AMBER   = "#f59e0b"
RED     = "#ef4444"
PURPLE  = "#7c3aed"
TEXT    = "#e2e8f0"
SUBTEXT = "#64748b"
BORDER  = "#1e293b"

class AlertaPopup(ctk.CTkToplevel):

    def __init__(self, parent: ctk.CTk, hora: int, poblacion: int, limite: int):
        super().__init__(parent)
        self.title("⚠ Alerta Bacteriana")
        self.geometry("420x480")
        self.configure(fg_color="#0d1a0d")
        self.resizable(False, False)
        self.grab_set()
        self.lift()
        self.focus_force()

        parent.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width()  // 2 - 210
        py = parent.winfo_y() + parent.winfo_height() // 2 - 240
        self.geometry(f"420x480+{px}+{py}")

        self._build(hora, poblacion, limite)

    def _build(self, hora: int, poblacion: int, limite: int):
        ctk.CTkFrame(self, fg_color="#22c55e", height=6, corner_radius=0).pack(fill="x")

        canvas = tk.Canvas(self, width=200, height=200,
                           bg="#0d1a0d", highlightthickness=0)
        canvas.pack(pady=(18, 0))
        self._draw_bacteria(canvas)

        ctk.CTkLabel(self, text="¡ALERTA EN LA COLONIA!",
                     font=("Courier New", 17, "bold"),
                     text_color="#22c55e").pack(pady=(10, 2))

        ctk.CTkLabel(self,
                     text=f"Se han superado los {limite:,}\nbacterias en la colonia.",
                     font=("Courier New", 13), text_color=TEXT,
                     justify="center").pack(pady=(4, 2))

        detail = ctk.CTkFrame(self, fg_color="#1a2e1a", corner_radius=10)
        detail.pack(padx=30, pady=12, fill="x")
        ctk.CTkLabel(detail, text=f"🕐  Hora de superación:  {hora}",
                     font=("Courier New", 11), text_color=AMBER).pack(pady=(10, 2))
        ctk.CTkLabel(detail, text=f"🧫  Población total:     {poblacion:,}",
                     font=("Courier New", 11), text_color="#4ade80").pack(pady=(2, 10))

        ctk.CTkButton(self, text="Entendido ✓",
                      font=("Courier New", 12, "bold"),
                      fg_color="#16a34a", hover_color="#15803d",
                      width=160, command=self.destroy).pack(pady=(4, 20))

        ctk.CTkFrame(self, fg_color="#22c55e", height=6,
                     corner_radius=0).pack(fill="x", side="bottom")

    def _draw_bacteria(self, c: tk.Canvas):
        c.create_oval(38, 60, 162, 170, fill="#22c55e", outline="")

        c.create_oval(55, 65, 95, 90, fill="#4ade80", stipple="gray50")

        flagelos = [
            [(155,105),(170,85),(162,65),(172,48)],
            [(148,128),(168,122),(178,108),(172,90)],
            [(45,105),(28,88),(32,66),(20,50)],
            [(52,128),(32,126),(22,110),(28,92)],
            [(80,165),(74,182),(62,188),(52,178)],
            [(120,165),(126,182),(140,188),(150,178)],
        ]
        for pts in flagelos:
            c.create_line(*[x for p in pts for x in p],
                          smooth=True, fill="#16a34a", width=3)

        c.create_oval(72, 95, 96, 122, fill="white", outline="")
        c.create_oval(104, 95, 128, 122, fill="white", outline="")

        c.create_oval(77, 100, 92, 117, fill="#111", outline="")
        c.create_oval(109, 100, 124, 117, fill="#111", outline="")

        c.create_oval(86, 102, 92, 108, fill="white", outline="")
        c.create_oval(117, 102, 123, 108, fill="white", outline="")

        c.create_line(73, 91, 82, 85, 93, 90, smooth=True, fill="#15803d", width=3)
        c.create_line(107, 90, 118, 85, 127, 90, smooth=True, fill="#15803d", width=3)

        c.create_oval(86, 128, 114, 148, fill="#15803d", outline="")
        c.create_oval(90, 132, 110, 146, fill="#052e16", outline="")

        c.create_line(44, 108, 32, 88, 38, 70, smooth=True, fill="#22c55e", width=7)
        c.create_oval(32, 63, 46, 77, fill="#22c55e", outline="")

        c.create_line(156, 108, 168, 88, 162, 70, smooth=True, fill="#22c55e", width=7)
        c.create_oval(154, 63, 168, 77, fill="#22c55e", outline="")

        c.create_text(100, 48, text="!", font=("Courier New", 26, "bold"), fill="#facc15")


class BacteriaApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("🧫 Simulación Colonia Bacteriana")
        self.geometry("1100x720")
        self.configure(fg_color=BG)
        self.resizable(True, True)

        self._limite  = LIMITE_DEFAULT
        self._target  = hora_limite(self._limite)
        self._running = False
        self._hora    = 0
        self._thread  = None
        self._chart_data      = []
        self._alerta_mostrada = False

        self._build_ui()

    # ──────────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ──────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        self._build_input_panel()
        self._build_cards()
        self._build_progress_bar()
        self._build_main_area()
        self._build_controls()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=54)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        ctk.CTkLabel(hdr, text="⬡  COLONIA BACTERIANA  ⬡",
                     font=("Courier New", 20, "bold"),
                     text_color=ACCENT).pack(side="left", padx=22, pady=10)

        self._lbl_header_meta = ctk.CTkLabel(
            hdr, text=f"Límite: {self._limite:,}",
            font=("Courier New", 10), text_color=SUBTEXT)
        self._lbl_header_meta.pack(side="right", padx=22)

    def _build_input_panel(self):
        input_frame = ctk.CTkFrame(self, fg_color=CARD, corner_radius=10)
        input_frame.pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(input_frame,
                     text="🔬  Límite máximo de bacterias en la colonia:",
                     font=("Courier New", 11, "bold"),
                     text_color=TEXT).pack(side="left", padx=16, pady=12)

        self._entry_limite = ctk.CTkEntry(
            input_frame,
            width=180,
            font=("Courier New", 13, "bold"),
            fg_color="#0d1117",
            border_color=ACCENT,
            text_color=AMBER,
            justify="center",
            placeholder_text="1,000,000")
        self._entry_limite.insert(0, str(LIMITE_DEFAULT))
        self._entry_limite.pack(side="left", padx=10)

        ctk.CTkButton(
            input_frame,
            text="Aplicar",
            font=("Courier New", 11, "bold"),
            fg_color=PURPLE, hover_color="#6d28d9",
            width=100,
            command=self._aplicar_limite
        ).pack(side="left", padx=6)

        self._lbl_limite_info = ctk.CTkLabel(
            input_frame,
            text=f"✔  Límite establecido en {self._limite:,} bacterias",
            font=("Courier New", 10),
            text_color=GREEN)
        self._lbl_limite_info.pack(side="left", padx=16)

    def _build_cards(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 6))

        self._c_nuevas  = self._card(row, "NUEVAS ESTA HORA",  "100", AMBER)
        self._c_muertas = self._card(row, "MUERTES ESTA HORA", "0",   RED)
        self._c_total   = self._card(row, "TOTAL VIVAS",       "100", GREEN)

        for c in (self._c_nuevas, self._c_muertas, self._c_total):
            c.pack(side="left", fill="both", expand=True, padx=5)

    def _build_progress_bar(self):
        pf = ctk.CTkFrame(self, fg_color=CARD, corner_radius=10)
        pf.pack(fill="x", padx=14, pady=4)

        self._lbl_prog_title = ctk.CTkLabel(
            pf, text=f"Progreso hacia {self._limite:,}",
            font=("Courier New", 10), text_color=SUBTEXT)
        self._lbl_prog_title.pack(anchor="w", padx=14, pady=(8, 2))

        self._progress = ctk.CTkProgressBar(pf, height=16,
                                             progress_color=GREEN, fg_color=BORDER)
        self._progress.set(0)
        self._progress.pack(fill="x", padx=14, pady=(0, 4))

        self._lbl_prog = ctk.CTkLabel(pf, text=f"0 / {self._limite:,}  (0.0%)",
                                      font=("Courier New", 9), text_color=SUBTEXT)
        self._lbl_prog.pack(anchor="e", padx=14, pady=(0, 6))

    def _build_main_area(self):
        mid = ctk.CTkFrame(self, fg_color="transparent")
        mid.pack(fill="both", expand=True, padx=14, pady=4)

        cf = ctk.CTkFrame(mid, fg_color=CARD, corner_radius=10)
        cf.pack(side="left", fill="both", expand=True, padx=(0, 5))
        ctk.CTkLabel(cf, text="Historial  ( 🟢 vivas  🔴 muertas )",
                     font=("Courier New", 11, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=14, pady=(10, 2))

        self._canvas = tk.Canvas(cf, bg="#0d1117", highlightthickness=0)
        self._canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        lf = ctk.CTkFrame(mid, fg_color=CARD, corner_radius=10, width=380)
        lf.pack(side="right", fill="both")
        lf.pack_propagate(False)

        log_hdr = ctk.CTkFrame(lf, fg_color="#1e293b", corner_radius=6)
        log_hdr.pack(fill="x", padx=10, pady=(10, 2))
        ctk.CTkLabel(log_hdr,
                     text=f"{'HORA':^6}  {'NUEVAS':^14}  {'MUERTAS':^14}  {'TOTAL VIVAS':^14}",
                     font=("Courier New", 10, "bold"),
                     text_color=ACCENT).pack(padx=8, pady=6)

        self._log = ctk.CTkTextbox(lf, font=("Courier New", 10),
                                   fg_color="#0d1117", text_color=TEXT,
                                   wrap="none", state="disabled")
        self._log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_controls(self):
        ctrl = ctk.CTkFrame(self, fg_color=CARD, corner_radius=10)
        ctrl.pack(fill="x", padx=14, pady=(4, 12))

        ctk.CTkLabel(ctrl, text="Velocidad:", font=("Courier New", 10),
                     text_color=TEXT).pack(side="left", padx=14, pady=10)

        self._slider = ctk.CTkSlider(ctrl, from_=0.05, to=1.5, number_of_steps=29,
                                     width=160, button_color=ACCENT,
                                     progress_color=PURPLE, command=self._on_speed)
        self._slider.set(0.5)
        self._slider.pack(side="left", padx=6)

        self._lbl_speed = ctk.CTkLabel(ctrl, text="0.50s",
                                       font=("Courier New", 9), text_color=SUBTEXT, width=45)
        self._lbl_speed.pack(side="left")

        self._btn = ctk.CTkButton(ctrl, text="▶  INICIAR",
                                  font=("Courier New", 12, "bold"),
                                  fg_color=GREEN, hover_color="#059669",
                                  width=130, command=self._toggle)
        self._btn.pack(side="left", padx=16)

        ctk.CTkButton(ctrl, text="⟳  REINICIAR",
                      font=("Courier New", 11),
                      fg_color=BORDER, hover_color="#334155",
                      width=120, command=self._reset).pack(side="left", padx=4)

        self._lbl_status = ctk.CTkLabel(ctrl, text="",
                                        font=("Courier New", 10, "bold"),
                                        text_color=GREEN)
        self._lbl_status.pack(side="right", padx=16)

    # ──────────────────────────────────────────────
    #  WIDGET AUXILIAR: tarjeta de métrica
    # ──────────────────────────────────────────────

    def _card(self, parent: ctk.CTkFrame, title: str, value: str, color: str) -> ctk.CTkFrame:
        f = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=10)
        ctk.CTkLabel(f, text=title,
                     font=("Courier New", 9, "bold"),
                     text_color=SUBTEXT).pack(pady=(12, 2))
        lbl = ctk.CTkLabel(f, text=value,
                           font=("Courier New", 22, "bold"),
                           text_color=color)
        lbl.pack(pady=(0, 12))
        f._lbl = lbl
        return f

    # ──────────────────────────────────────────────
    #  CALLBACKS DE CONTROLES
    # ──────────────────────────────────────────────

    def _on_speed(self, v: float):
        self._lbl_speed.configure(text=f"{float(v):.2f}s")

    def _aplicar_limite(self):
        raw = self._entry_limite.get().replace(",", "").replace(".", "").strip()
        try:
            valor = int(raw)
            if valor < 100:
                raise ValueError("El límite debe ser mayor a 100")
        except ValueError:
            self._lbl_limite_info.configure(
                text="⚠  Ingresa un número entero mayor a 100",
                text_color=RED)
            return

        self._limite = valor
        self._target = hora_limite(self._limite)
        #self._reset()

        self._lbl_header_meta.configure(text=f"Límite: {self._limite:,}")
        self._lbl_prog_title.configure(text=f"Progreso hacia {self._limite:,}")
        self._lbl_prog.configure(text=f"0 / {self._limite:,}  (0.0%)")
        self._lbl_limite_info.configure(
            text=f"✔  Límite establecido en {self._limite:,} bacterias",
            text_color=GREEN)

    def _toggle(self):
        if self._running:
            self._running = False
            self._btn.configure(text="▶  REANUDAR", fg_color=GREEN)
        else:
            self._running = True
            self._btn.configure(text="⏸  PAUSAR", fg_color=AMBER)
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._run, daemon=True)
                self._thread.start()

    def _reset(self):
        self._running = False
        self._hora = 0
        self._chart_data = []
        self._alerta_mostrada = False

        self._btn.configure(text="▶  INICIAR", fg_color=GREEN, state="normal")
        self._lbl_status.configure(text="")

        self._c_nuevas._lbl.configure(text="100")
        self._c_muertas._lbl.configure(text="0")
        self._c_total._lbl.configure(text="100", text_color=GREEN)

        self._progress.set(0)
        self._lbl_prog.configure(text=f"0 / {self._limite:,}  (0.0%)")

        self._canvas.delete("all")
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")
        self.destroy()
        new_app = BacteriaApp()
        new_app.mainloop()

    # ──────────────────────────────────────────────
    #  HILO DE SIMULACIÓN
    # ──────────────────────────────────────────────

    def _run(self):
        n = self._hora

        while True:
            if not self._running:
                time.sleep(0.05)
                continue

            bn = B(n)
            mn = M(n)
            pn = P(n)

            self.after(0, self._update, n, bn, mn, pn)

            if pn > self._limite:
                if not self._alerta_mostrada:
                    self._alerta_mostrada = True
                    limite_snap = self._limite
                    self.after(200, lambda h=n, p=pn, l=limite_snap: AlertaPopup(self, h, p, l))
                    self.after(0, self._lbl_status.configure,
                               {"text": f"🎯 ¡Límite superado en hora {n}!"})

                self._running = False
                self.after(0, lambda: self._btn.configure(
                    text="✔  LÍMITE ALCANZADO",
                    fg_color=SUBTEXT,
                    state="disabled"
                ))

                break

            self._hora = n
            n += 1
            time.sleep(float(self._slider.get()))

    # ──────────────────────────────────────────────
    #  ACTUALIZACIÓN DE LA UI
    # ──────────────────────────────────────────────

    def _update(self, n: int, bn: int, mn: int, pn: int):
        self._c_nuevas._lbl.configure(text=f"{bn:,}")
        self._c_muertas._lbl.configure(text=f"{mn:,}")
        self._c_total._lbl.configure(
            text=f"{pn:,}",
            text_color=GREEN if pn > self._limite else TEXT)

        ratio = min(pn / self._limite, 1.0)
        self._progress.set(ratio)
        self._lbl_prog.configure(
            text=f"{min(pn, self._limite):,} / {self._limite:,}  ({ratio*100:.1f}%)")

        marker = "  ◀ ¡LÍMITE!" if pn > self._limite else ""
        linea  = f"  {n:^4}   {bn:>12,}   {mn:>12,}   {pn:>12,}{marker}\n"
        self._log.configure(state="normal")
        self._log.insert("end", linea)
        self._log.see("end")
        self._log.configure(state="disabled")

        self._chart_data.append((pn, mn))
        self._draw_chart()

    # ──────────────────────────────────────────────
    #  GRÁFICA DE BARRAS APILADAS
    # ──────────────────────────────────────────────

    def _draw_chart(self):
        c = self._canvas
        c.delete("all")

        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or h < 10 or not self._chart_data:
            return

        vivas   = [d[0] for d in self._chart_data]
        muertas = [d[1] for d in self._chart_data]

        pl, pr, pt, pb = 60, 14, 16, 28
        cw = w - pl - pr
        ch = h - pt - pb
        mx = max(max(vivas), 1)
        n  = len(self._chart_data)

        for i in range(5):
            y   = pt + ch * i / 4
            val = mx * (4 - i) / 4
            c.create_line(pl, y, w - pr, y, fill="#1e293b", dash=(4, 4))
            c.create_text(pl - 4, y, text=self._fmt(val),
                          fill=SUBTEXT, font=("Courier New", 7), anchor="e")

        if mx >= self._limite:
            ym = pt + ch * (1 - self._limite / mx)
            c.create_line(pl, ym, w - pr, ym, fill=GREEN, dash=(6, 3), width=1)
            c.create_text(w - pr - 2, ym - 7, text=self._fmt(self._limite),
                          fill=GREEN, font=("Courier New", 7), anchor="e")

        slot = cw / n
        bw   = max(2, slot * 0.7)

        for i, (v, m) in enumerate(self._chart_data):
            x1   = pl + i * slot + (slot - bw) / 2
            x2   = x1 + bw
            base = pt + ch

            h_m = ch * (m / mx) if m > 0 else 0
            h_v = ch * (v / mx)

            if h_m > 0:
                c.create_rectangle(x1, base - h_m, x2, base,
                                   fill=RED, outline="")

            col = GREEN if v > self._limite else ACCENT
            c.create_rectangle(x1, base - h_m - h_v, x2, base - h_m,
                               fill=col, outline="")

        step = max(1, n // 8)
        for i in range(0, n, step):
            x = pl + i * slot + bw / 2
            c.create_text(x, h - 6, text=str(i),
                          fill=SUBTEXT, font=("Courier New", 7))

    # ──────────────────────────────────────────────
    #  UTILIDADES
    # ──────────────────────────────────────────────

    def _fmt(self, val: float) -> str:
        if val >= 1_000_000: return f"{val/1e6:.1f}M"
        if val >= 1_000:     return f"{val/1e3:.0f}K"
        return str(int(val))


if __name__ == "__main__":
    app = BacteriaApp()
    app.mainloop()

