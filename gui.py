import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import tkinter
import tkinter.messagebox
import customtkinter
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.x = []
        self.y = []
        self.z = []
        self.plottingCanvas = None
        self.pause = False

        # configure window
        self.title("Fallkapsel Server")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Fallkapsel Server", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidbar-buttons for plotting
        self.sidebar_start_button = customtkinter.CTkButton(self.sidebar_frame, command=self.start_plot_event, text="Start")
        self.sidebar_start_button.grid(row=1, column=0, padx=20, pady=10)
        self.siedbar_pause_button = customtkinter.CTkButton(self.sidebar_frame, command=self.pause_plot_event, text="Stop")
        self.siedbar_pause_button.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_save_button = customtkinter.CTkButton(self.sidebar_frame, command=self.save_plot_event, text="Save")
        self.sidebar_save_button.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_reset_button = customtkinter.CTkButton(self.sidebar_frame, command=self.reset_state_event, text="Reset")
        self.sidebar_reset_button.grid(row=4, column=0, padx=20, pady=10)

        # Buttons for UI customisations
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # Plot
        self.fig = plt.Figure(figsize = (5, 5),
                    dpi = 100)
        self.current_plot = self.fig.add_subplot(111)

        # draw canvas
        self.plottingCanvas = FigureCanvasTkAgg(self.fig, self)
        self.plottingCanvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", rowspan=4)
        self.plottingCanvas.draw()

    def update_data(self, x : float, y : float, z : float):
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        print("resetting")
         # adding the subplot
        self.current_plot = self.fig.add_subplot(111)
        self.current_plot.plot(self.x)
        self.current_plot.plot(self.y)
        self.current_plot.plot(self.z)
        # draw canvas
        self.plottingCanvas = FigureCanvasTkAgg(self.fig, self)
        self.plottingCanvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", rowspan=4)
        self.plottingCanvas.draw()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def start_plot_event(self):
        global pause
        pause = False
    
    def pause_plot_event(self):
        global pause
        pause = True

    def save_plot_event(self):
        timestamp = time.localtime()
        timestamp = time.strftime("%H_%M_%S", timestamp)
        self.fig.savefig(f'Acceleration_{timestamp}.png')

    def reset_state_event(self):
        self.x = []
        self.y = []
        self.z = []
        print("resetting")
         # adding the subplot
        self.current_plot = self.fig.add_subplot(111)
        self.current_plot.plot(self.x)
        self.current_plot.plot(self.y)
        self.current_plot.plot(self.z)
        # draw canvas
        self.plottingCanvas = FigureCanvasTkAgg(self.fig, self)
        self.plottingCanvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", rowspan=4)
        self.plottingCanvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()