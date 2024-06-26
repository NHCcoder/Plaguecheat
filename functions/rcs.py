from win32gui import GetForegroundWindow, GetWindowText

from utils.mouse import move_mouse
from utils.offsets import Client
from utils.player import PlayerPawn
from utils.structs import Offsets, Vec3

nv = Client()
offsets = Offsets()

offsets_dict = {
    'dwEntityList': nv.offset('dwEntityList'),
    'dwLocalPlayerPawn': nv.offset('dwLocalPlayerPawn'),
    'dwSensitivity': nv.offset('dwSensitivity'),
    'dwSensitivity_sensitivity': nv.offset('dwSensitivity_sensitivity'),
    'm_iIDEntIndex': nv.get('C_CSPlayerPawnBase', 'm_iIDEntIndex'),
    'm_iTeamNum': nv.get('C_BaseEntity', 'm_iTeamNum'),
    'm_iHealth': nv.get('C_BaseEntity', 'm_iHealth'),
    'm_iShotsFired': nv.get('C_CSPlayerPawn', 'm_iShotsFired'),
    'm_aimPunchCache': nv.get('C_CSPlayerPawn', 'm_aimPunchCache'),
    'm_angEyeAngles': nv.get('C_CSPlayerPawnBase', 'm_angEyeAngles'),
    'm_aimPunchAngle': nv.get('C_CSPlayerPawn', 'm_aimPunchAngle')
}

offsets.add_offsets(offsets_dict)


def rcs(pm, client, amt):    
    old_punch = Vec3(0.0, 0.0, 0.0)
    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                continue
            
            else:
                player = pm.read_longlong(client + offsets.dwLocalPlayerPawn)
                
                if player:
                    local = PlayerPawn(pm, player, client, offsets)
                    
                    if local.get_aim_punch_cache() and local.get_view_angle() and local.get_shots_fired():
                        
                        punch_angle = Vec3()
                            
                        if local.AimPunchCache.Count <= 0 or local.AimPunchCache.Count > 0xFFFF:
                            continue
                        
                        punch_angle = local.cache_to_punch()
                                            
                        if local.get_shots_fired() > 1:

                            new_punch = Vec3(punch_angle.x - old_punch.x,
                                            punch_angle.y - old_punch.y, 0)
                            
                            new_angle = Vec3(local.ViewAngle.x - new_punch.x * amt,
                                            local.ViewAngle.y - new_punch.y * amt, 0)
                                                    
                            move_mouse(int(((new_angle.y - local.ViewAngle.y) / local.ClientSensitivity) / -0.022),
                                    int(((new_angle.x - local.ViewAngle.x) / local.ClientSensitivity) / 0.022),
                                    False)
                            
                            old_punch = punch_angle
                            
                        else:
                            old_punch = punch_angle

                else:
                    continue
                       
        
        except KeyboardInterrupt:
            break
        
        except Exception:
            pass
        