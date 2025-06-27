import tkinter as tk
from tkinter import messagebox
import time

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")
        master.geometry("400x350") # Aumentamos un poco la altura para el contador
        master.resizable(False, False)

        self.pomodoro_time = 1 * 60  # 25 minutos en segundos
        self.short_break_time = 1 * 60  # 5 minutos en segundos
        self.long_break_time = 15 * 60 # 15 minutos en segundos (no implementado en este básico)
        self.current_time = self.pomodoro_time # Inicia directamente con el tiempo de pomodoro
        self.running = False
        self.session_type = "Pomodoro" # "Pomodoro", "Descanso Corto"
        self.pomodoro_cycles_completed = 0 # Contador para los ciclos completados

        # --- Componentes de la UI ---
        self.label_timer = tk.Label(master, text="00:00", font=("Arial", 60, "bold"), bg="black", fg="lime")
        self.label_timer.pack(pady=20, expand=True)

        self.label_session = tk.Label(master, text="Listo para Pomodoro", font=("Arial", 16), fg="white")
        self.label_session.pack()

        # Label para el contador de ciclos
        self.label_cycles = tk.Label(master, text="Ciclos completados: 0", font=("Arial", 14), fg="cyan")
        self.label_cycles.pack(pady=10) # Añadir un poco de padding

        self.btn_frame = tk.Frame(master)
        self.btn_frame.pack(pady=10)

        self.btn_start = tk.Button(self.btn_frame, text="Iniciar Pomodoro", command=self.start_timer, font=("Arial", 12))
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(self.btn_frame, text="Pausar", command=self.pause_timer, font=("Arial", 12), state=tk.DISABLED)
        self.btn_pause.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(self.btn_frame, text="Reiniciar", command=self.reset_timer, font=("Arial", 12))
        self.btn_reset.grid(row=0, column=2, padx=5)

        self.btn_skip = tk.Button(self.btn_frame, text="Saltar", command=self.skip_timer, font=("Arial", 12))
        self.btn_skip.grid(row=0, column=3, padx=5)

        # Configuración inicial del temporizador y pantalla
        self.set_timer_display(self.current_time) # Muestra el tiempo inicial (25:00)
        master.configure(bg="black") # Fondo de la ventana principal

    def set_timer_display(self, seconds):
        """Formatea los segundos a MM:SS y actualiza la etiqueta."""
        minutes = seconds // 60
        secs = seconds % 60
        time_format = f"{minutes:02d}:{secs:02d}"
        self.label_timer.config(text=time_format)

    def update_cycles_display(self):
        """Actualiza la etiqueta que muestra los ciclos completados."""
        self.label_cycles.config(text=f"Ciclos completados: {self.pomodoro_cycles_completed}")

    def start_timer(self):
        """Inicia o reanuda el temporizador."""
        if not self.running:
            self.running = True
            self.btn_start.config(text="Reanudar", state=tk.DISABLED)
            self.btn_pause.config(state=tk.NORMAL)

            if self.session_type == "Pomodoro":
                self.label_session.config(text="¡A concentrarse!", fg="red")
            else: # Descanso Corto
                self.label_session.config(text="¡Hora de descansar!", fg="green")
            
            self.countdown() 

    def pause_timer(self):
        """Pausa el temporizador."""
        if self.running:
            self.running = False
            self.btn_start.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)
            self.label_session.config(text="Pausado")
            if hasattr(self, '_job_id'):
                self.master.after_cancel(self._job_id)

    def reset_timer(self):
        """Reinicia el temporizador y el contador de ciclos al estado inicial."""
        self.pause_timer() # Pausa si está corriendo
        self.session_type = "Pomodoro"
        self.current_time = self.pomodoro_time
        self.pomodoro_cycles_completed = 0 # Reiniciamos el contador de ciclos
        self.set_timer_display(self.current_time)
        self.update_cycles_display() # Actualiza la visualización del contador
        self.label_session.config(text="Listo para Pomodoro", fg="white")
        self.btn_start.config(text="Iniciar Pomodoro", state=tk.NORMAL)

    def skip_timer(self):
        """Salta la sesión actual y cambia a la siguiente."""
        self.pause_timer() # Asegurarse de que el temporizador esté pausado
        
        if self.session_type == "Pomodoro":
            # Si se salta un pomodoro, no se considera completado
            self.session_type = "Descanso Corto"
            self.current_time = self.short_break_time
            messagebox.showinfo("Sesión Saltada", "Pomodoro saltado. ¡Es hora de un descanso corto!")
        else: # Estaba en Descanso Corto
            self.session_type = "Pomodoro"
            self.current_time = self.pomodoro_time
            messagebox.showinfo("Sesión Saltada", "Descanso saltado. ¡De vuelta al Pomodoro!")

        self.set_timer_display(self.current_time)
        self.label_session.config(text=f"Listo para {self.session_type}", fg="white")
        self.btn_start.config(text=f"Iniciar {self.session_type}", state=tk.NORMAL)


    def countdown(self):
        """Función recursiva para el conteo regresivo."""
        if self.running and self.current_time > 0:
            self.current_time -= 1
            self.set_timer_display(self.current_time)
            self._job_id = self.master.after(1000, self.countdown)
        elif self.running and self.current_time == 0:
            self.running = False
            # Manejo del final de la sesión
            if self.session_type == "Pomodoro":
                # Un Pomodoro ha terminado, ahora vamos al descanso.
                # NO incrementamos el ciclo aquí, ya que el ciclo completo incluye el descanso.
                self.session_type = "Descanso Corto"
                self.current_time = self.short_break_time
                messagebox.showinfo("Pomodoro Terminado", "¡Pomodoro completado! Es hora de un descanso corto.")
            else: # self.session_type == "Descanso Corto"
                # Un Descanso Corto ha terminado, lo que significa que un ciclo completo ha finalizado.
                self.pomodoro_cycles_completed += 1 # ¡Aquí se incrementa el contador!
                self.update_cycles_display()        # ¡Aquí se actualiza la visualización!
                self.session_type = "Pomodoro"
                self.current_time = self.pomodoro_time
                messagebox.showinfo("Descanso Terminado", f"¡Descanso terminado! Ciclo {self.pomodoro_cycles_completed} completado. De vuelta al Pomodoro.")

            self.set_timer_display(self.current_time)
            self.label_session.config(text=f"Listo para {self.session_type}", fg="white")
            self.btn_start.config(text=f"Iniciar {self.session_type}", state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()