import time

import glfw
import imgui
import OpenGL.GL as gl
import win32con
import win32gui
from imgui.integrations.glfw import GlfwRenderer
from win32api import GetSystemMetrics

from utils.offsets import Client
from utils.structs import Offsets

ScreenY = GetSystemMetrics(0)
ScreenX = GetSystemMetrics(1)

nv = Client()
offsets = Offsets()

offsets_dict = {
    'dwEntityList': nv.offset('dwEntityList'),
    'dwLocalPlayerPawn': nv.offset('dwLocalPlayerPawn'),
    'dwViewMatrix': nv.offset("dwViewMatrix"),
    'm_lifeState': nv.get('C_BaseEntity','m_lifeState'),
    'm_pGameSceneNode': nv.get('C_BaseEntity','m_pGameSceneNode'),
    'm_modelState': nv.get('CSkeletonInstance','m_modelState'),
    'm_hPlayerPawn': 2028, #nv.get('CCSPlayerController','m_hPlayerPawn'),
    'm_iIDEntIndex': nv.get('C_CSPlayerPawnBase', 'm_iIDEntIndex'),
    'm_iTeamNum': nv.get('C_BaseEntity', 'm_iTeamNum'),
    'm_iHealth': nv.get('C_BaseEntity', 'm_iHealth'),
    'm_iszPlayerName': nv.get("CBasePlayerController", "m_iszPlayerName"),
    'm_pBoneArray': 128
}

offsets.add_offsets(offsets_dict)


def w2s(mtx, posx, posy, posz, width, height):
    screenW = (mtx[12] * posx) + (mtx[13] * posy) + (mtx[14] * posz) + mtx[15]

    if screenW > 0.001:
        screenX = (mtx[0] * posx) + (mtx[1] * posy) + (mtx[2] * posz) + mtx[3]
        screenY = (mtx[4] * posx) + (mtx[5] * posy) + (mtx[6] * posz) + mtx[7]

        camX = width / 2
        camY = height / 2

        x = camX + (camX * screenX / screenW)//1
        y = camY - (camY * screenY / screenW)//1

        return [x, y]

    return [-999, -999]


def bonePos(pm, bone, bone_matrix):    
    x = pm.read_float(bone_matrix + bone * 0x20)
    y = pm.read_float(bone_matrix + bone * 0x20 + 0x4)
    z = pm.read_float(bone_matrix + bone * 0x20 + 0x8)

    return [x, y, z]


# ESP function
def pre_esp(pm, client, draw_list):
    view_matrix = []
    
    for i in range(64):
       
        temp_mat_val = pm.read_float(client + offsets.dwViewMatrix + i * 4)
        view_matrix.append(temp_mat_val)

    local_player_pawn_addr = pm.read_longlong(client + offsets.dwLocalPlayerPawn)

    try:
        local_player_team = pm.read_int(local_player_pawn_addr + offsets.m_iTeamNum)
    except Exception:
        print("You are not in game")
        time.sleep(7)
        return

    for i in range(64):
        
        entity = pm.read_longlong(client + offsets.dwEntityList)

        if not entity:
            continue

        list_entry = pm.read_longlong(entity + ((8 * (i & 0x7FFF) >> 9) + 16))

        if not list_entry:
            continue

        entity_controller = pm.read_longlong(list_entry + (120) * (i & 0x1FF))

        if not entity_controller:
            continue

        entity_controller_pawn = pm.read_longlong(entity_controller + offsets.m_hPlayerPawn)

        if not entity_controller_pawn:
            continue

        list_entry = pm.read_longlong(entity + (0x8 * ((entity_controller_pawn & 0x7FFF) >> 9) + 16))

        if not list_entry:
            continue

        entity_pawn_addr = pm.read_longlong(list_entry + (120) * (entity_controller_pawn & 0x1FF))

        if not entity_pawn_addr or entity_pawn_addr == local_player_pawn_addr:
            continue

        entity_alive = pm.read_int(entity_pawn_addr + offsets.m_lifeState)

        if entity_alive != 256:
            continue
        entity_team = pm.read_int(entity_pawn_addr + offsets.m_iTeamNum)
        if entity_team == local_player_team:
              continue

        player_name = pm.read_string(entity_controller + offsets.m_iszPlayerName, 32)
        player_name = player_name.split("\x00")[0]
          
        health = pm.read_int(entity_pawn_addr + offsets.m_iHealth)
        
        color = imgui.get_color_u32_rgba(0, 0.7, 1, 1)
        
        game_scene = pm.read_longlong(entity_pawn_addr + offsets.m_pGameSceneNode)
        bone_matrix = pm.read_longlong(game_scene + offsets.m_modelState + 0x80)

        try:
            cou_bone = bonePos(pm, 5, bone_matrix)
            shoulderR_bone = bonePos(pm, 8, bone_matrix)
            shoulderL_bone = bonePos(pm, 13, bone_matrix)
            brasR_bone = bonePos(pm, 9, bone_matrix)
            brasL_bone = bonePos(pm, 14, bone_matrix)
            handR_bone = bonePos(pm, 11, bone_matrix)
            handL_bone = bonePos(pm, 16, bone_matrix)
            waist_bone = bonePos(pm, 0, bone_matrix)
            kneesR_bone = bonePos(pm, 23, bone_matrix)
            kneesL_bone = bonePos(pm, 26, bone_matrix)
            feetR_bone = bonePos(pm, 24, bone_matrix)
            feetL_bone = bonePos(pm, 27, bone_matrix)
            
            cou = w2s(view_matrix, cou_bone[0], cou_bone[1], cou_bone[2], ScreenY, ScreenX)
            shoulderR = w2s(view_matrix, shoulderR_bone[0], shoulderR_bone[1], shoulderR_bone[2], ScreenY, ScreenX)
            shoulderL = w2s(view_matrix, shoulderL_bone[0], shoulderL_bone[1], shoulderL_bone[2], ScreenY, ScreenX)
            brasR = w2s(view_matrix, brasR_bone[0], brasR_bone[1], brasR_bone[2], ScreenY, ScreenX)
            brasL = w2s(view_matrix, brasL_bone[0], brasL_bone[1], brasL_bone[2], ScreenY, ScreenX)
            handR = w2s(view_matrix, handR_bone[0], handR_bone[1], handR_bone[2], ScreenY, ScreenX)
            handL = w2s(view_matrix, handL_bone[0], handL_bone[1], handL_bone[2], ScreenY, ScreenX)
            waist = w2s(view_matrix, waist_bone[0], waist_bone[1], waist_bone[2], ScreenY, ScreenX)
            kneesR = w2s(view_matrix, kneesR_bone[0], kneesR_bone[1], kneesR_bone[2], ScreenY, ScreenX)
            kneesL = w2s(view_matrix, kneesL_bone[0], kneesL_bone[1], kneesL_bone[2], ScreenY, ScreenX)
            feetR = w2s(view_matrix, feetR_bone[0], feetR_bone[1], feetR_bone[2], ScreenY, ScreenX)
            feetL = w2s(view_matrix, feetL_bone[0], feetL_bone[1], feetL_bone[2], ScreenY, ScreenX)

            # Skeleton ESP
            draw_list.add_line(cou[0], cou[1], shoulderR[0], shoulderR[1], color, 1)
            draw_list.add_line(cou[0], cou[1], shoulderL[0], shoulderL[1], color, 1)
            draw_list.add_line(brasL[0], brasL[1], shoulderL[0], shoulderL[1], color, 1)
            draw_list.add_line(brasR[0], brasR[1], shoulderR[0], shoulderR[1], color, 1)
            draw_list.add_line(brasR[0], brasR[1], handR[0], handR[1], color, 1)
            draw_list.add_line(brasL[0], brasL[1], handL[0], handL[1], color, 1)
            draw_list.add_line(cou[0], cou[1], waist[0], waist[1], color, 1)
            draw_list.add_line(kneesR[0], kneesR[1], waist[0], waist[1], color, 1)
            draw_list.add_line(kneesL[0], kneesL[1], waist[0], waist[1], color, 1)
            draw_list.add_line(kneesL[0], kneesL[1], feetL[0], feetL[1], color, 1)
            draw_list.add_line(kneesR[0], kneesR[1], feetR[0], feetR[1], color, 1)
            
            headX = pm.read_float(bone_matrix + 6 * 0x20)
            headY = pm.read_float(bone_matrix + 6 * 0x20 + 0x4)
            headZ = pm.read_float(bone_matrix + 6 * 0x20 + 0x8) + 8

            head_pos = w2s(view_matrix, headX, headY, headZ, ScreenY, ScreenX)

            legZ = pm.read_float(bone_matrix + 28 * 0x20 + 0x8)

            leg_pos = w2s(view_matrix, headX, headY, legZ, ScreenY, ScreenX)

            deltaZ = abs(head_pos[1] - leg_pos[1])

            leftX = head_pos[0] - deltaZ // 3.5
            rightX = head_pos[0] + deltaZ // 3.5
            
            topY = head_pos[1] - 12
            bottomY = head_pos[1] + deltaZ

            draw_list.add_line(leftX, head_pos[1], rightX, head_pos[1], color, 1)
            draw_list.add_line(leftX, leg_pos[1], rightX, leg_pos[1], color, 1)

            draw_list.add_line(leftX, head_pos[1], leftX, leg_pos[1], color, 1)
            draw_list.add_line(rightX, head_pos[1], rightX, leg_pos[1], color, 1)
            
            # Head circle
            head_bone = bonePos(pm, 6, bone_matrix)
            head_bone_pos = w2s(view_matrix, head_bone[0], head_bone[1], head_bone[2], ScreenY, ScreenX)
            
            draw_list.add_circle(head_bone_pos[0], head_bone_pos[1], abs(head_pos[1] - cou[1]) / 2, color)

            # Health Bar
            scaled_health_pos = head_pos[1] + ((100 - health) / 100.0) * deltaZ
            
            if health >= 70:
                health_color = imgui.get_color_u32_rgba(0, 128, 0, 1)
            elif 70 > health > 30:
                health_color = imgui.get_color_u32_rgba(255, 140, 0, 1)
            else:
                health_color = imgui.get_color_u32_rgba(255, 0, 0, 1)

            # Draw the health bar
            draw_list.add_line(leftX - 5, scaled_health_pos, leftX - 5, leg_pos[1], health_color, 2)
            draw_list.add_text(leftX, bottomY, imgui.get_color_u32_rgba(1,1,0,1), f"HP: {health}")
            
            # Player Name
            draw_list.add_text(leftX, topY, imgui.get_color_u32_rgba(1,1,0,1), player_name)

        except Exception as e:
            print(f"cant get bones: {e}")
            return


def esp(pm, client):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    window = glfw.create_window(ScreenY, ScreenX, "Overlay", None, None)

    hwnd = glfw.get_win32_window(window)

    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

    ex_style = win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, -2, -2, 0, 0,
                          win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

    glfw.make_context_current(window)

    imgui.create_context()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()
        imgui.set_next_window_size(ScreenY, ScreenX)
        imgui.set_next_window_position(0, 0)

        imgui.begin("overlay", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BACKGROUND)
        draw_list = imgui.get_window_draw_list()

        pre_esp(pm, client, draw_list)

        imgui.end()
        imgui.end_frame()

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()
