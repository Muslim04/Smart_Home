import smart_device as SmartLight
class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.is_automation_on = False

    def __init__(self):
        self.devices = []
        self.is_automation_on = False

    def add_device(self, device):
        self.devices.append(device)

    def execute_automation_states(self, task):
        if task == "Turn on lights when motion is detected":
            for device in self.devices:
                if isinstance(device, SmartLight):
                    device.turn_on()