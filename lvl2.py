import arcade
import math
import os

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Уровень 2: Защитники леса"
PROJECTILE_SPEED = 10  
PROJECTILE_DAMAGE = 1  
BOSS_HP = 11  
TOWER_FIRE_RATE = 1.0  
BOSS_SPEED = 1  


background_image = "C:/Users/Fridrix/Desktop/PyProject/img/back.png"
tower_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/p3.png"
tower_image = "C:/Users/Fridrix/Desktop/PyProject/img/tower/tower3.png"
boss_images = [
    "C:/Users/Fridrix/Desktop/PyProject/img/boss/boss-0001.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/boss/boss-0002.png",
    "C:/Users/Fridrix/Desktop/PyProject/img/boss/boss-0003.png"
]
dialogue_box_image = "C:/Users/Fridrix/Desktop/PyProject/img/mag.png"
continue_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/cont.png"
font_path = "C:/Users/Fridrix/Desktop/PyProject/fonts/pixel.ttf"
return_button_image = "C:/Users/Fridrix/Desktop/PyProject/img/exit.png"

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

projectile_images = [
    f"C:/Users/Fridrix/Desktop/PyProject/img/fireball/fireball{i}.png" for i in range(1, 13)
]
fireball_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/fireball.mp3"
slap_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/slap.mp3"
kill_sound = "C:/Users/Fridrix/Desktop/PyProject/sound/kill.mp3"
song_path = "C:/Users/Fridrix/Desktop/PyProject/sound/oleg.mp3"  

class Tower(arcade.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__(tower_image, scale=0.5)
        self.center_x = position_x
        self.center_y = position_y
        self.damage = PROJECTILE_DAMAGE
        self.fire_rate = TOWER_FIRE_RATE
        self.time_since_last_shot = 0

    def update(self, delta_time):
        self.time_since_last_shot += delta_time
        if self.time_since_last_shot >= self.fire_rate:
            self.time_since_last_shot = 0
            return True  
        return False

class Boss(arcade.AnimatedTimeBasedSprite):
    def __init__(self, position_x, position_y, target_x, target_y):
        super().__init__(scale=0.5)
        for image in boss_images:
            texture = arcade.load_texture(image)
            self.textures.append(texture)
        self.cur_texture_index = 0
        self.center_x = position_x
        self.center_y = position_y
        self.target_x = target_x
        self.target_y = target_y
        self.hp = BOSS_HP
        self.total_hp = BOSS_HP
        self.speed = BOSS_SPEED
        self.hp_textures = [arcade.load_texture(image) for image in boss_hp_images]
        self.hp_texture_index = 0
        self.time_since_last_change = 0

    def update(self):
        super().update()
        if self.hp > 0:
            self.time_since_last_change += 1
            if self.time_since_last_change >= 10: 
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
                self.texture = self.textures[self.cur_texture_index]
                self.time_since_last_change = 0
            direction = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
            self.center_x += (self.speed * 0.5) * math.cos(direction) 
            self.center_y += (self.speed * 0.5) * math.sin(direction)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        self.hp_texture_index = self.total_hp - self.hp
        self.hp_texture_index = min(self.hp_texture_index, len(self.hp_textures) - 1)
        if self.hp == 0:
            self.game.show_victory_screen()
            self.kill()

    def draw_health_bar(self):
        if self.hp > 0: 
            hp_texture = self.hp_textures[self.hp_texture_index]
            arcade.draw_texture_rectangle(self.center_x, self.center_y + 50, hp_texture.width // 4, hp_texture.height // 4, hp_texture)

class Projectile(arcade.Sprite):
    def __init__(self, start_position, target, damage):
        super().__init__(scale=0.5)
        self.textures = [arcade.load_texture(image) for image in projectile_images]
        self.center_x, self.center_y = start_position
        self.target = target
        self.damage = damage
        self.angle = math.atan2(target.center_y - self.center_y, target.center_x - self.center_x)
        self.cur_texture_index = 0
        self.time_since_last_change = 0
        self.fire_sound = arcade.load_sound(fireball_sound)
        self.slap_sound = arcade.load_sound(slap_sound)
        self.kill_sound = arcade.load_sound(kill_sound)


        self.angle = math.degrees(self.angle) - 90

    def update(self):
        self.center_x += PROJECTILE_SPEED * math.cos(math.radians(self.angle + 90))
        self.center_y += PROJECTILE_SPEED * math.sin(math.radians(self.angle + 90))
        self.time_since_last_change += 1
        if self.time_since_last_change >= 5:  
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.texture = self.textures[self.cur_texture_index]
            self.time_since_last_change = 0
        if check_collision(self, self.target):
            arcade.play_sound(self.slap_sound, volume=0.3) 
            self.target.take_damage(self.damage)
            if self.target.hp <= 0:
                arcade.play_sound(self.kill_sound, volume=0.3) 
                self.target.kill()
            self.kill()

    def on_spawn(self):
        arcade.play_sound(self.fire_sound, volume=0.3)

class Level2Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_image = arcade.load_texture(background_image)
        self.tower_button = arcade.Sprite(tower_button_image, scale=0.5, center_x=950, center_y=50)
        self.tower = None
        self.boss = None
        self.projectiles_list = arcade.SpriteList()
        self.show_dialogue = True
        self.dialogue_stage = 0
        self.dialogue_text = ""
        self.dialogue_index = 0
        self.dialogue_timer = 0
        self.dialogue_box = arcade.Sprite(dialogue_box_image, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2)
        self.dialogue_text_x = self.dialogue_box.center_x - 350
        self.dialogue_text_y = self.dialogue_box.center_y - 335
        self.continue_button = arcade.Sprite(continue_button_image, scale=0.5, center_x=SCREEN_WIDTH // 2 - 200, center_y=SCREEN_HEIGHT // 4 + 50)
        self.dialogue_texts = [
            ("Ну ничего себе", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/23.mp3"),
            ("Ты попал сюда", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/24.mp3"),
            ("В настоящий АД", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/25.mp3"),
            ("Не завидую тебе", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/26.mp3")
        ]
        self.boss_dialogue_texts = [
            ("ЕМАЕ!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/27.mp3"),
            ("ЭТО ОЛЕГ!!", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/28.mp3"),
            ("Если ты не умрешь", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/29.mp3"),
            ("Я отдам тебе", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/30.mp3"),
            ("А в приципе ничего", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/31.mp3"),
            ("Попробуй не здохнуть", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/32.mp3")
        ]
        self.end_dialogue_texts = [
            ("Вы победили", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/12.mp3"),
            ("Вернутся в меню", "C:/Users/Fridrix/Desktop/PyProject/sound/voice/13.mp3")
        ]
        self.boss_timer = 15
        self.show_boss_timer = False
        self.paused = False
        self.victory = False
        self.return_button = None
        self.song = arcade.load_sound(song_path)  # Загрузка песни

    def setup(self):
        self.font_name = arcade.load_font(font_path)
        arcade.set_background_color(arcade.color.WHITE)
        self
        self.font_name = arcade.load_font(font_path)
        arcade.set_background_color(arcade.color.WHITE)
        self.schedule_dialogue_texts()
        self.dialogue_sounds = [arcade.load_sound(sound) for _, sound in self.dialogue_texts]
        if self.dialogue_texts:
            arcade.play_sound(self.dialogue_sounds[self.dialogue_stage])

    def schedule_dialogue_texts(self):
        self.dialogue_sounds = [arcade.load_sound(sound) for _, sound in self.dialogue_texts]
        self.boss_dialogue_sounds = [arcade.load_sound(sound) for _, sound in self.boss_dialogue_texts]
        self.end_dialogue_sounds = [arcade.load_sound(sound) for _, sound in self.end_dialogue_texts]

    def show_victory(self):
        self.victory = True
        self.victory_text = "Вы победили!"
        self.return_button = arcade.Sprite(return_button_image, scale=0.5, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 4 + 50)
        self.boss.kill()  
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        if self.tower:
            self.tower.draw()
        if self.boss:
            self.boss.draw()
            self.boss.draw_health_bar()
        self.projectiles_list.draw()
        if self.tower_button:
            self.tower_button.draw()
        if self.show_dialogue:
            self.draw_dialogue()
        if self.show_boss_timer:
            arcade.draw_text(f"До появления босса: {int(self.boss_timer)} секунд", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60, arcade.color.WHITE, 14, font_name='Minecraft Rus', anchor_x="center")
        if self.victory:
            arcade.draw_text("Вы победили!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, arcade.color.WHITE, 20, anchor_x="center", font_name='Minecraft Rus')
            self.return_button.draw()

    def draw_dialogue(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 150))
        self.dialogue_box.draw()
        arcade.draw_text(self.dialogue_text, self.dialogue_text_x, self.dialogue_text_y, arcade.color.BLACK, 16, anchor_x="left", font_name='Minecraft Rus')
        if self.dialogue_stage < len(self.dialogue_texts):
            self.continue_button.draw()

    def on_update(self, delta_time):
        if self.paused:
            return

        if self.show_dialogue:
            self.dialogue_timer += delta_time
            if self.dialogue_timer > 0.1 and self.dialogue_index < len(self.dialogue_texts[self.dialogue_stage][0]):
                self.dialogue_text += self.dialogue_texts[self.dialogue_stage][0][self.dialogue_index]
                self.dialogue_index += 1
                self.dialogue_timer = 0
            elif self.dialogue_index == 0 and self.dialogue_timer == 0:
                sound_path = self.dialogue_texts[self.dialogue_stage][1]
                arcade.play_sound(self.dialogue_sounds[self.dialogue_stage])
        else:
            if self.show_boss_timer:
                self.boss_timer -= delta_time
                if self.boss_timer <= 0:
                    self.show_boss_timer = False
                    self.spawn_boss()
            if self.boss:
                self.boss.update()
            if self.tower and self.tower.update(delta_time):
                if self.boss and not self.boss.hp <= 0:
                    projectile = Projectile((self.tower.center_x, self.tower.center_y), self.boss, PROJECTILE_DAMAGE)
                    self.projectiles_list.append(projectile)
                    projectile.on_spawn()  
            self.projectiles_list.update()

    def spawn_boss(self):
        self.boss = Boss(0, SCREEN_HEIGHT // 2, self.tower.center_x, self.tower.center_y)
        self.boss.game = self  
        self.boss_timer = None

    def on_mouse_press(self, x, y, button, modifiers):
        if self.show_dialogue and self.continue_button.collides_with_point((x, y)):
            self.dialogue_stage += 1
            if self.dialogue_stage >= len(self.dialogue_texts):
                self.show_dialogue = False
                if self.dialogue_texts == self.boss_dialogue_texts:
                    self.show_boss_timer = True
                    self.boss_timer = 15
                    arcade.play_sound(self.song) 
                elif self.dialogue_texts == self.end_dialogue_texts:
                    self.window.show_view(LevelMenuView(None))
                return
            self.dialogue_text = ""
            self.dialogue_index = 0
            self.dialogue_timer = 0
            if self.dialogue_stage < len(self.dialogue_sounds):
                arcade.play_sound(self.dialogue_sounds[self.dialogue_stage])
        elif not self.show_dialogue:
            if self.tower_button and self.tower_button.collides_with_point((x, y)):
                self.tower = Tower(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                self.tower_button.kill()
                self.tower_button = None
                self.show_dialogue = True
                self.dialogue_stage = 0
                self.dialogue_text = ""
                self.dialogue_index = 0
                self.dialogue_timer = 0
                self.dialogue_texts = self.boss_dialogue_texts
                self.dialogue_sounds = [arcade.load_sound(sound) for _, sound in self.dialogue_texts]
                if self.dialogue_texts:
                    arcade.play_sound(self.dialogue_sounds[self.dialogue_stage])
            if self.victory and self.return_button.collides_with_point((x, y)):
                arcade.close_window()

    def show_victory_screen(self):
        self.paused = True
        self.victory = True
        self.return_button = arcade.Sprite(return_button_image, scale=0.5, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - 50)

def get_bounding_box(sprite):
    left = sprite.center_x - sprite.width / 2
    right = sprite.center_x + sprite.width / 2
    bottom = sprite.center_y - sprite.height / 2
    top = sprite.center_y + sprite.height / 2
    return left, right, bottom, top

def check_collision(sprite1, sprite2):
    left1, right1, bottom1, top1 = get_bounding_box(sprite1)
    left2, right2, bottom2, top2 = get_bounding_box(sprite2)
    return not (right1 < left2 or right2 < left1 or top1 < bottom2 or top2 < bottom1)

class LevelMenuView(arcade.View):
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Меню уровней", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, 20, anchor_x="center", font_name='Minecraft Rus')

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    level2_game = Level2Game()
    level2_game.setup()
    window.show_view(level2_game)
    arcade.run()

if __name__ == "__main__":
    main()
