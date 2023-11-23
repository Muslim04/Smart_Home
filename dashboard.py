from datetime import datetime
import tkinter as tk
from smart_device import SmartLight, Thermostat, SecurityCamera
from automation_system import AutomationSystem

class Dashboard:
    def __init__(self, master, automation_system):
        self.master = master
        self.master.title("Smart Home Monitoring Dashboard")
        self.automation_system = automation_system

        # Size of the window
        self.master.geometry('1100x900')
        self.master.configure(bg="lightgrey")  # Changes the background color to light blue

        # Create a font for text widgets and labels
        custom_font = ("Times New Roman", 12)

        # Automation toggle button
        self.automation_button = tk.Button(master, text="Automation ON/OFF", command=self.toggle_automation, font=custom_font)
        self.automation_button.pack()
        self.Automation_status_label = tk.Label(master, text="Automation Status: OFF", font=custom_font)
        self.Automation_status_label.pack()

        self.text_status = tk.Text(master, height=10, width=40, font=custom_font)
        self.text_status.pack()

        self.update_device_status()

        # SmartLight
        self.smart_light_label = tk.Label(master, text=f"{self.automation_system.devices[0].device_id} Brightness", font=custom_font)
        self.smart_light_label.pack()
        self.smart_light_brightness_scale = tk.Scale(master, from_=0, to=100, orient="horizontal", command=lambda value, self=self: self.update_brightness(value), font=custom_font)
        self.smart_light_brightness_scale.pack(pady=0)
        self.smart_light_button = tk.Button(master, text="Toggle ON/OFF", command=self.toggle_smart_light, font=custom_font)
        self.smart_light_button.pack()
        self.smart_light_bright_level = tk.Label(master, text=f"Living room Light - {self.automation_system.devices[0].brightness}%", font=custom_font)
        self.smart_light_bright_level.pack()

        # Thermostat
        self.thermostat_label = tk.Label(master, text=f"{self.automation_system.devices[1].device_id} - Temperature", font=custom_font)
        self.thermostat_label.pack()
        self.thermostat_scale = tk.Scale(master, from_=0, to=50, orient="horizontal", command=self.update_temperature_label, font=custom_font)
        self.thermostat_scale.pack()
        self.thermostat_button = tk.Button(master, text="Toggle ON/OFF", command=self.toggle_thermostat, font=custom_font)
        self.thermostat_button.pack()
        self.thermostat_level_label = tk.Label(master, text=f"Living room Thermostat - {self.automation_system.devices[1].temperature}C", font=custom_font)
        self.thermostat_level_label.pack()

        # Camera
        self.motion_detect_label = tk.Label(master, text="Front door Camera Motion Detection", font=custom_font)
        self.motion_detect_label.pack()
        self.random_motion_detect = tk.Button(master, text="Random Detect Motion", command=self.random_detect, font=custom_font)
        self.random_motion_detect.pack()
        self.camera_button = tk.Button(master, text="Toggle ON/OFF", command=self.toggle_camera, font=custom_font)
        self.camera_button.pack()
        self.camera_status = tk.Label(master, text="Front door Camera - Motion: NO", font=custom_font)
        self.camera_status.pack()

        self.t_light_event = tk.Label(master, text="Brightness Events", font=custom_font)
        self.t_light_event.pack()

        self.light_event = tk.Text(master, height=10, width=80, font=custom_font)
        self.light_event.pack()

    # Other methods remain the same...
        #Automation button functions -- start
    def update_brightness(self, value):
        new_brightness = int(value)
        self.automation_system.devices[0].set_brightness(new_brightness)
        self.smart_light_bright_level.config(text=f"Living room Light - {new_brightness}%")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.brightness_change_text = f"[{current_time}] - Brightness of {self.automation_system.devices[0].device_id} changed to {new_brightness}%"

    def randomize_device_states(self):
        import random

        for device in self.automation_system.devices:
            if isinstance(device,SmartLight):
                    import random
                    device.turn_on()
                    new_brightness = random.randint(1, 100)
                    device.set_brightness(new_brightness)
                    self.smart_light_brightness_scale.set(new_brightness)  # Set the scale to the new brightness
            if isinstance(device,Thermostat):
                    import random
                    device.turn_on()
                    new_temperature = random.randint(1, 100)
                    device.set_temperature(new_temperature)
                    self.thermostat_scale.set(new_temperature)  # Set the scale to the new brightness
            if isinstance(device,SecurityCamera):
                    import random
                    motion_status = random.choice(["YES", "NO"])  # Generate random motion status

                    # Assuming your front door camera is at a specific index in the devices list
                    camera = None
                    for device in self.automation_system.devices:
                        if isinstance(device, SecurityCamera) and device.device_id == "Front door camera":
                            camera = device
                            break

                    if camera:
                        camera.set_security_status("Unsafe" if motion_status == "YES" else "Safe")
                        if motion_status == "YES":
                            for device in self.automation_system.devices:
                                if isinstance(device,SmartLight):
                                    if device.status:
                                        pass
                                    else:
                                        self.toggle_smart_light()
                        self.camera_status.config(text=f"Front door Camera - Motion: {motion_status}")
                    else:
                    # Handle the case where the front door camera is not found in the devices list
                        print("Front door camera not found in the devices list.")
            else:
                pass
    


    def gather_and_store_sensor_data(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("sensor_data.txt","a") as file:
            for device in self.automation_system.devices:
                if isinstance (device,SmartLight):
                    file.write(f"{current_time} - Device: {device.device_id}, Status: {device.status}, Brightness: {device.brightness}%\n")


    def update_device_status(self):
        device_status_text = ""
        for device in self.automation_system.devices:
            device_status_text += f"{device.device_id} - Status: {'ON' if device.status else 'OFF'}\n"

        self.text_status.delete(1.0, tk.END)  # Clear the existing text
        self.text_status.insert(tk.END, device_status_text)

    def update_light_events(self):
        light_status_text = ""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for device in self.automation_system.devices:
            if isinstance(device,SmartLight):
                light_status_text += f"[{current_time}] - {device.device_id} brightness set to {self.smart_light_brightness_scale.get()}%\n"
        
        # self.light_event.delete(1.0,tk.END)
        self.light_event.insert(tk.END,light_status_text)

    def toggle_automation(self):
        if not self.automation_system.is_automation_on:
            self.automation_system.is_automation_on = True
            self.randomize_device_states()
            self.Automation_status_label.config(text="Automation status: ON")
        else:
            self.automation_system.is_automation_on = False
            self.Automation_status_label.config(text="Automation status: OFF")
        
        self.update_device_status()
        self.update_light_events()
        self.gather_and_store_sensor_data()
    #Automation button functions -- end

    #Smart Light -- start
    def toggle_smart_light(self):
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight):
                if device.status:
                    device.turn_off()
                    device.set_brightness(0)
                    self.smart_light_brightness_scale.set(0)  # Set the scale value to 0
                else:
                    import random
                    device.turn_on()
                    new_brightness = random.randint(1, 100)
                    device.set_brightness(new_brightness)
                    self.smart_light_brightness_scale.set(new_brightness)  # Set the scale to the new brightness
        self.update_brightness_label()
        self.update_device_status()
        self.update_light_events()
        self.gather_and_store_sensor_data()
    def update_brightness_label(self, event=None):
        new_brightness = self.smart_light_brightness_scale.get()
        self.automation_system.devices[0].set_brightness(new_brightness)
        self.smart_light_bright_level.config(text=f"Living room Light - {new_brightness}%")

  

    #Smart Light -- end

    #Thermostat functions  --- start

    def toggle_thermostat(self):
        for device in self.automation_system.devices:
            if isinstance(device, Thermostat):
                if device.status:
                    device.turn_off()
                    device.set_temperature(0)
                    self.thermostat_scale.set(0)  # Set the scale value to 0
                else:
                    import random
                    device.turn_on()
                    new_temperature = random.randint(1, 100)
                    device.set_temperature(new_temperature)
                    self.thermostat_scale.set(new_temperature)  # Set the scale to the new brightness
        self.update_temperature_label()
        self.update_device_status()
    def update_temperature_label(self, event=None):
        new_temperature = self.thermostat_scale.get()
        self.automation_system.devices[1].set_temperature(new_temperature)
        self.thermostat_level_label.config(text=f"Living room Thermostat - {new_temperature}%")

    #Thermostat functions --- end


    #Camera -- start
    def random_detect(self):
        for device in self.automation_system.devices:
            if isinstance(device,SecurityCamera):
                if device.status:
                    import random
                    motion_status = random.choice(["YES", "NO"])  # Generate random motion status

                    # Assuming your front door camera is at a specific index in the devices list
                    camera = None
                    for device in self.automation_system.devices:
                        if isinstance(device, SecurityCamera) and device.device_id == "Front door camera":
                            camera = device
                            break

                    if camera:
                        camera.set_security_status("Unsafe" if motion_status == "YES" else "Safe")
                        if motion_status == "YES":
                            for device in self.automation_system.devices:
                                if isinstance(device,SmartLight):
                                    if device.status:
                                        pass
                                    else:
                                        self.toggle_smart_light()
                        self.camera_status.config(text=f"Front door Camera - Motion: {motion_status}")
                    else:
                    # Handle the case where the front door camera is not found in the devices list
                        print("Front door camera not found in the devices list.")
                else:
                    pass
       

    
    def toggle_camera(self):
        for device in self.automation_system.devices:
            if isinstance(device,SecurityCamera):
                if device.status:
                    device.turn_off()
                else:
                    device.turn_on()
        self.update_device_status()