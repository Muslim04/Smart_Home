import tkinter as tk
from dashboard import Dashboard
from automation_system import AutomationSystem
from smart_device import SmartLight, Thermostat, SecurityCamera

if __name__ == "__main__":
    light1 = SmartLight("Living room Light", brightness=40)
    thermostat1 = Thermostat("Living room Thermostat")
    camera1 = SecurityCamera("Front door camera")

    automation_system = AutomationSystem()
    automation_system.add_device(light1)
    automation_system.add_device(thermostat1)
    automation_system.add_device(camera1)

    root = tk.Tk()

    dashboard = Dashboard(root, automation_system)

    root.mainloop()