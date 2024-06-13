import time
from random import uniform

import keyboard
from pynput.mouse import Button, Controller
from win32gui import GetForegroundWindow, GetWindowText

from utils.offsets import Client
from utils.structs import Offsets

mouse = Controller()
nv = Client()
offsets = Offsets()

offsets_dict = {
    "dwEntityList": nv.offset('dwEntityList'),
    "dwLocalPlayerPawn": nv.offset('dwLocalPlayerPawn'),
    "m_iIDEntIndex": nv.get('C_CSPlayerPawnBase', 'm_iIDEntIndex'),
    "m_iTeamNum": nv.get('C_BaseEntity', 'm_iTeamNum'),
    "m_iHealth": nv.get('C_BaseEntity', 'm_iHealth')
}

offsets.add_offsets(offsets_dict)


def trig(pm, client, triggerkey="shift"):
    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                continue

            if keyboard.is_pressed(triggerkey):
                player = pm.read_longlong(client + offsets.dwLocalPlayerPawn)
                entityId = pm.read_int(player + offsets.m_iIDEntIndex)

                if entityId > 0:
                    entList = pm.read_longlong(client + offsets.dwEntityList)

                    entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                    entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                    entityTeam = pm.read_int(entity + offsets.m_iTeamNum)
                    playerTeam = pm.read_int(player + offsets.m_iTeamNum)

                    if entityTeam != playerTeam:
                        entityHp = pm.read_int(entity + offsets.m_iHealth)
                        if entityHp > 0:
                            time.sleep(uniform(0.01, 0.03))
                            mouse.press(Button.left)
                            time.sleep(uniform(0.01, 0.05))
                            mouse.release(Button.left)

                time.sleep(0.03)
                
            else:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            break
        
        except Exception:
            pass
