import json


class Client:
    def __init__(self):
        try:
            with open('output\offsets.json') as f:
                self.offsets = json.load(f)
        except Exception as e:
            print(f'Unable to get offsets: {e}')
            exit()
               
        try:
            with open('output\client.dll.json') as f:
                self.clientdll = json.load(f)
        except Exception as e:
            print(f"Unable to get client.dll: {e}")
            exit()
            
    def offset(self, a):
        try:
            return self.offsets['client.dll'][a]
        except Exception as e:
            print(f'Offset {a} not found: {e}')
            exit()

    def get(self, a, b):
        try:
            return self.clientdll['client.dll']['classes'][a]['fields'][b]
        except Exception as e:
            print(f'Unable to get {a}, {b}: {e}')
            exit()
