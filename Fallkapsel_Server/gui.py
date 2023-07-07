import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter
import tkinter.messagebox
import customtkinter
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    """
    An application for displaying and updating a plot of acceleration data.

    Attributes:
        x (list): List of x-axis acceleration values.
        y (list): List of y-axis acceleration values.
        z (list): List of z-axis acceleration values.
        plottingCanvas (FigureCanvasTkAgg): Canvas for displaying the plot.
        paused (bool): Flag indicating whether the plot display is paused.
        starttime (struct_time): The initial time when the application is started.
        fig (Figure): Figure object for the plot.
        current_plot (AxesSubplot): The current subplot for the plot.

    Methods:
        update_data(x, y, z): Updates the displayed plot by adding the given x, y, and z values.
        change_appearance_mode_event(new_appearance_mode): Changes the appearance mode of the GUI.
        change_scaling_event(new_scaling): Changes the scaling of the GUI.
        start_plot_event(): Continues the displaying of the received data in the GUI.
        pause_plot_event(): Stops the displaying of the received data in the GUI.
        save_plot_event(): Opens a save file dialog to save the current plot displayed in the GUI.
        set_initial_state(): Sets/reset the plot to its initial state.
    """
    def __init__(self):
        super().__init__()
        self.x = []
        self.y = []
        self.z = []
        self.plottingCanvas = None
        self.paused = False
        self.starttime = time.localtime()   

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
        self.sidebar_reset_button = customtkinter.CTkButton(self.sidebar_frame, command=self.set_inital_state, text="Reset")
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

        # setup Plot
        self.fig = plt.Figure(figsize = (5, 5),
                    dpi = 100)
        self.current_plot = self.fig.add_subplot(111)

        # setup canvas
        self.plottingCanvas = FigureCanvasTkAgg(self.fig, self)
        self.plottingCanvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", rowspan=4)
        # set inital state
        self.set_inital_state()

    def update_data(self, x: float, y: float, z: float):
        """Updates the displayed plot, by adding the given x, y, z values.

        Args:
            x (float): x-axis acceleration value
            y (float): y-axis acceleration value
            z (float): z-axis acceleration value
        """
        if not self.paused:
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
            # adding the subplot
            self.current_plot.plot(self.x,color='red', label='x-Richtung')
            self.current_plot.plot(self.y,color='blue', label='y-Richtung')
            self.current_plot.plot(self.z,color='green', label='z-Richtung')
            # update canvas
            self.plottingCanvas.draw()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Changes the appearance mode of the GUI.

        Args:
            new_appearance_mode (str): Appearance mode as string, can be: light, dark, system
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        """Changes the scaling of the GUI.

        Args:
            new_scaling (str): The new scaling in percent as a String.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def start_plot_event(self):
        """Continues the displaying of the recieved data in the GUI.
        """
        self.paused = False
    
    def pause_plot_event(self):
        """Stops the displaying of the recieved data in the GUI.
        """
        self.paused = True

    def save_plot_event(self):
        """Opens a save file dialog to save the current fig displayde in the GUI to the choosen location.
        """
        timestamp = time.localtime()
        timestamp = time.strftime("%H_%M_%S", timestamp)
        files = [('PNG Files', '*.png'), 
                ('JPG Files', '*.jpg')]
        file = tkinter.filedialog.asksaveasfile(filetypes = files, defaultextension = '.png', initialfile=f'image_{timestamp}' )
        if file is not None:
            self.fig.savefig(os.path.abspath(file.name))

    def set_inital_state(self):
        """Sets/resets the plot to its initial state.
        """
        # clear remaining data
        self.x = []
        self.y = []
        self.z = []
        # clear old axis
        self.current_plot.cla()
        # introduce lables for legend
        self.current_plot.plot(self.x,color='red', label='x-Richtung')
        self.current_plot.plot(self.y,color='blue', label='y-Richtung')
        self.current_plot.plot(self.z,color='green', label='z-Richtung')
        # add formatting to plot
        self.current_plot.legend(loc= 'upper right')
        self.current_plot.set_title('Beschleunigung der Kapsel')
        self.current_plot.set_ylabel('Beschleunigung')
        self.current_plot.set_xlabel('Zeit')
        # draw canvas
        self.plottingCanvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()