import tkinter as tk
import datetime
import math
import beepy

class GUI:

    def __init__(self, root):
        """
        Initializes all frames and widgets for the main view of the timer.
        Sets up the timer, start/pause button, settings button, and shift label which
        tells the user which shift they are on (work or break)
        :param root: The window object declared outside the init
        """
        # settigs for the application, determines a number of the functional features.
        self.appSettings = {
            "workLength": 25 * 60000,
            "breakLength": 5 * 60000,
            "longBreakLength": 25 * 60000,
            "numCycles": 4
        }

        self.running = False  # state is a way to track which state the app is in: paused = 0, counting = 1,
        self.updated_time = None
        self.numPomodoros = 1

        self.root = root

        self.currentTime = self.appSettings["workLength"]
        # timer frame code, controls upper frame, countdown and positionings
        self.timerFrame = tk.Frame(master=root, height=300, width=500, bg='#1e1e1e')
        self.timerFrame.pack(fill=tk.X)

        self.timer = tk.Label(master=self.timerFrame, text=self.formatTime(self.currentTime), font='Arial 100 bold',bg='#1e1e1e', fg='white')
        self.timer.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # interaction frame code, controls button placements and fields.
        self.interactionFrame = tk.Frame(master=root,width=500, bg="blue")
        self.interactionFrame.pack(fill=tk.X)

        # set interactions grid
        self.interactionFrame.rowconfigure(0, minsize=50, weight=1)
        self.interactionFrame.columnconfigure([0, 1, 2], minsize=50, weight=1)

        # fill interactions grid with buttons, start/stop and settings button and shift label.
        self.startStopBtn = tk.Button(master=self.interactionFrame, text="Start", command=self.startTimer, bg='#1e1e1e', fg='white')
        self.startStopBtn.grid(row=0, column=0, sticky="nsew")

        self.settingsBtn = tk.Button(master=self.interactionFrame, text="Settings", command=self.openSettings, bg='#1e1e1e', fg='white')
        self.settingsBtn.grid(row=0, column=1, sticky="nsew")

        self.shiftLabel = tk.Label(master=self.interactionFrame, text="WORK", font='Arial 40 bold', fg="white", bg='#1e1e1e')
        self.shiftLabel.grid(row=0, column=2, sticky="nsew")


    def formatTime(self, time):
        """

        :param time: a time in ms to format to MM:SS
        :return: string, the time remaining in the current shift.
        """

        seconds = math.floor(time / 1000)
        minutes = math.floor(seconds / 60)
        hours = math.floor(minutes / 60)

        seconds = seconds % 60
        minutes = minutes % 60
        res = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        if hours != 0:  #if timer needs to account for hours as well.
            res = str(hours) + ":" + res
        return res


    def determineShift(self):
        """
        Determines the correct shift the timer should be on (break, work, long break)
        Sets the on screen label to inform the user which shift they are in.
        :return: int, the appropriate ms value to its call point for use.
        """

        if self.numPomodoros % 2 == 0:  # break pomodoro since they always happen on even shifts
            self.shiftLabel["text"] = "BREAK"
            if self.numPomodoros % (self.appSettings["numCycles"] * 2) == 0:
                time = self.appSettings["longBreakLength"]
            else:
                time = self.appSettings["breakLength"]

        else:
            time = self.appSettings["workLength"]
            self.shiftLabel["text"] = "WORK"

        return time

    def startTimer(self):
        """
        Sets up the states for when the timer is running. Called by the Start button widget
        """
        if not self.running:

            # setup the timer starter
            self.updateTimer()
            self.running = True

            # update button state, set to pause button functionality
            self.startStopBtn['text'] = 'Pause'
            self.startStopBtn['command'] = self.stopTimer

    def stopTimer(self):
        """
        Stops the timer from running, called by the Pause button widget.
        """
        if self.running:
            self.running = False
            self.timer.after_cancel(self.updated_time) #retrieve the timer label's state before cancel.

            # update button state, set to start button functionality
            self.startStopBtn['text'] = 'Start'
            self.startStopBtn['command'] = self.startTimer

    def resetTimer(self):
        """
        resets the timer to the next shift. Sets next time for the user to start on. Called when currentTime == 0
        or when settings were changed.
        """
        self.numPomodoros += 1
        self.stopTimer()
        self.currentTime =self.determineShift()
        self.timer.config(text=self.formatTime(self.currentTime))

    def updateTimer(self):
        """
        updates the timer label every 1000 ms unless currentTime == 0, in which case will reset the timer
        """
        self.timer.config(text=self.formatTime(self.currentTime))  # update displayed time to user

        if self.currentTime == 0:  # exit when timer reaches 0.
            beepy.beep(sound="ping")
            self.resetTimer()
            return

        # call updateTimer 1000 ms later, with an update to currentTime
        self.currentTime = self.currentTime - 1000
        self.updated_time = self.timer.after(1000, self.updateTimer)


    def openSettings(self):
        """
        Opens the settings grid, which allows for the user to change things like:
        break duration, long break duration, work duration, number per cycle
        """

        # set settings frame
        self.settingsFrame = tk.Frame(master=self.root)
        self.settingsFrame.pack()

        # set grid for settings menu.
        self.settingsFrame.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
        self.settingsFrame.columnconfigure([0, 1], minsize=50, weight=1)

        # populate settings fields and apply button

        workLabel = tk.Label(master=self.settingsFrame, text="Work duration (min): ")
        self.workEntry = tk.Entry(master=self.settingsFrame, width="10")

        breakLabel = tk.Label(master=self.settingsFrame, text="Break duration (min):")
        self.breakEntry = tk.Entry(master=self.settingsFrame, width="10")

        longBreakLabel = tk.Label(master=self.settingsFrame, text="Long break duration (min):")
        self.longBreakEntry = tk.Entry(master=self.settingsFrame, width="10")

        cycleLabel = tk.Label(master=self.settingsFrame, text="number of Pomodoros per cycle: ")
        self.cycleEntry = tk.Entry(master=self.settingsFrame, width="10")

        # populate all entry field with current settings so user knows what they are
        self.workEntry.delete(0)
        self.workEntry.insert(0, int(self.appSettings["workLength"] / 60000))
        self.breakEntry.delete(0)
        self.breakEntry.insert(0, int(self.appSettings["breakLength"] / 60000))
        self.longBreakEntry.delete(0)
        self.longBreakEntry.insert(0, int(self.appSettings["longBreakLength"] / 60000))
        self.cycleEntry.insert(0, int(self.appSettings["numCycles"]))

        self.applySettingsBtn = tk.Button(master=self.settingsFrame,text="Apply Settings \n (This will reset the timer)",command=self.applySettings)

        # generate onto grid
        workLabel.grid(row=0, column=0, sticky="nsew")
        self.workEntry.grid(row=0, column=1, sticky="nsew")

        breakLabel.grid(row=1, column=0, sticky="nsew")  # display the break label
        self.breakEntry.grid(row=1, column=1, sticky="nsew")

        longBreakLabel.grid(row=2, column=0, sticky="nsew")  # display the long break label
        self.longBreakEntry.grid(row=2, column=1, sticky="nsew")

        cycleLabel.grid(row=3, column=0, sticky="nsew")
        self.cycleEntry.grid(row=3, column=1, sticky="nsew")

        self.applySettingsBtn.grid(row=4, column=1, sticky="nsew")

        # disable settings button from oppening more settings frames, make it function as apply
        self.settingsBtn["command"] = self.closeSettings

    def applySettings(self):
        """
        Applies settings entered by the user in their respective fields. Converts minutes into ms
        For storage in our settings dictionary.
        """
        # apply all settings to global settings dictionary
        self.appSettings["workLength"] = int(self.workEntry.get()) * 60000
        self.appSettings["breakLength"] = int(self.breakEntry.get()) * 60000
        self.appSettings["longBreakLength"] = int(self.longBreakEntry.get()) * 60000
        self.appSettings["numCycles"] = int(self.cycleEntry.get())

        self.closeSettings()

        # since user changed settings, start app from beginning
        self.numPomodoros = 0
        self.resetTimer()

    def closeSettings(self):
        """
        Closes the settings page, flips function of settingsBtn to open settings page again.
        """
        # close the grid, removing the menu from users view
        self.settingsFrame.destroy()
        # re-enable settings button function
        self.settingsBtn["command"] = self.openSettings




#run the code
root = tk.Tk()
root.title("Pomodoro Timer")
window = GUI(root)
root.mainloop()