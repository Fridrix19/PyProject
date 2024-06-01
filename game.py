import arcade
import math
import time
import os
import subprocess

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Защитники леса"
PROJECTILE_SPEED = 10  
MOB_SPEED = 0.5  
MOB_SPEED_2 = 1.0  
MOB_SPEED_3 = 1.5  
TOWER_HP = 100
MOB_HP = 100
WAVE_DELAY = 8  
SPAWN_INTERVAL = 3  
DETECTION_RADIUS = 1000 
PROJECTILE_DAMAGE = 50  
UPGRADED_PROJECTILE_DAMAGE = 100  
UPGRADE_COST = 3  
POTION_DAMAGE_MULTIPLIER = 3  

level1_completed = False

def check_file_path(path):
    if not os.path.isfile(path):
        print(f"Файл не найден: {path}")
        return False
    return True


tower_image = "C:/Users/Fridrix/Desktop/PyProject/img/tower/tower.png"
tower2_image = "C:/Users/Fridrix/Desktop/PyProject/img/tower/tower2.png"
tower3_image = "C:/Users/Fridrix/Desktop/PyProject/img/tower/tower3.png"
enemy_image = "C:/Users/Fridrix/Desktop/PyProject/img/p1.png"
slime_images = [
    "C:/Users/Fridrix/Desktop/PyProject/img/slime.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/slime1.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/slime2.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/slime3.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/slime4.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/slime5.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/slime6.png",
]
boss_hp_images = [
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp1.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp2.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp3.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp4.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp5.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp6.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp7.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp8.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp9.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp10.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/bossHP/hp11.png"
]

projectile_image = "C:/Users/Fridrix/Desktop/PyProject/img/ball.png"
heart_image = "C:/Users/Fridrix/Desktop/PyProject/img/money.png"
background_image = "C:/Users/Fridrix/Desktop/PyProject/img/back.png"
tower_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/p3.png"
upgrade_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/up.png"
menu_background_image = "C:/Users/Fridrix/Desktop/PyProject/img/back.gif"
logo_image = "C:/Users/Fridrix/Desktop/PyProject/img/Logo.png"
play_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/play.png"
exit_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/exit.png"
level1_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/1.png"
dialogue_box_image = "C:/Users/Fridrix/Desktop/PyProject/img/mag.png"
continue_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/cont.png"
arrow_image = "C:/Users/Fridrix/Desktop/PyProject/img/arow.png"
return_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/return.png"
font_path = "C:/Users/Fridrix/Desktop/PyProject/fonts/pixel.ttf"
music_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/music.mp3"
hover_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/hover.mp3"
click_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/klik.mp3"
main_theme_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/main_them.mp3"
fireball_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/fireball.mp3"
slap_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/slap.mp3"
kill_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/kill.mp3"
upgrade_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/up.mp3"
final_upgrade_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/final.mp3"


required_files = [
    tower_image, tower2_image, tower3_image, enemy_image, slime_images[0], projectile_image, heart_image,
    background_image, tower_button_image, upgrade_button_image, menu_background_image,
    logo_image, play_button_image, exit_button_image, level1_button_image, dialogue_box_image, continue_button_image,
    arrow_image, font_path, music_sound, hover_sound, click_sound, main_theme_sound,
    fireball_sound, slap_sound, kill_sound, upgrade_sound, final_upgrade_sound
]

for file in required_files:
    if isinstance(file, list):
        for f in file:
            if not check_file_path(f):
                raise FileNotFoundError(f"Cannot locate resource: {f}")
    else:
        if not check_file_path(file):
            raise FileNotFoundError(f"Cannot locate resource: {file}")

class Heart(arcade.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__(heart_image, scale=0.1)
        self.center_x = position_x
        self.center_y = position_y

class Tower(arcade.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__(tower_image, scale=0.5)
        self.center_x = position_x
        self.center_y = position_y
        self.hp = TOWER_HP
        self.damage = PROJECTILE_DAMAGE
        self.upgraded = False
        self.time_since_last_shot = 0

    def upgrade(self):
        if not self.upgraded:
            self.texture = arcade.load_texture(tower2_image)
            self.damage = UPGRADED_PROJECTILE_DAMAGE
            self.upgraded = True

class Enemy(arcade.Sprite):
    def __init__(self, position_x, position_y, target_x, target_y, speed, texture, hp=MOB_HP):
        super().__init__(texture, scale=0.5)
        self.center_x = position_x
        self.center_y = position_y
        self.hp = hp
        self.total_hp = hp
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed

    def update(self):
        super().update()
        direction = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
        self.center_x += self.speed * math.cos(direction)
        self.center_y += self.speed * math.sin(direction)

    def draw_health_bar(self):
        health_width = 40 * (self.hp / self.total_hp)
        if self.hp > 50:
            arcade.draw_lrtb_rectangle_filled(self.center_x - 20, self.center_x - 20 + health_width, self.center_y + 35, self.center_y + 30, arcade.color.GREEN)
        else:
            arcade.draw_lrtb_rectangle_filled(self.center_x - 20, self.center_x - 20 + health_width, self.center_y + 35, self.center_y + 30, arcade.color.RED)

class Slime(arcade.Sprite):
    def __init__(self, position_x, position_y, target_x, target_y):
        super().__init__(scale=0.25)
        self.texture_paths = slime_images
        self.textures = [arcade.load_texture(path) for path in self.texture_paths]
        self.center_x = position_x
        self.center_y = position_y
        self.hp = MOB_HP * 3  
        self.total_hp = MOB_HP * 3  
        self.target_x = target_x
        self.target_y = target_y
        self.speed = MOB_SPEED_2
        self.cur_texture_index = 0
        self.time_since_last_change = 0

    def update(self):
        super().update()
        self.time_since_last_change += 1
        if self.time_since_last_change >= 10:  #  частотa кадров 
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.texture = self.textures[self.cur_texture_index]
            self.time_since_last_change = 0
        direction = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
        self.center_x += self.speed * math.cos(direction)
        self.center_y += self.speed * math.sin(direction)

    def draw_health_bar(self):
        health_width = 40 * (self.hp / self.total_hp)
        if self.hp > 50:
            arcade.draw_lrtb_rectangle_filled(self.center_x - 20, self.center_x - 20 + health_width, self.center_y + 35, self.center_y + 30, arcade.color.GREEN)
        else:
            arcade.draw_lrtb_rectangle_filled(self.center_x - 20, self.center_x - 20 + health_width, self.center_y + 35, self.center_y + 30, arcade.color.RED)

class Projectile(arcade.Sprite):
    def __init__(self, start_position, target, damage, game):
        super().__init__(scale=0.5)
        self.texture_paths = [
            f"C:/Users/Fridrix/Desktop/PyProject/img/fireball/fireball{i}.png" for i in range(1, 13)
        ]
        self.textures = [arcade.load_texture(path) for path in self.texture_paths]
        self.center_x, self.center_y = start_position
        self.target = target
        self.damage = damage
        self.angle = math.atan2(target.center_y - self.center_y, target.center_x - self.center_x)
        self.game = game  
        self.fire_sound = arcade.load_sound(fireball_sound)
        self.slap_sound = arcade.load_sound(slap_sound)
        self.kill_sound = arcade.load_sound(kill_sound)
        self.cur_texture_index = 0
        self.time_since_last_change = 0

    def update(self):
        self.center_x += PROJECTILE_SPEED * math.cos(self.angle)
        self.center_y += PROJECTILE_SPEED * math.sin(self.angle)
        self.time_since_last_change += 1
        if self.time_since_last_change >= 5: 
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.texture = self.textures[self.cur_texture_index]
            self.time_since_last_change = 0
        if check_collision(self, self.target):
            arcade.play_sound(self.slap_sound, volume=0.3)
            self.target.hp -= self.damage
            if self.target.hp <= 0:
                arcade.play_sound(self.kill_sound, volume=0.3)
                self.game.drop_heart(self.target.center_x, self.target.center_y)
                self.target.kill()
                self.game.on_enemy_killed(self.target)
            self.kill()

    def on_spawn(self):
        arcade.play_sound(self.fire_sound, volume=0.3)


class Game(arcade.View):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.background_image = arcade.load_texture(background_image)
        self.tower_button = arcade.Sprite(tower_button_image, scale=0.5, center_x=950, center_y=50)
        self.upgrade_button = None
        self.tower = None
        self.enemies_list = arcade.SpriteList()
        self.projectiles_list = arcade.SpriteList()
        self.hearts_list = arcade.SpriteList()
        self.wave_in_progress = False
        self.wave_timer = None
        self.spawned_mob_count = 0
        self.next_mob_spawn_time = 0
        self.last_shot_time = 0
        self.music = arcade.load_sound(music_sound)
        self.music_player = None
        self.coin_texture = arcade.load_texture(heart_image)
        self.coins = 0
        self.mob_speed = MOB_SPEED
        self.mob_image = enemy_image
        self.mob_count = 3
        self.dialogue_box = arcade.Sprite(dialogue_box_image, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2)
        self.continue_button = arcade.Sprite(continue_button_image, scale=0.5, center_x=SCREEN_WIDTH // 2 - 200, center_y=SCREEN_HEIGHT // 4 + 50)
        self.dialogue_stage = 0
        self.show_dialogue = True
        self.show_boss_screen = False
        self.dialogue_text = ""
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.dialogue_text_x = self.dialogue_box.center_x - 200
        self.dialogue_text_y = self.dialogue_box.center_y - 335
        self.arrow_visible = False
        self.potion_image = arcade.load_texture("C:/Users/Fridrix/Desktop/PyProject/img/Potion.png")
        self.potion = None
        self.potion_button = None
        self.double_damage = False
        self.heart_pickup_count = 0
        self.upgrade_dialogue_shown = False

        self.dialogue_speed = 0.05  # Скорость  текста 
        self.dialogue_sounds = []  # хранениe звуков 

        self.setup()

    def setup(self):
        self.font_name = arcade.load_font(font_path)
        self.boss_button = None
        self.schedule_dialogue_texts()
        if self.dialogue_texts:
            first_sound_path = self.dialogue_texts[0][1]
            arcade.play_sound(arcade.load_sound(first_sound_path))

    def schedule_dialogue_texts(self):
        self.dialogue_texts = [
            ("УХТЫ! НОВИЧОК!!!!!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/1.mp3"),
            ("Раз уж ты сюда попал", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/2.mp3"),
            ("Значит у нас общие цели.", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/3.mp3"),
            ("Я Хатабыч - твой наставник.", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/4.mp3"),
            ("Для начала тебе нужно:", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/5.mp3"),
            ("Построить твою крепость.", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/6.mp3"),
            ("Нажми на кнопку СПРАВА тебя", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/7.mp3"),
            ("И приступай к обороне!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/8.mp3"),
            ("УДАЧИ!!!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/9.mp3"),
            ("Ах да", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/10.mp3"),
            ("Не забывай собирать сердца", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/11.mp3"),
            ("За них ты будешь улучшаться!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/12.mp3"),
            ("Счетчик сердец справа сверху!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/13.mp3"),
            ("Приступай!!!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/14.mp3"),
        ]

        self.additional_dialogue_texts = [
            ("ЗЕЛЬЕ!!!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/18.mp3"),
            ("ТЕБЕ СРОЧНО НУЖНО ЗЕЛЬЕ!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/19.mp3"),
            ("Слизьням плевать на урон", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/20.mp3"),
            ("ОНИ ТОЛСТЫЕ КАК СВИНЬИ.", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/21.mp3"),
            ("ИСПОЛЬЗУЙ ЗЕЛЬЕ - ПОВЫСЬ УРОН!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/22.mp3"),
        ]

        self.upgrade_dialogue_texts = [
            ("У тебя 3 сердца", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/15.mp3"),
            ("Улучши свою башню!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/16.mp3"),
            ("Кнопка СПРАВА снизу", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/17.mp3"),
        ]

        self.boss_dialogue_texts = [
            ("Азы изучены", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/23.mp3"),
            ("Перейти к следующему уровню", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/24.mp3"),
        ]

        self.dialogue_sounds = [arcade.load_sound(sound_path) for _, sound_path in self.dialogue_texts]

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        if self.tower:
            self.tower.draw()
        self.enemies_list.draw()
        self.projectiles_list.draw()
        self.hearts_list.draw()
        self.tower_button.draw()
        if self.upgrade_button:
            self.upgrade_button.draw()
        if self.potion_button:
            self.potion_button.draw()
            arcade.draw_text("ИСПОЛЬЗОВАТЬ!", 850, 110, arcade.color.WHITE, 14, font_name='Minecraft Rus', anchor_x="center")
        if self.show_boss_screen:
            self.draw_boss_screen()
        if self.show_dialogue:
            self.draw_dialogue()
        for enemy in self.enemies_list:
            enemy.draw_health_bar()
        arcade.draw_texture_rectangle(950, 950, self.coin_texture.width * 0.1, self.coin_texture.height * 0.1, self.coin_texture) #отрисовка сердца
        arcade.draw_text(str(self.coins), 970, 940, arcade.color.WHITE, 14, font_name='Minecraft Rus', anchor_x="left")
        if not self.wave_in_progress and self.wave_timer is not None:
            arcade.draw_text(f"Волна наступает через: {int(self.wave_timer)} секунд", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40, arcade.color.WHITE, 14, font_name='Minecraft Rus', anchor_x="center")

    def draw_dialogue(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 150))
        self.dialogue_box.draw()
        arcade.draw_text(self.dialogue_text, self.dialogue_text_x, self.dialogue_text_y, arcade.color.BLACK, 16, anchor_x="center", font_name='Minecraft Rus')
        if self.dialogue_stage < len(self.dialogue_texts):
            self.continue_button.draw()

    def draw_boss_screen(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 150))
        arcade.draw_text("Азы изучены", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.WHITE, 20, anchor_x="center", font_name='Minecraft Rus')
        arcade.draw_text("Перейти к следующему уровню", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 16, anchor_x="center", font_name='Minecraft Rus')
        if self.boss_button:
            self.boss_button.draw()

    def on_update(self, delta_time):
        if self.show_dialogue:
            self.dialogue_timer += delta_time
            current_speed = self.dialogue_speed
            if self.dialogue_timer > current_speed and self.dialogue_index < len(self.dialogue_texts[self.dialogue_stage][0]):
                self.dialogue_text += self.dialogue_texts[self.dialogue_stage][0][self.dialogue_index]
                self.dialogue_index += 1
                self.dialogue_timer = 0
            elif self.dialogue_index == 0 and self.dialogue_timer == 0:
                sound_path = self.dialogue_texts[self.dialogue_stage][1]
                arcade.play_sound(arcade.load_sound(sound_path))
        else:
            self.enemies_list.update()
            self.projectiles_list.update()
            self.hearts_list.update()
            if self.tower and not self.wave_in_progress and self.wave_timer is not None:
                self.wave_timer -= delta_time
                if self.wave_timer <= 0:
                    self.wave_in_progress = True
                    self.wave_timer = None
                    self.spawned_mob_count = 0
                    self.next_mob_spawn_time = time.time() + SPAWN_INTERVAL
            if self.wave_in_progress and time.time() > self.next_mob_spawn_time:
                if self.spawned_mob_count < self.mob_count:
                    self.spawn_mob()
                    self.spawned_mob_count += 1
                    self.next_mob_spawn_time = time.time() + SPAWN_INTERVAL
            if self.tower and time.time() - self.last_shot_time > 2 and self.wave_in_progress:
                closest_enemy = self.get_closest_enemy(self.tower.center_x, self.tower.center_y)
                if closest_enemy:
                    self.fire_projectile((self.tower.center_x, self.tower.center_y), closest_enemy)
                    self.last_shot_time = time.time()
            if self.tower and len(self.enemies_list) == 0 and len(self.hearts_list) == 0 and not self.wave_in_progress and self.wave_timer is None:
                self.wave_timer = WAVE_DELAY
            if self.tower:
                for heart in self.hearts_list:
                    if check_collision(self.tower, heart):
                        heart.kill()
                        self.coins += 1
                        self.heart_pickup_count += 1
                        if self.heart_pickup_count == 3 and not self.upgrade_dialogue_shown:
                            self.show_upgrade_dialogue()
                        if self.heart_pickup_count == 8:
                            self.show_boss_screen = True
                            self.boss_button = arcade.Sprite("C:/Users/Fridrix/Desktop/PyProject/img/cont.png", scale=0.5, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - 50)
                        if self.coins >= UPGRADE_COST and not self.upgrade_button and not self.tower.upgraded:
                            self.upgrade_button = arcade.Sprite(upgrade_button_image, scale=0.125, center_x=950, center_y=50)
                            self.upgrade_button.alpha = 128

    def show_upgrade_dialogue(self):
        self.show_dialogue = True
        self.dialogue_texts = self.upgrade_dialogue_texts
        self.dialogue_stage = 0
        self.dialogue_text = ""
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.upgrade_dialogue_shown = True
        if self.dialogue_texts:
            first_sound_path = self.dialogue_texts[0][1]
            arcade.play_sound(arcade.load_sound(first_sound_path))

    def on_mouse_press(self, x, y, button, modifiers):
        if self.show_dialogue and self.continue_button.collides_with_point((x, y)):
            self.dialogue_stage += 1
            if self.dialogue_stage >= len(self.dialogue_texts):
                self.show_dialogue = False
                self.schedule_dialogue_texts()
                return
            self.dialogue_text = ""
            self.dialogue_index = 0
            self.dialogue_timer = 0
            sound_path = self.dialogue_texts[self.dialogue_stage][1]
            arcade.play_sound(arcade.load_sound(sound_path))
        elif not self.show_dialogue:
            if not self.tower and self.tower_button.collides_with_point((x, y)):
                self.tower = Tower(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                self.tower_button.kill()
                self.wave_timer = WAVE_DELAY
                self.wave_in_progress = False
                self.music_player = arcade.play_sound(self.music, volume=0.3, looping=True)
            if self.upgrade_button and self.upgrade_button.collides_with_point((x, y)):
                if self.coins >= UPGRADE_COST and not self.tower.upgraded:
                    self.tower.upgrade()
                    arcade.play_sound(arcade.load_sound(upgrade_sound), volume=2)
                    self.upgrade_button.kill()
                    self.upgrade_button = None
                    self.coins -= UPGRADE_COST
                    self.wave_timer = 5
                    self.wave_in_progress = False
                    self.mob_speed = MOB_SPEED_2
                    self.mob_image = slime_images[0]
                    self.mob_count = 5
            if self.potion_button and self.potion_button.collides_with_point((x, y)):
                self.double_damage = True
                self.potion_button.kill()
                self.potion_button = None
            if self.boss_button and self.boss_button.collides_with_point((x, y)):
                self.show_boss_screen = False
                self.start_level_2()
            for heart in self.hearts_list:
                if heart.collides_with_point((x, y)):
                    heart.kill()
                    self.coins += 1
                    self.heart_pickup_count += 1
                    if self.heart_pickup_count == 3 and not self.upgrade_dialogue_shown:
                        self.show_upgrade_dialogue()
                    if self.heart_pickup_count == 8:
                        self.show_boss_screen = True
                        self.boss_button = arcade.Sprite("C:/Users/Fridrix/Desktop/PyProject/img/cont.png", scale=0.5, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - 50)
                    if self.coins >= UPGRADE_COST and not self.upgrade_button and not self.tower.upgraded:
                        self.upgrade_button = arcade.Sprite(upgrade_button_image, scale=0.125, center_x=950, center_y=50)
                        self.upgrade_button.alpha = 128

    def start_level_2(self):
        arcade.close_window()
        subprocess.Popen(["python", "lvl2.py"])

    def spawn_mob(self):
        if self.mob_image in slime_images:
            enemy = Slime(SCREEN_WIDTH / 2, 0, self.tower.center_x, self.tower.center_y)
        else:
            enemy = Enemy(SCREEN_WIDTH / 2, 0, self.tower.center_x, self.tower.center_y, self.mob_speed, self.mob_image)
        self.enemies_list.append(enemy)

    def get_closest_enemy(self, tower_x, tower_y):
        closest_enemy = None
        closest_distance = DETECTION_RADIUS
        for enemy in self.enemies_list:
            distance = math.sqrt((enemy.center_x - tower_x) ** 2 + (enemy.center_y - tower_y) ** 2)
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
        return closest_enemy

    def fire_projectile(self, start_position, target):
        damage = self.tower.damage * POTION_DAMAGE_MULTIPLIER if self.double_damage else self.tower.damage
        projectile = Projectile(start_position, target, damage, self)
        projectile.on_spawn()
        self.projectiles_list.append(projectile)

    def drop_heart(self, x, y):
        heart = Heart(x, y)
        self.hearts_list.append(heart)

    def on_enemy_killed(self, enemy):
        if isinstance(enemy, Slime) and self.potion is None:
            self.show_dialogue = True
            self.dialogue_texts = self.additional_dialogue_texts
            self.dialogue_stage = 0
            self.dialogue_text = ""
            self.dialogue_index = 0
            self.dialogue_timer = 0
            self.potion = arcade.Sprite("C:/Users/Fridrix/Desktop/PyProject/img/Potion.png", scale=0.5)
            self.potion_button = arcade.Sprite("C:/Users/Fridrix/Desktop/PyProject/img/Potion.png", scale=0.125, center_x=850, center_y=150)
            if self.dialogue_texts:
                first_sound_path = self.dialogue_texts[0][1]
                arcade.play_sound(arcade.load_sound(first_sound_path))
        elif isinstance(enemy, Slime) and len([e for e in self.enemies_list if isinstance(e, Slime)]) == 0:
            self.double_damage = False

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(menu_background_image)
        self.logo = arcade.load_texture(logo_image)
        self.play_button = arcade.load_texture(play_button_image)
        self.exit_button = arcade.load_texture(exit_button_image)
        self.background_music = arcade.load_sound(main_theme_sound)
        self.hover_sound = arcade.load_sound(hover_sound)
        self.click_sound = arcade.load_sound(click_sound)
        self.background_music_player = arcade.play_sound(self.background_music, volume=0.3, looping=True)
        self.hovered_button = None

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        logo_x = SCREEN_WIDTH / 2
        logo_y = SCREEN_HEIGHT - 200
        arcade.draw_texture_rectangle(logo_x, logo_y, self.logo.width, self.logo.height, self.logo)
        play_x = SCREEN_WIDTH / 2
        play_y = SCREEN_HEIGHT / 2
        arcade.draw_texture_rectangle(play_x, play_y, self.play_button.width, self.play_button.height, self.play_button)
        exit_x = SCREEN_WIDTH / 2
        exit_y = play_y - 100
        arcade.draw_texture_rectangle(exit_x, exit_y, self.exit_button.width, self.exit_button.height, self.exit_button)

    def on_mouse_motion(self, x, y, dx, dy):
        play_x, play_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        exit_x, exit_y = SCREEN_WIDTH / 2, play_y - 100
        if play_x - self.play_button.width / 2 < x < play_x + self.play_button.width / 2 and \
           play_y - self.play_button.height / 2 < y < play_y + self.play_button.height / 2:
            if self.hovered_button != 'play':
                arcade.play_sound(self.hover_sound, volume=0.3)
                self.hovered_button = 'play'
        elif exit_x - self.exit_button.width / 2 < x < exit_x + self.exit_button.width / 2 and \
             exit_y - self.exit_button.height / 2 < y < exit_y + self.exit_button.height / 2:
            if self.hovered_button != 'exit':
                arcade.play_sound(self.hover_sound, volume=0.3)
                self.hovered_button = 'exit'
        else:
            self.hovered_button = None

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            play_x, play_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            exit_x, exit_y = SCREEN_WIDTH / 2, play_y - 100
            if play_x - self.play_button.width / 2 < x < play_x + self.play_button.width / 2 and \
               play_y - self.play_button.height / 2 < y < play_y + self.play_button.height / 2:
                arcade.play_sound(self.click_sound, volume=0.3)
                level_menu_view = LevelMenuView(self.background_music_player)
                self.window.show_view(level_menu_view)
            elif exit_x - self.exit_button.width / 2 < x < exit_x + self.exit_button.width / 2 and \
                 exit_y - self.exit_button.height / 2 < y < exit_y + self.exit_button.height / 2:
                arcade.play_sound(self.click_sound, volume=0.3)
                arcade.close_window()

class LevelMenuView(arcade.View):
    def __init__(self, background_music_player):
        super().__init__()
        self.background = arcade.load_texture(menu_background_image)
        self.logo = arcade.load_texture(logo_image)
        self.level1_button = arcade.load_texture(level1_button_image)
        self.hover_sound = arcade.load_sound(hover_sound)
        self.click_sound = arcade.load_sound(click_sound)
        self.hovered_button = None
        self.background_music_player = background_music_player
        self.level1_completed = level1_completed

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        logo_x = SCREEN_WIDTH / 2
        logo_y = SCREEN_HEIGHT - 200
        arcade.draw_texture_rectangle(logo_x, logo_y, self.logo.width, self.logo.height, self.logo)
        level1_x = SCREEN_WIDTH / 2 - 100
        level1_y = SCREEN_HEIGHT / 2
        arcade.draw_texture_rectangle(level1_x, level1_y, self.level1_button.width, self.level1_button.height, self.level1_button)

    def on_mouse_motion(self, x, y, dx, dy):
        level1_x, level1_y = SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2
        if level1_x - self.level1_button.width / 2 < x < level1_x + self.level1_button.width / 2 and \
           level1_y - self.level1_button.height / 2 < y < level1_y + self.level1_button.height / 2:
            if self.hovered_button != 'level1':
                arcade.play_sound(self.hover_sound, volume=0.3)
                self.hovered_button = 'level1'
        else:
            self.hovered_button = None

    def on_mouse_press(self, x, y, button, modifiers):
        level1_x, level1_y = SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2
        if level1_x - self.level1_button.width / 2 < x < level1_x + self.level1_button.width / 2 and \
           level1_y - self.level1_button.height / 2 < y < level1_y + self.level1_button.height / 2:
            arcade.play_sound(self.click_sound, volume=0.3)
            arcade.stop_sound(self.background_music_player)
            game_view = Game(level=1)
            game_view.setup()
            self.window.show_view(game_view)

def get_bounding_box(sprite):
    left = sprite.center_x - sprite.width / 2
    right = sprite.center_x + sprite.width / 2
    bottom = sprite.center_y - sprite.height / 2
    top = sprite.center_y + sprite.height / 2
    return left, right, bottom, top

def check_collision(sprite1, sprite2):
    left1, right1, bottom1, top1 = get_bounding_box(sprite1)
    left2, right2, bottom2, top2 = get_bounding_box(sprite2)
    
    if right1 < left2 or right2 < left1 or top1 < bottom2 or top2 < bottom1:
        return False
    return True

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
