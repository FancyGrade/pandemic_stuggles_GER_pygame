from settings import *
import pygame
import random


class Human(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.humans
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.colour = WHITE
        surface = pygame.Surface((HUMAN_SIZE, HUMAN_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.colour, (HUMAN_SIZE/2, HUMAN_SIZE/2), HUMAN_SIZE/2)
        self.image = surface
        self.game = game
        self.apply_colour()
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vx = 0
        self.vy = 0
        self.moving = False
        self.ill = False
        self.human_timer = 0
        self.walked_frames = 0
        self.walk_delay = (WALKCYCLE / 60 * FPS + random.randint(-100, 1000))
        self.walk_distance = (WALKDISTANCE + random.randint(0, 20))
        self.walk_direction_x = random.randint(-1, 1)
        self.walk_direction_y = random.randint(-1, 1)
        self.vacc_state = False
        # infect X% of Humans, if True then run infect
        self.infection_calculator = random.randint(1, 100)
        if self.infection_calculator > INITIAL_INFECTION_CHANCE:
            self.infected_status = False
        else:
            self.infected_status = True
            self.infect()

    def apply_colour(self):
        surface = pygame.Surface((HUMAN_SIZE, HUMAN_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.colour, (HUMAN_SIZE / 2, HUMAN_SIZE / 2), HUMAN_SIZE / 2)
        self.image = surface

    def infect_check(self):
        ix = random.randint(0, int(FPS * INFECT_CHANCE / (self.game.infect_multiplyer / 10)))
        if ix == int(FPS * INFECT_CHANCE / (self.game.infect_multiplyer / 10)):
            if pygame.sprite.spritecollideany(self, self.game.infected) is not None:
                return True

    def ill_check(self):
        if self.infected_status is True:
            x = random.randint(0, (FPS * ILL_CHANCE))
            if x == (FPS * ILL_CHANCE):
                self.ill = True
                self.colour = MAGENTA
                self.game.ill.add(self)

    def infect(self):
        self.colour = RED
        self.game.infected.add(self)
        self.infected_status = True

    def heal(self):
        self.colour = WHITE
        self.game.infected.remove(self)
        self.game.ill.remove(self)
        self.infected_status = False
        self.apply_colour()

    def vaccinate(self):
        self.colour = BLUE
        self.vacc_state = True
        self.game.vacced.add(self)
        self.apply_colour()

    def walk(self, wx, wy):
        self.vx = wx
        self.vy = wy
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.collide_with_borders():
            self.vx = wx * -1
            self.vy = wy * -1
            self.rect.x += self.vx
            self.rect.y += self.vy
            # turn them around
            self.walk_direction_x = self.walk_direction_x * -1
            self.walk_direction_y = self.walk_direction_y * -1

    def collide_with_borders(self):
        if pygame.sprite.spritecollideany(self, self.game.borders) is not None:
            return True

    def update(self):
        # move humans randomly
        # ramdomise how frequent they move
        self.vx = 0
        self.vy = 0
        if self.moving is False:
            self.human_timer += 1
            if self.human_timer > self.walk_delay:
                # randomise next delay & distance & direction
                self.walk_delay = (WALKCYCLE / 60 * FPS + random.randint(-100, 1000))
                self.walk_distance = (WALKDISTANCE + random.randint(0, 20))
                self.walk_direction_x = random.randint(-1, 1)
                self.walk_direction_y = random.randint(-1, 1)
                self.moving = True

        if self.moving is True:
            if self.walked_frames < self.walk_distance:
                Human.walk(self, self.walk_direction_x, self.walk_direction_y)
                self.walked_frames += 1
            else:
                self.moving = False
                self.walked_frames = 0
                self.human_timer = 0

        if not self.vacc_state:
            if self.infected_status is False:
                if self.infect_check():
                    self.infect()

        self.rect.x += self.vx
        self.rect.y += self.vy

        self.ill_check()


# --------------------------------------------


class Border(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.borders
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


# --------------------------------------------
class Buildings(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.testcenterimage = "assets/buildingicons/testcenter_scaled.png"
        self.game.hospitalimage = "assets/buildingicons/hospital_scaled.png"
        self.game.vaccineimage = "assets/buildingicons/vacc_scaled.png"

        self.image = pygame.Surface((HUMAN_SIZE, HUMAN_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def deselect_icons(self):
        for sprite in self.game.tempbuildings:
            sprite.kill()
        self.game.currently_selected_building = None


class BuildingIcon(Buildings):
    def __init__(self, game, btype, y):
        super().__init__(game)
        self.game.building_icons.add(self)
        if btype == "testcenter":
            image = self.game.testcenterimage
            infotext = str(" erstelle ein Testcenter ("
                           + str(game.testcenter_price) + "???) (Hotkey: 1) ")
        elif btype == "hospital":
            image = self.game.hospitalimage
            infotext = str(" erstelle ein Krankenhaus ("
                           + str(HOSPITAL_PRICE) + "???) (Hotkey: 2) ")
        else:
            image = self.game.vaccineimage
            infotext = str(" erstelle ein Impfzentrum ("
                           + str(game.vaccinecenter_price) + "???) (Hotkey: 3) ")
        self.type = btype
        self.game = game
        self.text = game.font_munro_small.render(infotext, False, pygame.Color(WHITE), pygame.Color(BLACK))
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = HEIGHT / 2 - y

    def update_mouseover_text(self):
        if self.type == "testcenter":
            image = self.game.testcenterimage
            infotext = str(" erstelle ein Testcenter ("
                           + str(self.game.testcenter_price) + "???) (Hotkey: 1) ")
        elif self.type == "hospital":
            image = self.game.hospitalimage
            infotext = str(" erstelle ein Krankenhaus ("
                           + str(HOSPITAL_PRICE) + "???) (Hotkey: 2) ")
        else:
            image = self.game.vaccineimage
            infotext = str(" erstelle ein Impfzentrum ("
                           + str(self.game.vaccinecenter_price) + "???) (Hotkey: 3) ")
        self.text = self.game.font_munro_small.render(infotext, False, pygame.Color(WHITE), pygame.Color(BLACK))
        self.image = pygame.image.load(image)

    def update(self):
        if self.game.currently_selected_building is None:
            if self.rect.collidepoint((pygame.mouse.get_pos())) and pygame.mouse.get_pressed()[0]:
                if self.type == "testcenter":
                    self.game.currently_selected_building = 1
                    b = BuildingIconShadow(self.game, self.game.testcenterimage,
                                           int(TESTCENTER_RANGE * self.game.testcenter_range_multiplyer))
                elif self.type == "hospital":
                    self.game.currently_selected_building = 2
                    b = BuildingIconShadow(self.game, self.game.hospitalimage, HOSPITAL_RANGE)
                elif self.type == "vacc":
                    self.game.currently_selected_building = 3
                    b = BuildingIconShadow(self.game, self.game.vaccineimage, VACCINECENTER_RANGE)

    def drawinfotext(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint((x, y)):
            self.game.gamewindow.blit(self.text, (x + 20, y + 10))
            self.game.mouseover += 1
            self.game.mouseover_building_icons = True



class BuildingIconShadow(Buildings):
    def __init__(self, game, image, effect_range):
        super().__init__(game)
        self.game.tempbuildings.add(self)
        bigimage = pygame.image.load(image)
        bigimage_w = bigimage.get_width()
        bigimage_h = bigimage.get_height()
        self.image = pygame.transform.scale(bigimage, (int(bigimage_w / 2), int(bigimage_h / 2)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.ring_colour = BLACK
        self.shadowrange = effect_range

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.center = x, y
        self.game.gamewindow.blit(self.image, pygame.mouse.get_pos())
        self.game.mouseover += 1

    def draw_range(self):
        pygame.draw.circle(self.game.gamewindow, self.ring_colour,
                           (self.rect.x + self.width / 2,
                            self.rect.y + self.height / 2), int(self.shadowrange), 3)


class BuildingTemplate(Buildings):
    def __init__(self, game):
        game.plop_sound.play()
        super().__init__(game)
        self.game.buildings.add(self)
        self.deselect_icons()
        self.x, self.y = pygame.mouse.get_pos()
        self.livetimer = self.time * FPS
        self.orig_livetimer = self.livetimer
        self.ring_colour = 255
        self.radius = self.range
        self.effect_counter = FPS
        game.money -= self.price

    def setup_image(self, image):
        bigimage = pygame.image.load(image)
        bigimage_w = bigimage.get_width()
        bigimage_h = bigimage.get_height()
        self.image = pygame.transform.scale(bigimage, (int(bigimage_w / 2), int(bigimage_h / 2)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def draw_range(self):
        pygame.draw.circle(self.game.gamewindow, (self.ring_colour,
                                                  self.ring_colour, self.ring_colour),
                           (self.rect.x + self.width / 2,
                            self.rect.y + self.height / 2), int(self.range), 3)

    def kill_countdown(self):
        self.livetimer -= 1
        if self.livetimer <= 0:
            self.kill()

    def colour_changer(self):  # Change the ring colour to indicate rem. time
        livepercentage = 100 - (self.livetimer / self.orig_livetimer * 100)
        self.ring_colour = int(livepercentage * 255 / 100)

    def effect_timer(self):
        if self.effect_counter == FPS:
            self.effect_counter = 0
            self.effect()
        self.effect_counter += 1

    def effect(self):
        pass

    def update(self):
        self.kill_countdown()
        self.colour_changer()
        self.effect_timer()


class TestCenter(BuildingTemplate):
    def __init__(self, game):
        self.range = int(TESTCENTER_RANGE * game.testcenter_range_multiplyer)
        self.price = game.testcenter_price
        self.time = TESTCENTER_TIME
        super().__init__(game)
        image = self.game.testcenterimage
        self.setup_image(image)

    def effect(self):  # expose true status (colour) of humans in range
        spritelist = pygame.sprite.spritecollide(self, self.game.humans, False,
                                                 pygame.sprite.collide_circle)
        for sprite in spritelist:
            sprite.apply_colour()

        if not self.game.hospitalunlocked:  # unlock hospital after first found infection
            spritelist = pygame.sprite.spritecollide(self, self.game.infected, False,
                                                     pygame.sprite.collide_circle)
            for sprite in spritelist:
                self.game.hospitalunlocked = True


class Hospital(BuildingTemplate):
    def __init__(self, game):
        self.range = HOSPITAL_RANGE
        self.price = HOSPITAL_PRICE
        self.time = HOSPITAL_TIME
        super().__init__(game)
        image = self.game.hospitalimage
        self.setup_image(image)

    def effect(self):
        spritelist = pygame.sprite.spritecollide(self, self.game.infected, False,
                                                 pygame.sprite.collide_circle)
        for sprite in spritelist:
            sprite.heal()


class VaccineCenter(BuildingTemplate):
    def __init__(self, game):
        self.range = VACCINECENTER_RANGE
        self.price = game.vaccinecenter_price
        self.time = VACCINECENTER_TIME
        super().__init__(game)
        image = self.game.vaccineimage
        self.setup_image(image)

    def effect(self):
        spritelist = pygame.sprite.spritecollide(self, self.game.humans, False,
                                                 pygame.sprite.collide_circle)
        for sprite in spritelist:
            sprite.vaccinate()


class Menuoptions():
    def __init__(self, game, text, x_offset, y_offset):
        self.game = game
        self.text = text
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.highlight = False
        self.colour = self.game.option_default_colour

        self.textobject = self.game.font_munro.render(self.text, False, self.colour, self.game.option_background_colour)

        self.textobject_rect = self.textobject.get_rect()
        self.textobject_rect.center = WIDTH / 2 + self.x_offset, HEIGHT / 2 - 20 + self.y_offset

        self.ready = False
        self.cooldown_timer = 0

    def get_textobject(self):
        return self.textobject

    def get_textobject_rect(self):
        return self.textobject_rect

    def get_highlighted_status(self):
        return self.highlight

    def update_text_colour(self, colour):
        if self.colour != colour:
            self.colour = colour
            self.textobject = self.game.font_munro.render(self.text, False, self.colour,
                                                          self.game.option_background_colour)

    def draw_text(self):
        if self.get_textobject_rect().collidepoint((pygame.mouse.get_pos())):
            self.game.mouseover += 1
            if not self.get_highlighted_status():
                self.update_text_colour(self.game.option_highlight_colour)
            if pygame.mouse.get_pressed()[0] and self.ready:
                for menu in self.game.menu_button_list:
                    menu.unready_self()
                self.game.gamewindow.blit(self.textobject, self.textobject_rect)
                self.game.plop_sound.play()
                return True
            elif not pygame.mouse.get_pressed()[0] and not self.ready:
                self.ready = True
        else:
            self.update_text_colour(self.game.option_default_colour)

        self.game.gamewindow.blit(self.textobject, self.textobject_rect)

    def unready_self(self):
        self.ready = False

    def update_text(self, text):
        self.text = text
        self.textobject = self.game.font_munro.render(self.text, False, self.colour,
                                                      self.game.option_background_colour)
        self.textobject_rect = self.textobject.get_rect()
        self.textobject_rect.center = WIDTH / 2, HEIGHT / 2 - 20 + self.y_offset
