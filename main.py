import pygame
import asyncio
from game import Button, Achievement, AchievementPopup
import random
import time
import os
import webbrowser
import platform
import json, zlib
from cryptography.fernet import Fernet
import pyperclip
KEY = b'eJ9Ece-sJAwmHBmw-D7ubTVt6jX_UVmmTSn7BX2xkQk='
fernet = Fernet(KEY)
try:
    seed = int.from_bytes(os.urandom(8), 'big')
except BytesWarning as e:
    seed = int(time.time())
last_money_tick = pygame.time.get_ticks()
ship_frenzy_tick = pygame.time.get_ticks()
random.seed(seed)
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coastline Clicker BETA")
FONT_PATH = 'assets/fonts/pixel_font.ttf'
font = pygame.font.Font(FONT_PATH, 30)
font2 = pygame.font.Font(FONT_PATH, 20)
font3 = pygame.font.Font(FONT_PATH, 15)
font4 = pygame.font.Font(FONT_PATH, 50)
font5 = pygame.font.Font(FONT_PATH, 10)
font6 = pygame.font.Font(FONT_PATH, 7)
font7 = pygame.font.Font(FONT_PATH, 12)
font8 = pygame.font.Font(FONT_PATH, 13)
clock = pygame.time.Clock()
multiplier = 1.0
reducer = 1.0
reducer_end_time = 0
achievement_popups = []
achievement_queue = []
met_achievements = []
current_popup = None
expedition = {
    'soldiers':[],
    'tanks':[],
    'planes':[],
    'state':'idle'
}
achievements = {
    'achievement1' : Achievement('Free Money?', 'Click Money Button', 1, 'clicks'),
    'achievement2' : Achievement('Clicking Novice', 'Click Money Button 100 Times', 100, 'clicks'),
    'achievement3' : Achievement('Skilled Clicker', 'Click Money Button 250 Times', 250, 'clicks'),
    'achievement4' : Achievement('Proficient Clicker', 'Click Money Button 500 Times', 500, 'clicks'),
    'achievement12' : Achievement('Clicking Elite', 'Click Money Button 2500 Times', 2500, 'clicks'),
    'achievement13' : Achievement('Legendary Clicker', 'Click Money Button 5000 Times', 5000, 'clicks'),
    'achievement14' : Achievement('Clicking God', 'Click Money Button 10000 Times', 10000, 'clicks'),
    'achievement6' : Achievement("Rollin' In It", 'Get to $1000', 1000, 'money'),
    'achievement15' : Achievement('Fortune-Bearer', 'Get to $5000', 5000, 'money'),
    'achievement24' : Achievement('The Golden Emperor', 'Get to $50000', 50000, 'money'),
    'achievement25' : Achievement('Crowned in Cash', 'Get to $25000', 25000, 'money'),
    'achievement26' : Achievement('The Lord of Riches', 'Get to $100000', 100000, 'money'),
    'achievement27' : Achievement('The Infinite Treasury', 'Get to $500000', 500000, 'money'),
    'achievement28' : Achievement('Magnificent Millionaire', 'Get to $1000000', 1000000, 'money'),
    'achievement29' : Achievement('Elon Musk', 'Get to $717900000000', 717900000000, 'money'),
    'achievement30' : Achievement('Cheater!', 'Cheat in $10000000000000000000000000000', 10000000000000000000000000000, 'money'),
    'achievement16' : Achievement('Wealth-Magnet', 'Get to $10000', 10000, 'money'),
    'achievement7' : Achievement('Clicking Master', 'Click Money Button 1000 Times', 1000, 'clicks'),
    'achievement8' : Achievement('Squad Commander', 'Hire 5 Soldiers', 5, 'soldiers'),
    'achievement17' : Achievement('Corporal', 'Hire 10 Soldiers', 10, 'soldiers'),
    'achievement18' : Achievement('Lieutenant', 'Hire 20 Soldiers', 20, 'soldiers'),
    'achievement19' : Achievement('Tank Handler', 'Buy 3 Infantry Tanks', 3, 'tanks'),
    'achievement20' : Achievement('Tank Specialist', 'Buy 10 Infantry Tanks', 10, 'tanks'),
    'achievement21' : Achievement("Sky's the Limit!", 'Buy 8 Fighter Jets', 8, 'planes'),
    'achievement22' : Achievement("Ace Pilot", 'Buy 3 Fighter Jets', 3, 'planes'),
    'achievement23' : Achievement('Air Dominator', 'Buy 5 Fighter Jets', 5, 'planes'),
    'achievement9' : Achievement('Armored Novice', 'Buy an Infantry Tank', 1, 'tanks'),
    'achievement10' : Achievement("Aviator", 'Buy a Fighter Jet', 1, 'planes'),
    'achievement11' : Achievement("More Than Bosnia's Coast!", 'Gain 0.01 Miles of Coastline', 0.01, 'coast')
}

missing_ss = []
missing_tt = []
missing_pp = []
floating_texts2 = []
banner = None
show_banner = False
go_to_flag = True
def bannerbegone():
    global banner, show_banner
    banner = None
    show_banner = False
def update_all_buttons():
    global money, money_per_second, tick_speed, coast_mi, country_name
    global upgrade_money_price, upgrade_money_per_second_price, upgrade_tick_speed_price
    global per_tick_efficiency_upgrade, critical_clicks_price, soldier_price
    global tank_price, plane_price, heal_price, logistic_enhancement_price
    global chance_of_success, ascend_miles, money_per_click, critical_clicks_chance
    if money_per_click >= 10:
        upgrade1.text = ['Upgrade Money Per Click', 'MAX LEVEL']
    else:
        upgrade1.text = ['Upgrade Money Per Click', f'(Price = ${upgrade_money_price})']

    upgrade2.text = ['Upgrade Money Per Tick', f'(Price = ${upgrade_money_per_second_price})']

    if tick_speed <= 50:
        upgrade3.text = [' Reduce Tick Speed ', 'MAX LEVEL']
    else:
        upgrade3.text = [' Reduce Tick Speed ', f'(Price = ${upgrade_tick_speed_price})']
    if pygame.time.get_ticks() < multiplier_end_time:
        upgrade4.text = ['Multiply Money Per Tick', '(ACTIVE - 30s)']
    else:
        upgrade4.text = ['Multiply Money Per Tick', f'(30 seconds | Price = ${per_tick_efficiency_upgrade})']

    if critical_clicks_chance <= 10:
        upgrade5.text = ['Upgrade CritClick Chance', 'MAX LEVEL']
    else:
        upgrade5.text = ['Upgrade CritClick Chance', f'(Price = ${critical_clicks_price})']
    upgrade6.text = ['Hire Infantry Soldier', f'(Price = ${soldier_price:.0f})']
    upgrade7.text = ['Purchase Infantry Tank', f'(Price = ${tank_price:.0f})']
    upgrade8.text = ['Purchase Fighter Jet', f'(Price = ${plane_price:.0f})']
    upgrade9.text = ['Heal Military Units', f'(Price = ${heal_price:.0f})']
    if pygame.time.get_ticks() < reducer_end_time:
        upgrade10.text = ['Enhance Logistics', '(ACTIVE - 30s)']
    else:
        upgrade10.text = ['Enhance Logistics', f'30 Seconds | (Price = ${logistic_enhancement_price:.0f})']
    money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
    coast_knowing.text = f'Coastline: {coast_mi}mi'
    tick_speed_knowing.text = f'Tick speed = {tick_speed}ms'
    name_of_country.text = f'Country: {country_name}'
    ascend_button.text = ['ASCEND', f'{ascend_miles}mi Coastline Required']
    send_expedition.text = ['Send Expedition!', f'Chance of Success: {chance_of_success}%']
def handle_instant_import():
    global banner, show_banner
    encoded_str = pyperclip.paste()
    if not encoded_str:
        banner = Button(pygame.Rect(365, 250, 500, 200), text=['Import Failed', 'Please ensure that you have your save file','code copied to your clipboard (Ctrl + C).', '(ERROR CODE 2: EMPTY CLIPBOARD)'], border_width=3, border_radius=0, border_color=(0,0,0))
        show_banner = True
        return
    try:
        import_save(encoded_str)
    except Exception as e:
        banner = Button(pygame.Rect(365, 250, 500, 200),text=['Import Failed', 'Please ensure that you have your save file','code copied to your clipboard (Ctrl + C).', '[ERROR CODE 1: INVALID CODE]'], border_width=3, border_radius=0, border_color=(0,0,0))
        show_banner = True
        print(f"Error: {e}")
def main_menu():
    global current_screen, go_to_flag
    current_screen = MENU
    go_to_flag = False
def settings():
    global SETTINGS
    SETTINGS = True
def get_save_data():
    return {
        "money": money,
        "army_level": army_level,
        "coast_mi": coast_mi,
        "coast_percent": coast_percent,
        "step_sheets": step_sheets,
        "clicks": clicks,
        "money_per_click": money_per_click,
        "upgrade_money_price": upgrade_money_price,
        "tick_speed": tick_speed,
        "x": x,
        "ascend_miles": ascend_miles,
        "base_money_per_second": base_money_per_second,
        "money_per_second": money_per_second,
        "upgrade_money_per_second_price": upgrade_money_per_second_price,
        "upgrade_tick_speed_price": upgrade_tick_speed_price,
        "per_tick_efficiency_upgrade": per_tick_efficiency_upgrade,
        "multiplier_end_time": multiplier_end_time,
        "original_money_per_second": original_money_per_second,
        "soldiers": soldiers,
        "soldier_price": soldier_price,
        "tanks": tanks,
        "tanks_price": tank_price,
        "planes": planes,
        "plane_price": plane_price,
        "expedition_power": expedition_power,
        "chance_of_success": chance_of_success,
        "ship_spawn_rate": ship_spawn_rate,
        "spawn_end_time": spawn_end_time,
        "critical_clicks_price": critical_clicks_price,
        "critical_clicks_chance": critical_clicks_chance,
        "logistic_enhancement_price": logistic_enhancement_price,
        "heal_price": heal_price,
        "i" : i,
        'country_name' : country_name,
        'achievements' : met_achievements
    }
def export_save():
    global banner,show_banner, SETTINGS
    data = get_save_data()
    json_bytes = json.dumps(data).encode()
    compressed = zlib.compress(json_bytes)
    encrypted = fernet.encrypt(compressed)
    encoded = encrypted.decode()
    pyperclip.copy(encoded)
    banner = Button(pygame.Rect(365, 250, 500, 200),text=['Export Success!', 'Save file code copied to clipboard','(Ctrl + V). Make sure to always save!'], border_width=3,border_radius=0, border_color=(0, 0, 0))
    show_banner = True
    SETTINGS = False
    return encoded
def import_save(encoded_str):
    global banner
    global show_banner
    global SETTINGS
    global go_to_flag
    compressed = fernet.decrypt(encoded_str.encode() if isinstance(encoded_str, str) else encoded_str)
    json_bytes = zlib.decompress(compressed)
    data = json.loads(json_bytes)
    banner = Button(pygame.Rect(365, 250, 500, 200), text=['Import Success!','Your save file has been successfully', 'imported. Make sure to always save!'], border_width=3,border_radius=0, border_color=(0, 0, 0))
    show_banner = True
    SETTINGS = False
    go_to_flag = False
    load_save_data(data)
def load_save_data(data):
    global money, army_level, coast_mi, coast_percent, step_sheets, clicks
    global money_per_click, upgrade_money_price, tick_speed, x, ascend_miles
    global base_money_per_second, money_per_second, met_achievements
    global upgrade_money_per_second_price, upgrade_tick_speed_price
    global per_tick_efficiency_upgrade, multiplier_end_time, original_money_per_second
    global soldiers, soldier_price, tanks, tank_price, planes, plane_price
    global expedition_power, chance_of_success, ship_spawn_rate
    global spawn_end_time, critical_clicks_price, critical_clicks_chance
    global logistic_enhancement_price, heal_price, current_flag, flag_panel, i, country_name

    money = data["money"]
    army_level = data["army_level"]
    coast_mi = data["coast_mi"]
    coast_percent = data["coast_percent"]
    step_sheets = data["step_sheets"]
    clicks = data["clicks"]
    money_per_click = data["money_per_click"]
    upgrade_money_price = data["upgrade_money_price"]
    tick_speed = data["tick_speed"]
    x = data["x"]
    ascend_miles = data["ascend_miles"]
    base_money_per_second = data["base_money_per_second"]
    money_per_second = data["money_per_second"]
    upgrade_money_per_second_price = data["upgrade_money_per_second_price"]
    upgrade_tick_speed_price = data["upgrade_tick_speed_price"]
    per_tick_efficiency_upgrade = data["per_tick_efficiency_upgrade"]
    multiplier_end_time = data["multiplier_end_time"]
    original_money_per_second = data["original_money_per_second"]
    soldiers = data["soldiers"]
    soldier_price = data["soldier_price"]
    tanks = data["tanks"]
    tank_price = data["tanks_price"]
    planes = data["planes"]
    plane_price = data["plane_price"]
    expedition_power = data["expedition_power"]
    chance_of_success = data["chance_of_success"]
    ship_spawn_rate = data["ship_spawn_rate"]
    spawn_end_time = data["spawn_end_time"]
    critical_clicks_price = data["critical_clicks_price"]
    critical_clicks_chance = data["critical_clicks_chance"]
    logistic_enhancement_price = data["logistic_enhancement_price"]
    heal_price = data["heal_price"]
    i = data['i']
    country_name = data['country_name']
    met_achievements = data['achievements']
    flag_panel.image = flags[i]
    flag_panel.image = pygame.transform.scale(flag_panel.image, (250, 175))
    update_all_buttons()
def enhance_logistics():
    global logistic_enhancement_price
    global money
    global enhancement_active
    global reducer, reducer_end_time
    global soldier_price, tank_price, plane_price
    if money < logistic_enhancement_price or enhancement_active:
        return
    upgrade.play()
    reducer = 0.5
    soldier_price = soldier_price * reducer
    tank_price = tank_price * reducer
    plane_price = plane_price * reducer
    upgrade6.text[1] = f'(Price = ${soldier_price:.0f})'
    upgrade7.text[1] = f'(Price = ${tank_price:.0f})'
    upgrade8.text[1] = f'(Price = ${plane_price:.0f})'
    enhancement_active = True
    reducer_end_time = pygame.time.get_ticks()
    money = money - logistic_enhancement_price
    logistic_enhancement_price = round(logistic_enhancement_price * 1.1543, 0)
    upgrade10.text[1] = f'(ACTIVE - 30s)'
    upgrade10.color = (200,200,200)
    upgrade10.pressed_text_color = (0,0,0)
    money_knowing.text[0] = f'You have ${money:.0f}'
    reducer_end_time = 30000
def heal_units():
    global soldiers
    global tanks
    global planes
    global money
    global heal_price
    global upgrade9
    if money < heal_price or (len(planes) <= 0 and len(tanks) <= 0 and len(soldiers) <= 0) or (all(soldier.hp == 50 for soldier in soldiers) and all(plane.hp == 850 for plane in planes) and all(tank.hp == 250 for tank in tanks)):
        upgrade9.color = (200,200,200)
        upgrade9.pressed_text_color = (0,0,0)
        return
    upgrade.play()
    for soldier in soldiers:
        soldier.hp = soldier.hp + (soldier.hp/5)
        if soldier.hp > 50:
            soldier.hp = 50
    for tank in tanks:
        tank.hp = tank.hp + (tank.hp/5)
        if tank.hp > 250:
            tank.hp = 250
    for plane in planes:
        plane.hp = plane.hp + (plane.hp/5)
        if plane.hp > 850:
            plane.hp = 850
    money -= heal_price
    heal_price = round(heal_price * 1.2, 0)
    upgrade9.text[1] = f'(Price = ${heal_price:.0f})'
    money_knowing.text[0] = f'You have ${money:.0f}'
def show_achievement(name_, desc_):
    popup = AchievementPopup(
        name_, width=300, height=60, name2=desc_, font=font8, small_font=font7, smaller_font=font5)
    return popup
def expedition_it():
    global chance_of_success
    global expedition
    global coast_mi
    global expedition_power
    send_expedition.color = (200, 200, 200)
    send_expedition.pressed_text_color = (0,0,0)
    if random.random() < (chance_of_success / 100):
        success.play()
        coast_mi = round((coast_mi + (expedition_power / 70) * (army_level / 1.3)), 2)
        coast_knowing.text = f'Coastline: {coast_mi}mi'
    else:
        downgrade.play()
    for entry in expedition['soldiers'][:]:
        ss, orig_x, orig_y = entry
        ss.hp = ss.hp - random.randint(10, 20)
        if ss.hp <= 0:
            missing_ss.append(orig_x)
            missing_ss.append(orig_y)
            expedition['soldiers'].remove(entry)
            expedition_power = expedition_power - 0.1
            chance_of_success = round(expedition_power * 100, 2)
            send_expedition.text[1] = f'Chance of success: {chance_of_success}%'
    for entry in expedition['tanks'][:]:
        tt, orig_x, orig_y = entry
        tt.hp = tt.hp - random.randint(40, 80)
        if tt.hp <= 0:
            missing_tt.append(orig_x)
            missing_tt.append(orig_y)
            expedition['tanks'].remove(entry)
            expedition_power = expedition_power - 1
            chance_of_success = round(expedition_power * 100, 2)
            send_expedition.text[1] = f'Chance of success: {chance_of_success}%'
    for entry in expedition['planes'][:]:
        pp, orig_x, orig_y = entry
        pp.hp = pp.hp - random.randint(80, 160)
        if pp.hp <= 0:
            missing_pp.append(orig_x)
            missing_pp.append(orig_y)
            expedition['planes'].remove(entry)
            expedition_power = expedition_power - 5
            chance_of_success = round(expedition_power * 100, 2)
            send_expedition.text[1] = f'Chance of success: {chance_of_success}%'
def send_an_expedition():
    global expedition
    global moving
    global available_to_buy
    if expedition['state'] != 'idle':
        return
    expedition['soldiers'] = [(ss, ss.rect.x, ss.rect.y) for ss in soldiers]
    expedition['tanks'] = [(tt, tt.rect.x, tt.rect.y) for tt in tanks]
    expedition['planes'] = [(pp, pp.rect.x, pp.rect.y) for pp in planes]
    soldiers.clear()
    tanks.clear()
    planes.clear()
    expedition['state'] = 'going'
    moving = True
    available_to_buy = False
def check_expedition():
    global chance_of_success
    global send_expedition
    if chance_of_success < 100:
        if chance_of_success < 0.1:
            send_expedition.color = (200,200,200)
            send_expedition.pressed_text_color = (0,0,0)
        elif chance_of_success >= 100:
            chance_of_success = 100
            send_expedition.text[1] = f'Chance of Success: {chance_of_success}%'
            upgrade6.color = (200,200,200)
            upgrade6.pressed_text_color = (0, 0, 0)
            upgrade6.text[1] = 'MAX LEVEL'
            upgrade7.color = (200, 200, 200)
            upgrade7.pressed_text_color = (0, 0, 0)
            upgrade7.text[1] = 'MAX LEVEL'
            upgrade8.color = (200, 200, 200)
            upgrade8.pressed_text_color = (0, 0, 0)
            upgrade8.text[1] = 'MAX LEVEL'
        else:
            send_expedition.color = (255, 255, 255)
            send_expedition.pressed_text_color = (200, 200, 200)
    else:
        send_expedition.color = (255,255,255)
        chance_of_success = 100
        return
def add_plane():
    global money
    global plane_price
    global planes
    global expedition_power
    if money >= plane_price and chance_of_success < 100 and available_to_buy:
        upgrade.play()
        money = money - plane_price
        money_knowing.text[0] = f'You have ${money:.0f}'
        index = len(planes)
        PLANE_H = 80
        PLANE_W = 80
        GAP = 1
        MAX_PER_ROW = 4
        if not missing_pp:
            x5 = 450 + (index % MAX_PER_ROW) * (PLANE_W + GAP)
            y5 = 480 + (index // MAX_PER_ROW) * (PLANE_H + GAP)
        else:
            x5 = missing_pp[0]
            y5 = missing_pp[1]
            missing_pp.pop(0)
            missing_pp.pop(0)
        plane = Button(pygame.Rect(x5, y5, PLANE_W, PLANE_H), image=plane_, color=None)
        plane.name = random.choice([
            'F15',
            'F14 Tomcat',
            'F14',
            'F4',
            'Mig 31 Foxhound',
            'F18'
])
        plane.hp = 850
        plane.visible = True
        planes.append(plane)
        global expedition_power
        expedition_power = expedition_power + 5
        if expedition_power >= 100:
            expedition_power = 100
def add_tank():
    global money
    global tank_price
    global tanks
    global expedition_power
    if money >= tank_price and chance_of_success < 100 and available_to_buy:
        upgrade.play()
        money = money - tank_price
        money_knowing.text[0] = f'You have ${money:.0f}'
        index = len(tanks)
        TANK_W = 50
        TANK_H = 50
        GAP = 1
        MAX_PER_ROW = 7
        if not missing_tt:
            x4 = 440 + (index % MAX_PER_ROW) * (TANK_W + GAP)
            y4 = 410 + (index // MAX_PER_ROW) * (TANK_H + GAP)
        else:
            x4 = missing_tt[0]
            y4 = missing_tt[1]
            missing_tt.pop(0)
            missing_tt.pop(0)
        tank = Button(pygame.Rect(x4, y4, TANK_W, TANK_H), image=tank_, color=None)
        tank.name = random.choice([
            'Renault FT-17',
            'Mark I-V',
            'M4 Sherman',
            'T-34',
            'KV-1',
            'KV-2'
            'M3 Stuart',
            'Panzer IV',
            'Panzer III',
            'M1 Abrams',
            'Leclerc',
            'Merkava MK.4',
            'Type 99',
            'K2 Black Panther',
            'T-90',
            'M60 Patton',
            'T-55',
            'T-62',
            'T-72'
])
        tank.hp = 250
        tank.visible = True
        tanks.append(tank)
        global expedition_power
        expedition_power = expedition_power + 1
        if expedition_power >= 100:
            expedition_power = 100
def add_soldier():
    print(missing_ss)
    global money
    global soldier_price
    global soldiers
    global expedition_power
    if money >= soldier_price and chance_of_success < 100 and available_to_buy:
        upgrade.play()
        money = money - soldier_price
        money_knowing.text[0] = f'You have ${money:.0f}'
        soldier_price = round(soldier_price * 1, 0)
        upgrade6.text = ['Hire Infantry Soldier', f'(Price = ${soldier_price:.0f})']
        index = len(soldiers)
        SOLDIER_W = 8
        SOLDIER_H = 16
        GAP = 7
        MAX_PER_ROW = 23
        if not missing_ss:
            x3 = 450 + (index % MAX_PER_ROW) * (SOLDIER_W + GAP)
            y3 = 370 + (index // MAX_PER_ROW) * (SOLDIER_H + GAP)
        else:
            x3 = missing_ss[0]
            y3 = missing_ss[1]
            missing_ss.pop(0)
            missing_ss.pop(0)
        soldier_ = Button(pygame.Rect(x3,y3,SOLDIER_W,SOLDIER_H), image=random.choice([soldier1_, soldier2_]), color=None)
        soldier_.name = random.choice([
            'Rifleman',
            'Machine Gunner',
            'Mortarman',
            'Scout',
            'Sniper',
            'Missileman',
            'Grenadier'
])
        soldier_.hp = 50
        soldier_.visible = True
        soldiers.append(soldier_)
        global expedition_power
        expedition_power = expedition_power + 0.1
        if expedition_power >= 100:
            expedition_power = 100
def change_screen2():
    global current_upgrade_screen
    current_upgrade_screen = UPGRADE1
def change_screen():
    global current_upgrade_screen
    current_upgrade_screen = UPGRADE2
def increase_crit_chance():
    global money
    global critical_clicks_chance
    global critical_clicks_price
    global upgrade5
    if money >= critical_clicks_price and critical_clicks_chance >= 10:
        upgrade.play()
        critical_clicks_chance = critical_clicks_chance - 11
        if critical_clicks_chance < 1:
            critical_clicks_chance = 1
        money = money - critical_clicks_price
        critical_clicks_price = round(critical_clicks_price * 1.3, 0)
        upgrade5.text = ['Upgrade CritClick Chance', f'(Price = ${critical_clicks_price:.0f})']
        money_knowing.text[0] = f'You have ${money:.0f}'
    else:
        return
def random_event():
    global money
    global money_per_second
    global ship_
    global shipping
    global spawning_fast
    action1 = '+$500'
    action2 = 'Ronaldo Edits (for Benji)!'
    action3 = 'Money Doubled!'
    action4 = '-$500'
    action5 = 'Money Divided'
    action6 = 'Ship Frenzy!'
    actions = [action1,action1,action1,action1,action1,action3,action4,action4,action4,action4,action5]
    action = random.choice(actions)
    if action == action1:
        upgrade.play()
        money = money + 500
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
    elif action == action2:
        upgrade.play()
        downgrade.play()
        urls = [
            'https://www.youtube.com/shorts/LlFX_L8Xnu0',
            'https://www.youtube.com/shorts/9lrO00uUADE',
            'https://www.youtube.com/shorts/7K_BaMYbTX0',
            'https://www.youtube.com/shorts/EvJPWyKiVfU'
        ]
        url = random.choice(urls)
        if platform.system() == 'emscripten':
            import js
            js.window.open(url, '_blank')
        else:
            import webbrowser
            webbrowser.open(url)
    elif action == action3:
        upgrade.play()
        money = money * 2
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
    elif action == action4:
        downgrade.play()
        money = money - 500
        if money < 0:
            money = 0
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
    elif action == action5:
        downgrade.play()
        money = money // 1.5
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
    elif action == action6:
        upgrade.play()
        spawning_fast = True
    ship_.rect.width = 0
    ship_.rect.height = 0
    shipping = False
    x2 = ship_.rect.x + 125
    y2 = ship_.rect.y + 100
    floating_texts2.append({'x': x2, 'y': y2, 'text': f"{action}", 'timer': 30})
def move(thing):
    thing.rect.x = thing.rect.x + 3
def multiply_efficiency():
    global money, multiplier_active, multiplier_end_time, multiplier, per_tick_efficiency_upgrade
    if money < per_tick_efficiency_upgrade or multiplier_active or money_per_second < 1:
        return
    else:
        upgrade.play()
        multiplier = 2.0
        multiplier_active = True
        multiplier_end_time = pygame.time.get_ticks() + 30_000
        per_tick_efficiency_upgrade = round(per_tick_efficiency_upgrade * 1.15, 0)
        money = money - per_tick_efficiency_upgrade
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
        upgrade4.text = ['Multiply Money Per Tick', '(ACTIVE - 30s)']
def increase_tick_speed():
    global tick_speed
    global upgrade_tick_speed_price
    global money
    if money >= upgrade_tick_speed_price and tick_speed > 50:
        upgrade.play()
        tick_speed = tick_speed - random.randint(35, 70)
        tick_speed = max(50, tick_speed)
        money = money - upgrade_tick_speed_price
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
        tick_speed_knowing.text = f'Tick Speed: {tick_speed}ms'
        upgrade_tick_speed_price = round(upgrade_tick_speed_price * (1.2 * random.uniform(1.1, 1.3)),0)
        upgrade3.text[1] = f'(Price = ${upgrade_tick_speed_price:.0f})'
    else:
        upgrade3.color = (200,200,200)
        return
def add_money_per_second():
    global money
    global money_per_second
    ch = click.play()
    if ch:
        ch.set_volume(0.5)
    money = money + money_per_second
    money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
def upgrade_money_per_second():
    global base_money_per_second, upgrade_money_per_second_price, money
    if money >= upgrade_money_per_second_price:
        upgrade.play()
        base_money_per_second += 1
        money -= upgrade_money_per_second_price
        upgrade_money_per_second_price = round(upgrade_money_per_second_price * 1.15, 0)
        money_knowing.text = [f'You have ${money:.0f}',f'Money Per Tick: ${money_per_second}']
        upgrade2.text = ['Upgrade Money Per Tick',f'(Price = ${upgrade_money_per_second_price:.0f})']
def get_font_for_button(button_):
    if isinstance(button_.text, list):
        if button_ == import_button:
            return font2, font2
        total_length = sum(len(line) for line in button_.text)
        length1 = len(button_.text[0])
        length2 = len(button_.text[1])
        if length1 != length2:
            if total_length >= 25:
                if length1 <= 17 and button_ != upgrade10:
                    return font2, font7
                elif button_ == upgrade10:
                    return font7, font5
                else:
                    return font7, font5
            elif 15 <= total_length <= 25:
                return font5, font6
            else:
                return font2, font7
        elif length1 == length2 or (length1 + 1) == length2:
            return font3, font3
    elif isinstance(button_.text, str):
        if button_.text == f'Tick speed = {tick_speed}ms':
            return font7
        length = len(button_.text)
        if length >= 25:
            return font5
        elif length >= 15:
            return font3
        else:
            return font2
    return font2
def check_ascend(button_):
    global coast_mi
    global ascend_miles
    if coast_mi < ascend_miles:
        button_.color = (200,200,200)
        button_.pressed_text_color = (160, 32, 240)
    else:
        button_.color = (255,255,255)
        button_.pressed_text_color = (140, 0, 195)
def check_money(button_, checker):
    global critical_clicks_price
    global upgrade_tick_speed_price
    global enhancement_active
    if button_.action == enhance_logistics and enhancement_active:
        return
    if button_.action == heal_units and money < heal_price or (len(planes) <= 0 and len(tanks) <= 0 and len(soldiers) <= 0) or (all(soldier.hp == 50 for soldier in soldiers) and all(plane.hp == 850 for plane in planes) and all(tank.hp == 250 for tank in tanks)):
        upgrade9.color = (200,200,200)
        upgrade9.pressed_text_color = (0,0,0)
    if tick_speed <= 50 and button_.action == increase_tick_speed:
        button_.text[1] = f'MAX LEVEL'
        button_.color = (200,200,200)
        button_.pressed_text_color = (0,0,0)
        upgrade_tick_speed_price = 999999999999999999999999
    if button_.action == increase_crit_chance and critical_clicks_chance <= 10:
        button_.text[1] = 'MAX LEVEL'
        button_.color = (200, 200, 200)
        button_.pressed_text_color = (0, 0, 0)
        critical_clicks_price = 999999999999999999
    if multiplier_active and button_.action == multiply_efficiency:
        button_.color = (200,200,200)
        button_.pressed_color = (0,0,0)
    if money < checker:
        button_.color = (200,200,200)
        button_.pressed_text_color = (0,0,0)
    else:
        button_.pressed_text_color = (200,200,200)
        button_.color = (255,255,255)
def more_money_when_clicked():
    global money_per_click
    global upgrade_money_price
    global money
    global x
    if money_per_click >= 10:
        upgrade1.text = ['Upgrade Money Per Click', 'MAX LEVEL']
        upgrade1.color = (200, 200, 200)
        upgrade1.pressed_text_color = (0, 0, 0)
        upgrade_money_price = 9999999999
        return
    if money >= upgrade_money_price:
        upgrade.play()
        money = money - upgrade_money_price
        money_per_click += 1
        upgrade_money_price = round(upgrade_money_price * x)
        x += 0.05 * random.uniform(1.45454545, 2.5)
        money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
        upgrade1.text = ['Upgrade Money Per Click', f'(Price = ${upgrade_money_price})']
        if money_per_click >= 10:
            upgrade1.text = ['Upgrade Money Per Click', 'MAX LEVEL']
            upgrade1.color = (200, 200, 200)
            upgrade1.pressed_text_color = (0, 0, 0)

floating_texts = []

def add_money():
    global money
    global money_button
    global clicks
    global x1,y1
    crit = random.randint(1, critical_clicks_chance)
    x1,y1 = pygame.mouse.get_pos()
    x1 = x1 + random.randint(-50,0)
    if crit != 1:
        floating_texts.append({'x': x1, 'y': y1, 'text': f"+${money_per_click}", 'timer': 30})
        money = money + money_per_click
    elif crit == 1:
        x1, y1 = pygame.mouse.get_pos()
        x1 = x1 - 100
        floating_texts.append({'x': x1, 'y': y1, 'text': f"+${money_per_click * 10} (Critical!)", 'timer': 60})
        money = money + (money_per_click * 10)
    money_click.play()
    clicks = clicks + 1
    money_knowing.text = [f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}']
    if clicks > 2:
        money_button.text = ''
def change_flag_up():
    global current_flag
    global i
    global more
    i = i + 1
    if i >= 13:
        i = 13
        more.text_color = (200,200,200)
        less.text_color = (0,255,0)
    elif i == 4:
        i = 5
        click.play()
    else:
        more.text_color = (0,255,0)
        less.text_color = (0,255,0)
        click.play()
    current_flag = flags[i]
def change_flag_down():
    global current_flag
    global i
    global less
    i = i - 1
    if i <= 0:
        i = 0
        less.text_color = (200,200,200)
        more.text_color = (0,255,0)
    elif i == 4:
        i = 3
        click.play()
    else:
        less.text_color = (0,255,0)
        more.text_color = (0,255,0)
        click.play()
    current_flag = flags[i]
def do():
    global SETTINGS
    SETTINGS = False
with open('assets/country_names/country_names.txt', 'r') as names:
    name = names.read().splitlines()
CREDITS = 'credits'
MENU = 'menu'
GAME = 'game'
COUNTRY = 'country'
UPGRADE1 = 'upgrade1'
UPGRADE2 = 'upgrade2'
SETTINGS = False
current_screen = MENU
current_upgrade_screen = UPGRADE1
country_name = str(random.choice(name))

#variables
money = 0
army_level = 1
coast_mi = 0.00
coast_percent = 0.00
step_sheets = 0
clicks = 0
money_per_click = 1
upgrade_money_price = 50
tick_speed = 1000
x = 1.2
ascend_miles = 10
base_money_per_second = 0
money_per_second = 0
upgrade_money_per_second_price = 150
upgrade_tick_speed_price = 300
per_tick_efficiency_upgrade = 1000
multiplier_end_time = 0
original_money_per_second = 0
soldiers = []
soldier_price = 350
tanks = []
tank_price = 1000
planes = []
plane_price = 5000
expedition_power = 0
chance_of_success = len(soldiers) + len(tanks) + len(planes)
ship_spawn_rate = 4321
spawn_end_time = 20_000
critical_clicks_price = 800
critical_clicks_chance = 100
logistic_enhancement_price = 3000
heal_price = 1750
moving = False
available_to_buy = True
enhancement_active = False
multiplier_active = False
shipping = False

#load sounds
click = pygame.mixer.Sound('assets/sounds/click.ogg')
select_ = pygame.mixer.Sound('assets/sounds/select.ogg')
upgrade = pygame.mixer.Sound('assets/sounds/upgrade.ogg')
money_click = pygame.mixer.Sound('assets/sounds/money_click.ogg')
downgrade = pygame.mixer.Sound('assets/sounds/downgrade.ogg')
success = pygame.mixer.Sound('assets/sounds/success.ogg')
swoosh = pygame.mixer.Sound('assets/sounds/swoosh.ogg')
swoosh_back = pygame.mixer.Sound('assets/sounds/swoosh2.ogg')
pygame.mixer.set_num_channels(8)
#load images

settings_ = pygame.image.load('assets/button_images/settings_icon.png').convert_alpha()
settings_ = pygame.transform.scale(settings_, (40,40))
menu_bg = pygame.image.load("assets/Menu.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
game_bg = pygame.image.load("assets/Game.png").convert()
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))
credits_bg = pygame.image.load('assets/credits.png').convert()
credits_bg = pygame.transform.scale(credits_bg, (WIDTH, HEIGHT))
money_buttoN = pygame.image.load('assets/button_images/Money.png').convert()
money_buttoN = pygame.transform.scale(money_buttoN, (350, 350))
money_buttoN_pressed = pygame.image.load('assets/button_images/Money_pressed.png').convert()
money_buttoN_pressed = pygame.transform.scale(money_buttoN_pressed, (350, 350))
flag1 = pygame.image.load('assets/flags/flag1.png').convert_alpha()
flag1 = pygame.transform.scale(flag1, (500, 350))
flag2 = pygame.image.load('assets/flags/flag2.png').convert_alpha()
flag2 = pygame.transform.scale(flag2, (500, 350))
flag3 = pygame.image.load('assets/flags/flag3.png').convert_alpha()
flag3 = pygame.transform.scale(flag3, (500, 350))
flag5 = pygame.image.load('assets/flags/flag5.png').convert_alpha()
flag5 = pygame.transform.scale(flag5, (500, 350))
flag6 = pygame.image.load('assets/flags/flag6.png').convert_alpha()
flag6 = pygame.transform.scale(flag6, (500, 350))
flag7 = pygame.image.load('assets/flags/flag7.png').convert_alpha()
flag7 = pygame.transform.scale(flag7, (500, 350))
flag8 = pygame.image.load('assets/flags/flag8.png').convert_alpha()
flag8 = pygame.transform.scale(flag8, (500, 350))
flag9 = pygame.image.load('assets/flags/flag9.png').convert_alpha()
flag9 = pygame.transform.scale(flag9, (500, 350))
flag10 = pygame.image.load('assets/flags/flag10.png').convert_alpha()
flag10 = pygame.transform.scale(flag10, (500, 350))
flag11 = pygame.image.load('assets/flags/flag11.png').convert_alpha()
flag11 = pygame.transform.scale(flag11, (500, 350))
flag12 = pygame.image.load('assets/flags/flag12.png').convert_alpha()
flag12 = pygame.transform.scale(flag12, (500, 350))
flag13 = pygame.image.load('assets/flags/flag13.png').convert_alpha()
flag13 = pygame.transform.scale(flag13, (500, 350))
flag14 = pygame.image.load('assets/flags/flag14.png').convert_alpha()
flag14 = pygame.transform.scale(flag14, (500, 350))
flag15 = pygame.image.load('assets/flags/flag15.png').convert_alpha()
flag15 = pygame.transform.scale(flag15, (500, 350))
ship = pygame.image.load('assets/button_images/Ship.png').convert_alpha()
ship = pygame.transform.scale(ship, (300, 200))
wood = pygame.image.load('assets/button_images/wood.png').convert()
wood = pygame.transform.scale(wood, (330, 630))
military_ = pygame.image.load('assets/button_images/Military.png').convert_alpha()
military_ = pygame.transform.scale(military_, (400,280))
soldier1_ = pygame.image.load('assets/button_images/soldier1.jpeg').convert_alpha()
soldier1_ = pygame.transform.scale(soldier1_, (8,16))
soldier2_ = pygame.image.load('assets/button_images/soldier2.jpg').convert_alpha()
soldier2_ = pygame.transform.scale(soldier2_, (8,16))
tank_ = pygame.image.load('assets/button_images/tank.png').convert_alpha()
tank_ = pygame.transform.scale(tank_, (50,50))
plane_ = pygame.image.load('assets/button_images/plane.png').convert_alpha()
plane_ = pygame.transform.scale(plane_, (80, 80))
island_img = pygame.image.load('assets/button_images/island.png').convert_alpha()
island_img = pygame.transform.scale(island_img, (400, 450))
flags = [flag1,flag2,flag3,flag5,flag6,flag7,flag8,flag9,flag10,flag11,flag12,flag13,flag14,flag15]
current_flag = flags[0]
i = 0
#buttons for menu and credits
start_button = Button(pygame.Rect(0, 0, 200, 100), 'START', text_color=(0, 255, 0))
start_button.rect.centerx = WIDTH // 2
start_button.rect.centery = 480
credits_button = Button(pygame.Rect(600, 540, 150, 80), 'CREDITS', text_color=(0,0,0))
X_button = Button(pygame.Rect(0,0,100,100), "X", text_color=(0,0,0))
X_button.rect.centerx = WIDTH - 100
X_button.rect.centery = HEIGHT - 650
import_button = Button(pygame.Rect(440, 540, 150, 80), text=['IMPORT', 'SAVE'])

#game buttons
money_button = Button(pygame.Rect(10, 120, 350, 350), image=money_buttoN, pressed_image=money_buttoN_pressed, action = add_money, text='Click for money!', text_color=(255,255,255))
money_knowing = Button(pygame.Rect(10,10, 350, 100), text=[f'You have ${money:.0f}', f'Money Per Tick: ${money_per_second}'],text_color=(0,0,0), pressed_text_color=(0,0,0), border_radius=0)
name_of_country = Button(pygame.Rect(10,485,350,75),text = f'Country: {country_name}', text_color= (0,0,0), pressed_text_color=(0,0,0), border_radius=0)
upgrade1 = Button(pygame.Rect(890, 250, 300, 75), text=['Upgrade Money Per Click', f'(Price = ${upgrade_money_price})'], text_color=(0,0,0), action=more_money_when_clicked)
upgrade2 = Button(pygame.Rect(890, 420, 300, 75), text=['Upgrade Money Per Tick', f'(Price = ${upgrade_money_per_second_price})'], text_color=(0,0,0), action = upgrade_money_per_second)
upgrade3 = Button(pygame.Rect(890, 505, 300, 75), text =[' Reduce Tick Speed ', f'(Price = ${upgrade_tick_speed_price})'], text_color=(0,0,0), action = increase_tick_speed)
upgrade4 = Button(pygame.Rect(890, 590, 300, 75), text=['Multiply Money Per Tick', f'(30 seconds | Price = ${per_tick_efficiency_upgrade})'], text_color=(0,0,0), action=multiply_efficiency)
upgrade5 = Button(pygame.Rect(890, 335, 300, 75), text=['Upgrade CritClick Chance', f'(Price = ${critical_clicks_price})'], text_color=(0,0,0), action=increase_crit_chance)
upgrade6 = Button(pygame.Rect(890, 250, 300, 75), text=['Hire Infantry Soldier', f'(Price = ${soldier_price})'], text_color=(0,0,0), action=add_soldier)
upgrade7 = Button(pygame.Rect(890, 335, 300, 75), text=['Purchase Infantry Tank', f'(Price = ${tank_price})'], text_color=(0,0,0), action=add_tank)
upgrade8 = Button(pygame.Rect(890, 420, 300, 75), text=['Purchase Fighter Jet', f'(Price = ${plane_price})'], text_color=(0,0,0), action=add_plane)
upgrade9 = Button(pygame.Rect(890, 505, 300, 75), text=['Heal Military Units', f'(Price = ${heal_price})'], text_color=(0,0,0), action=heal_units)
upgrade10 = Button(pygame.Rect(890, 590, 300, 75), text=['Enhance Logistics', f'30 Seconds | (Price = ${logistic_enhancement_price})'], action=enhance_logistics)
down_arrow = Button(pygame.Rect(890, 675, 300, 75), text=[' PRESS TO GO TO  ','MILITARY UPGRADES'], text_color=(0,255,0), action=change_screen)
up_arrow = Button(pygame.Rect(890, 675, 300, 75), text=['PRESS TO GO TO','MONEY UPGRADES'], text_color=(0,255,0), action=change_screen2)
the_thing = Button(pygame.Rect(890, 140, 300, 100), text = 'UPGRADES SHOP!', text_color=(0,0,0), pressed_text_color=(0,0,0), border_radius=0)
ascend_button = Button(pygame.Rect(890, 10, 300, 100), text=['ASCEND', f'{ascend_miles}mi Coastline Required'], text_color=(160, 32, 240), pressed_text_color=(140, 0, 195))
black_line1 = Button(pygame.Rect(870, 120, 400, 5), color=(0,0,0))
black_line2 = Button(pygame.Rect(870, 120, 5, 700), color = (0,0,0))
tick_speed_knowing = Button(pygame.Rect(135, 80, 100, 20), text = f'Tick speed = {tick_speed}ms', text_color=(0,0,0), pressed_text_color=(0,0,0))
settings_button = Button(pygame.Rect(6, 8, 40, 40), image=settings_, pressed_image=settings_, action=settings, border_width=3, border_color=(0,0,0), color=(255,255,255))
send_expedition = Button(pygame.Rect(415, 640, 400, 100), text=['Send Expedition!', f'Chance of Success: {chance_of_success}%'], text_color=(0,0,0), action=send_an_expedition)
coast_knowing = Button(pygame.Rect(415, 10, 400, 100), text=f'Coastline: {coast_mi}mi',text_color=(0,0,0), border_radius=0, pressed_text_color=(0,0,0))
wood_ = Button(pygame.Rect(870,120,330,630), image=wood, pressed_image=wood)
military = Button(pygame.Rect(415, 350, 400, 280), image=military_, pressed_image=military_, border_color=(0,0,0), border_width=3, border_radius=0)
island_border = Button(pygame.Rect(415, 120, 400, 220), border_color=(0,0,0), border_width=3, border_radius=0, color=None)
island = Button(pygame.Rect(415, 5, 400, 220), image=island_img, pressed_image=island_img, border_color=(0,0,0), border_width=0, border_radius=0)
game_buttons = [money_button, money_knowing, name_of_country, ascend_button, black_line1, black_line2, the_thing, tick_speed_knowing, send_expedition, coast_knowing, military, island, island_border, settings_button]
upgrade_screen1_buttons = [upgrade1, upgrade2, upgrade3, upgrade4, upgrade5, down_arrow]
upgrade_screen2_buttons = [up_arrow, upgrade6, upgrade7, upgrade8, upgrade9, upgrade10]
ship_ = Button(pygame.Rect(0,900,300,200), image=ship, color=None, text='Click me!', text_color=(0,0,0), action=random_event)

#country buttons
more = Button(pygame.Rect(925, 225, 100, 100), text=">", text_color=(0,255,0), action=change_flag_up, pressed_text_color=(200,200,200))
less = Button(pygame.Rect(175, 225, 100, 100), text="<", text_color=(200,200,200), action=change_flag_down, pressed_text_color=(200,200,200))
select = Button(pygame.Rect(0,500, 200, 125), text='SELECT', text_color=(0,255,0))
flag = Button(pygame.Rect(0,100,250,250), image=current_flag, pressed_image=flag1)
choose = Button(pygame.Rect(0,25,500,50), text="Choose your country's flag!", text_color=(0,0,0), pressed_text_color=(0,0,0))
select.rect.centerx = WIDTH // 2
flag.rect.centerx = WIDTH // 2 - 125
choose.rect.centerx = WIDTH // 2
country_buttons = [more, less]

#more game buttons (cause why not)
white = Button(pygame.Rect(10, 540, 350, 200), border_radius=0)
flag_panel = Button(pygame.Rect(60, 542, 275, 175))
flag_panel.image = pygame.transform.scale(flag.image, (250, 175))
flag_panel.pressed_image = pygame.transform.scale(flag.image, (250, 175))

#settings screen buttons
tar_and_feather = Button(pygame.Rect(-50,-50,1300,800), color=(0,0,0,150))
export_button = Button(pygame.Rect(475, 250, 300, 100), text='Export Save', action=export_save)
main_menu_button = Button(pygame.Rect(475, 360, 300, 100), text='Exit Game', action=main_menu)
settings_text = Button(pygame.Rect(375, 150, 500, 100), text='Settings', text_color=(255,255,255), pressed_text_color=(255,255,255), color=None)
x_button = Button(pygame.Rect(1110, 20, 70, 70), text='X',action=do)
x_button3 = Button(pygame.Rect(815, 250, 50, 50), text="X", border_color=(0,0,0), border_radius=0, border_width=3)
settings_buttons = [tar_and_feather, export_button, main_menu_button, settings_text, x_button]

stats = {
    'clicks' : clicks,
    'money' : money,
    'soldiers' : len(expedition['soldiers']),
    'tanks' : len(expedition['tanks']),
    'planes' : len(expedition['planes']),
    'coast' : coast_mi
}

async def main():
    bg_msc = pygame.mixer.Sound('assets/sounds/bg_msc.ogg')
    music_playing = False
    global current_screen, current_upgrade_screen, current_flag, i, money, clicks
    global money_per_second, base_money_per_second, multiplier, multiplier_active, multiplier_end_time
    global money_per_click, upgrade_money_price, x, tick_speed, upgrade_tick_speed_price
    global upgrade_money_per_second_price, per_tick_efficiency_upgrade, critical_clicks_price, critical_clicks_chance
    global soldier_price, tank_price, plane_price, expedition_power, chance_of_success, logistic_enhancement_price
    global shipping, moving, available_to_buy, last_money_tick, coast_mi, enhancement_active, reducer, reducer_end_time
    global SETTINGS, running
    running = True
    while running:
        for event in pygame.event.get():
            if not music_playing:
                if any(pygame.mouse.get_pressed()) or any(pygame.key.get_pressed()):
                    bg_msc.play(-1)
                    music_playing = True
            if event.type == pygame.QUIT:
                running = False
            if current_screen == MENU:
                if start_button.handle_event(event):
                    select_.play()
                    if go_to_flag:
                        current_screen = COUNTRY
                    else:
                        current_screen = GAME
                if credits_button.handle_event(event):
                    current_screen = CREDITS
                if import_button.handle_event(event):
                    handle_instant_import()
                if x_button3.handle_event(event):
                    bannerbegone()
            elif current_screen == GAME:
                for button in game_buttons:
                    button.handle_event(event)
                if current_upgrade_screen == UPGRADE1:
                    for button in upgrade_screen1_buttons:
                        button.handle_event(event)
                elif current_upgrade_screen == UPGRADE2:
                    for button in upgrade_screen2_buttons:
                        button.handle_event(event)
                if SETTINGS:
                    for button in settings_buttons:
                        button.handle_event(event)
                if x_button3.handle_event(event):
                    SETTINGS = False
                    bannerbegone()
            elif current_screen == CREDITS:
                if X_button.handle_event(event):
                    current_screen = MENU
            elif current_screen == COUNTRY:
                if select.handle_event(event):
                    select_.play()
                    current_screen = GAME
                    flag.image = current_flag
                    flag_panel.image = pygame.transform.scale(current_flag, (250, 175))
                    flag_panel.pressed_image = flag_panel.image
                for button in country_buttons:
                    button.handle_event(event)
        if current_screen == MENU:
            SETTINGS = False
            screen.blit(menu_bg, (0,0))
            start_button.draw(screen, font)
            import_button.draw(screen, get_font_for_button(import_button))
            credits_button.draw(screen, get_font_for_button(credits_button))
            if show_banner and banner is not None:
                tar_and_feather.draw(screen,font)
                banner.draw(screen, get_font_for_button(banner))
                x_button3.draw(screen, font2)
        elif current_screen == GAME:
            screen.blit(game_bg, (0,0))
            wood_.draw(screen, get_font_for_button(wood_))
            stats['clicks'] = clicks
            stats['money'] = money
            stats['soldiers'] = len(expedition['soldiers']) or len(soldiers)
            stats['tanks'] = len(expedition['tanks']) or len(tanks)
            stats['planes'] = len(expedition['planes']) or len(planes)
            stats['coast'] = coast_mi
            for achievement in achievements.values():
                if not achievement.met and achievement.check(stats[achievement.stat]) and achievement.name not in met_achievements:
                    achievement.met = True
                    achievement_queue.append(achievement)
                    met_achievements.append(achievement.name)
                    achievement.triggered_time = pygame.time.get_ticks()
            global current_popup
            if current_popup is None and len(achievement_queue) > 0:
                achievement_queue.sort(key = lambda it: it.criterion)
                next_ach = achievement_queue.pop(0)
                swoosh.play()
                current_popup = show_achievement(next_ach.name, next_ach.description)
            if expedition["state"] == "going":
                done = True
                for ss, _, _ in expedition["soldiers"]:
                    if ss.rect.y > 350:
                        ss.rect.y -= random.randint(1, 3)
                        done = False
                    else:
                        ss.visible = False
                for tt, _, _ in expedition["tanks"]:
                    if tt.rect.y > 350:
                        tt.rect.y -= random.randint(3, 6)
                        done = False
                    else:
                        tt.visible = False
                for pp, _, _ in expedition["planes"]:
                    if pp.rect.y > 350:
                        pp.rect.y -= random.randint(5, 9)
                        done = False
                    else:
                        pp.visible = False
                if done:
                    expedition['state'] = 'returning'
            elif expedition["state"] == "returning":
                done = True
                for ss, orig_x, orig_y in expedition["soldiers"]:
                    if ss.rect.y < orig_y:
                        ss.rect.y += 2
                        done = False
                    else:
                        ss.visible = True
                        ss.rect.x = orig_x
                        ss.rect.y = orig_y
                for tt, orig_x, orig_y in expedition["tanks"]:
                    if tt.rect.y < orig_y:
                        tt.rect.y += 3
                        done = False
                    else:
                        tt.visible = True
                        tt.rect.x = orig_x
                        tt.rect.y = orig_y
                for pp, orig_x, orig_y in expedition["planes"]:
                    if pp.rect.y < orig_y:
                        pp.rect.y += 4
                        done = False
                    else:
                        pp.visible = True
                        pp.rect.x = orig_x
                        pp.rect.y = orig_y
                if done:
                    expedition_it()

                    soldiers.extend([s[0] for s in expedition["soldiers"]])
                    tanks.extend([t[0] for t in expedition["tanks"]])
                    planes.extend([p[0] for p in expedition["planes"]])
                    expedition["soldiers"].clear()
                    expedition["tanks"].clear()
                    expedition["planes"].clear()
                    expedition["state"] = "idle"
                    moving = False
                    available_to_buy = True
            if money_per_click < 10:
                check_money(upgrade1, upgrade_money_price)
            check_money(upgrade2, upgrade_money_per_second_price)
            check_money(upgrade3, upgrade_tick_speed_price)
            check_money(upgrade4, per_tick_efficiency_upgrade)
            check_money(upgrade6, soldier_price)
            check_money(upgrade7, tank_price)
            check_money(upgrade8, plane_price)
            check_money(upgrade9, heal_price)
            if enhancement_active is False:
                check_money(upgrade10, logistic_enhancement_price)
            check_expedition()
            if critical_clicks_chance > 10:
                check_money(upgrade5, critical_clicks_price)
            else:
                upgrade5.text[1] = 'MAX LEVEL'
                upgrade5.color = (200, 200, 200)
                upgrade5.pressed_text_color = (0, 0, 0)
                critical_clicks_price = 99999999999
            check_ascend(ascend_button)
            money_per_second = int(base_money_per_second * multiplier)
            now = pygame.time.get_ticks()
            if money_per_second > 0 and now - last_money_tick >= tick_speed:
                add_money_per_second()
                last_money_tick = now
            if multiplier_active and now >= multiplier_end_time:
                multiplier = 1.0
                multiplier_active = False
                upgrade4.text = ['Multiply Money Per Tick', f'(30 seconds | Price = ${per_tick_efficiency_upgrade:.0f})']
            elif multiplier_active and now < multiplier_end_time or money_per_second < 1:
                upgrade4.color = (200,200,200)
                upgrade4.pressed_text_color = (0,0,0)
            if enhancement_active and now >= reducer_end_time:
                reducer = 2
                reducer_end_time = 0
                soldier_price = soldier_price * reducer
                tank_price = tank_price * reducer
                plane_price = plane_price * reducer
                upgrade6.text[1] = f'(Price = ${soldier_price:.0f})'
                upgrade7.text[1] = f'(Price = ${tank_price:.0f})'
                upgrade8.text[1] = f'(Price = ${plane_price:.0f})'
                upgrade10.text[1] = f'30 Seconds | (Price = ${logistic_enhancement_price:.0f})'
                upgrade10.color = (255, 255, 255)
                upgrade10.pressed_text_color = (200, 200, 200)
                enhancement_active = False
            elif enhancement_active and now < reducer_end_time:
                upgrade10.color = (200,200,200)
                upgrade10.pressed_text_color = (0,0,0)
            white.draw(screen, get_font_for_button(white))
            for button in game_buttons:
                if button == tick_speed_knowing:
                    button.draw(screen, get_font_for_button(button))
                else:
                    button.draw(screen, get_font_for_button(button))
            for ss in soldiers:
                if ss.visible and ss.rect.y < 395:
                    ss.draw(screen, font)
                chance_of_success = round(expedition_power, 1)
                send_expedition.text = ['Send Expedition!', f'Chance of Success: {chance_of_success:.2f}%']
            for tt in tanks:
                if tt.visible and tt.rect.y < 470:
                    tt.draw(screen, font)
                chance_of_success = round(expedition_power, 1)
                send_expedition.text = ['Send Expedition!', f'Chance of Success: {chance_of_success:.2f}%']
            for pp in planes:
                if pp.visible and pp.rect.y < 590:
                    pp.draw(screen, font)
                chance_of_success = round(expedition_power, 1)
                send_expedition.text = ['Send Expedition!', f'Chance of Success: {chance_of_success:.2f}%']
            mouse_pos_ = pygame.mouse.get_pos()
            for soldier in soldiers:
                if soldier.rect.collidepoint(mouse_pos_) and soldier.rect.y < 395:
                    name_surf = font6.render(soldier.name, False, (255,255,255))
                    name_rect = name_surf.get_rect(midbottom=(soldier.rect.centerx, soldier.rect.top - 2))
                    screen.blit(name_surf, name_rect)
            for tank in tanks:
                if tank.rect.collidepoint(mouse_pos_) and tank.rect.y < 470:
                    name_surfer = font6.render(tank.name, False, (255,255,255))
                    name_recter = name_surfer.get_rect(midbottom=(tank.rect.centerx, tank.rect.top + 4))
                    screen.blit(name_surfer, name_recter)
            for plane in planes:
                if plane.rect.collidepoint(mouse_pos_) and plane.rect.y < 590:
                    name_surferer = font6.render(plane.name, False, (255,255,255))
                    name_recterer = name_surferer.get_rect(midbottom=(plane.rect.centerx, plane.rect.top + 8))
                    screen.blit(name_surferer, name_recterer)
            if current_upgrade_screen == UPGRADE1:
                for button in upgrade_screen1_buttons:
                    button.draw(screen, get_font_for_button(button))
            elif current_upgrade_screen == UPGRADE2:
                for button in upgrade_screen2_buttons:
                    button.draw(screen, get_font_for_button(button))
            flag_panel.draw(screen, get_font_for_button(flag_panel))
            for ss, _, _ in expedition["soldiers"]:
                if ss.visible and ss.rect.y < 590:
                    ss.draw(screen, font)

            for tt, _, _ in expedition["tanks"]:
                if tt.visible and tt.rect.y < 590:
                    tt.draw(screen, font)

            for pp, _, _ in expedition["planes"]:
                if pp.visible and pp.rect.y < 570:
                    pp.draw(screen, font)

            for ft in floating_texts[:]:
                ft['y'] = ft['y'] - 1
                text_surface = font3.render(ft['text'], True, (255, 255, 255))
                screen.blit(text_surface, (ft['x'], ft['y']))
                ft['timer'] = ft['timer'] - 1
                if ft['timer'] <= 0:
                    floating_texts.remove(ft)
            for ft2 in floating_texts2[:]:
                ft2['y'] = ft2['y'] - 1
                text_surface = font3.render(ft2['text'], True, (0, 0, 0))
                screen.blit(text_surface, (ft2['x'], ft2['y']))
                ft2['timer'] = ft2['timer'] - 1
                if ft2['timer'] <= 0:
                    floating_texts2.remove(ft2)
            if current_popup:
                alive = current_popup.update()
                current_popup.draw_it(screen)
                if not alive:
                    swoosh_back.play()
                    current_popup = None
            if shipping is False:
                global ship_spawn_rate
                if random.randint(1, ship_spawn_rate) == 1:
                    ship_.rect.y = random.randint(450, 580)
                    ship_.rect.x = -100
                    ship_.rect.width = 300
                    ship_.rect.height = 200
                    ship_spawn_rate = 4321
                    shipping = True
            if shipping is True:
                move(ship_)
                if ship_.rect.x > 10:
                    ship_.draw(screen, get_font_for_button(ship_))
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    if ship_.rect.collidepoint(mouse_pos):
                        ship_.rect.width = 0
                        ship_.rect.height = 0
                        shipping = False
                        ship_.action()
                if ship_.rect.x > WIDTH:
                    shipping = False
                    ship_.rect.width = 0
                    ship_.rect.height = 0
            if SETTINGS:
                for button in settings_buttons:
                    button.draw(screen, get_font_for_button(button))
            if show_banner and banner is not None:
                tar_and_feather.draw(screen,font)
                banner.draw(screen, get_font_for_button(banner))
                x_button3.draw(screen, font2)
        elif current_screen == CREDITS:
            screen.blit(credits_bg, (0,0))
            X_button.draw(screen, font4)
        elif current_screen == COUNTRY:
            screen.blit(game_bg, (0,0))
            select.draw(screen, font)
            choose.draw(screen, font3)
            flag.image = current_flag
            flag.draw(screen, get_font_for_button(flag))
            for button in country_buttons:
                button.draw(screen, font4)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit()
asyncio.run(main())