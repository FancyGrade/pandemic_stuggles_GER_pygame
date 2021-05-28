# import
import pygame
import random
from os import path
from settings import *
from sprites import *
from tilemap import *
from events import *
import pytmx  # pytmx


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.gamewindow = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        # displaysize = pygame.display.Info()  # get native resolution
        self.clock = pygame.time.Clock()
        pygame.mouse.set_cursor(pygame.cursors.tri_left)
        self.mouseover = 0
        self.mouseover_cursor = False

        # load load_data
        self.running = True
        self.load_data()

        # camera setup
        self.camera_x = 0
        self.camera_y = 0
        self.cx = 0
        self.cy = 0
        self.camera_lastframe_x = 0
        self.camera_lastframe_y = 0
        self.camera_offset_x = 0
        self.camera_offset_y = 0

        # event setup
        self.show_event = False
        self.eventanimation_timer = 0
        self.click = False
        self.moneytooltip_shown = False

        # economy setup
        self.money = STARTMONEY
        self.oldmoney = STARTMONEY
        self.moneyearning = MONEYEARNING
        self.currentmoney = self.font_munro.render((" " + str(self.money) +
                                                    "€ "), False, pygame.Color(BLACK), pygame.Color(GREY50))

        # date tracker setup
        self.months = ["Januar", "Februar", "Maerz", "April",
                       "Mai", "Juni", "Juli", "August", "September",
                       "Oktober", "November", "Dezember"]
        self.year = 2020
        self.date_tracker = 0
        self.time_tracker = 0
        self.week_duration = int(TIMEOFMONTH / 4)
        self.week_tracker = 0
        self.week_counter = 1
        self.currentdate = self.font_munro_small.render((" " + str(self.months[self.date_tracker]) + " " +
                                                         str(self.year) + " Woche " + str(self.week_counter) + " "),
                                                        False, pygame.Color(BLACK), pygame.Color(WHITE))

        self.pause = False

        # building setup
        self.currently_selected_building = None

        # USEREVENTS
        self.BUILD_TESTCENTER = pygame.USEREVENT + 0
        self.build_testcenter_event = pygame.event.Event(self.BUILD_TESTCENTER)
        self.BUILD_HOSTPITAL = pygame.USEREVENT + 1
        self.build_hospital_event = pygame.event.Event(self.BUILD_HOSTPITAL)
        self.BUILD_VACCINECENTER = pygame.USEREVENT + 2
        self.build_vaccinecenter_event = pygame.event.Event(self.BUILD_VACCINECENTER)

        # no money setup
        self.not_enough_money = False
        self.not_enough_money_text = self.font_munro_small.render(" du hast nicht genug Geld ", False,
                                                                  pygame.Color(WHITE), pygame.Color(BLACK))
        self.not_enough_money_timer = 0

    # --------------------------------------------
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        assets_folder = path.join(game_folder, "assets")
        self.map = TiledMap(path.join(assets_folder, "tileset_map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # borders laden
        self.borders = pygame.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "unpassable_border":
                Border(self, tile_object.x, tile_object.y,
                       tile_object.width, tile_object.height)

        # load font
        self.font_munro_small = pygame.font.Font("assets/munro-small.ttf", 30)
        self.font_munro = pygame.font.Font("assets/munro.ttf", 80)

    # --------------------------------------------
    def time_event_setup(self, bg, event_headline, event_text, event_picture):

        self.event_background = pygame.image.load(bg)
        event_background_rect = self.event_background.get_rect()

        self.event_background_x = self.event_background.get_width()
        self.event_background_y = self.event_background.get_height()

        # render headline
        headline = self.font_munro.render(event_headline, False,
                                          pygame.Color(BLACK), pygame.Color(WHITE))
        headline_rect = headline.get_rect()
        headline_rect.center = self.event_background_x / 2, self.event_background_y / 2 - 200

        picture = pygame.image.load(event_picture)
        self.current_picture_x = picture.get_width()
        self.current_picture_y = picture.get_height()

        # rotate pictures and create rotated copys
        self.picture_rotated_right = pygame.transform.rotate(picture, 10)
        self.picture_rotated_right_rect = self.picture_rotated_right.get_rect()
        self.picture_rotated_right_rect.center = WIDTH / 2, HEIGHT / 2 + self.event_background_y / 2 - 125
        self.picture_rotated_left = pygame.transform.rotate(picture, -10)
        self.picture_rotated_left_rect = self.picture_rotated_left.get_rect()
        self.picture_rotated_left_rect.center = WIDTH / 2, HEIGHT / 2 + self.event_background_y / 2 - 125

        # enable alpha channel for surface
        self.current_surface = pygame.Surface((self.event_background_x,
                                               self.event_background_y),
                                              pygame.SRCALPHA)
        self.current_surface.convert_alpha()
        self.current_surface.fill((0, 0, 0, 0))

        # draw bg and headline
        self.current_surface.blit(self.event_background, event_background_rect)
        self.current_surface.blit(headline, headline_rect)

        # make text wrap around lines
        # (stolen from https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame)
        words = [word.split(' ') for word in event_text.splitlines()]
        space = self.font_munro_small.size(" ")[0]
        max_width, max_height = self.current_surface.get_size()
        max_width -= 150
        pos = self.event_background_x / 2 - 360, self.event_background_y / 3
        x, y = pos
        for line in words:
            for word in line:
                word_surface = self.font_munro_small.render(word, False,
                                                            pygame.Color(WHITE))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                self.current_surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

        # change values according to the event

    # --------------------------------------------
    def time_event(self):
        # animate & draw picture
        if self.eventanimation_timer <= 20 / 60 * FPS:
            self.gamewindow.blit(self.picture_rotated_left,
                                 self.picture_rotated_left_rect)
            self.eventanimation_timer += 1
        else:
            self.gamewindow.blit(self.picture_rotated_right,
                                 self.picture_rotated_right_rect)
            self.eventanimation_timer += 1
            if self.eventanimation_timer == 40 / 60 * FPS:
                self.eventanimation_timer = 0

        # draw event screen
        surface_rect = self.current_surface.get_rect()
        surface_rect.center = WIDTH / 2, HEIGHT / 2
        self.gamewindow.blit(self.current_surface, surface_rect)

        # check for click to exit event
        exitbutton = pygame.Rect(WIDTH / 2 + 280, HEIGHT / 2 - 340, 155, 110)
        if exitbutton.collidepoint((pygame.mouse.get_pos())):
            self.mouseover += 1
            if pygame.mouse.get_pressed()[0]:
                self.show_event = False

    # --------------------------------------------
    # keep track of current date and year and display it in top left corner
    # sorry für den schrecklichen code in diesem teil ich hab mich völlig verzettelt :D
    def time_tracker_function(self):
        if self.time_tracker == TIMEOFMONTH:
            self.time_tracker = 0
            self.date_tracker += 1
            self.week_counter = 0

        if self.date_tracker > 11:
            self.date_tracker = 0
            self.year += 1

        self.time_tracker += 1

        self.week_tracker += 1

        if self.week_duration < self.week_tracker:
            self.week_tracker = 0
            self.week_counter += 1
            self.money += self.moneyearning  # weekly earnings
            self.eventtriggercheck()
            self.currentdate = self.font_munro_small.render((" " + str(self.months[self.date_tracker]) + " " +
                                                             str(self.year) + " Woche " + str(self.week_counter) + " "),
                                                            False, pygame.Color(BLACK), pygame.Color(WHITE))

    # --------------------------------------------
    def moneytracker(self):

        if self.oldmoney is not self.money:
            if self.money <= 0:
                colour = RED
                if not self.moneytooltip_shown:
                    self.time_event_setup(*eventMN_list)
                    self.moneytooltip_shown = True
                    self.show_event = True
            else:
                colour = BLACK
            self.currentmoney = self.font_munro.render((" " + str(self.money) +
                                                        "€ "), False, pygame.Color(colour), pygame.Color(GREY50))

        self.oldmoney = self.money

    # --------------------------------------------
    def mouseovercursor(self):

        if self.mouseover <= 0:
            if self.mouseover_cursor:
                pass
            else:
                self.mouseover_cursor = True
                pygame.mouse.set_cursor(pygame.cursors.tri_left)

        else:
            if self.mouseover_cursor:
                self.mouseover_cursor = False
                pygame.mouse.set_cursor(pygame.cursors.broken_x)
            else:
                pass
        self.mouseover = 0

    # --------------------------------------------
    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.humans = pygame.sprite.Group()
        self.infected = pygame.sprite.Group()
        self.ill = pygame.sprite.Group()
        self.buildings = pygame.sprite.Group()
        self.tempbuildings = pygame.sprite.Group()
        self.building_icons = pygame.sprite.Group()
        # make humans spawn, kill everyone who didn't spawn inside play area
        # and repeat till all humans spawned
        self.human_count = 0
        while self.human_count < HUMAN_COUNT:
            h = Human(self, random.randint(10, self.map.width - 10),
                      random.randint(10, self.map.height - 10))
            self.human_count += 1
            # kill all Humans which spawn inside walls
            if h.collide_with_borders():
                h.kill()
                self.human_count -= 1

        # create build icons
        testcentericon = BuildingIcon(self, "testcenter", 100)
        hospitalicon = BuildingIcon(self, "hospital", 0)
        vaccicon = BuildingIcon(self, "vacc", -100)

        # show welcome event
        self.time_event_setup(*event01_list)
        self.show_event = True

        g.gameloop()

    # --------------------------------------------
    def gameloop(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.camera()
            self.moneytracker()
            self.mouseovercursor()

    # --------------------------------------------
    def update(self):
        if not self.show_event and not self.pause:
            self.all_sprites.update()
            self.time_tracker_function()

    # --------------------------------------------
    def camera(self):
        self.cx = 0
        self.cy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.cx = -CAMERA_SPEED
        if keys[pygame.K_a]:
            self.cx = +CAMERA_SPEED
        if keys[pygame.K_w]:
            self.cy = +CAMERA_SPEED
        if keys[pygame.K_s]:
            self.cy = -CAMERA_SPEED
        self.camera_x += self.cx
        self.camera_y += self.cy
        # limit camera to map_img
        self.camera_x = min(0, self.camera_x)
        self.camera_y = min(0, self.camera_y)
        self.camera_x = max(-(self.map.width - WIDTH), self.camera_x)
        self.camera_y = max(-(self.map.height - HEIGHT), self.camera_y)
        # making sure that sprites only move when camera moved
        self.camera_offset_x = self.camera_lastframe_x - self.camera_x
        self.camera_offset_y = self.camera_lastframe_y - self.camera_y
        self.camera_lastframe_x = self.camera_x
        self.camera_lastframe_y = self.camera_y
        for sprite in self.humans:
            sprite.rect.x -= self.camera_offset_x
            sprite.rect.y -= self.camera_offset_y
        for sprite in self.borders:
            sprite.rect.x -= self.camera_offset_x
            sprite.rect.y -= self.camera_offset_y
        for sprite in self.buildings:
            sprite.rect.x -= self.camera_offset_x
            sprite.rect.y -= self.camera_offset_y

    # --------------------------------------------
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # QUIT Knopf einfügen
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_e:
                    if not self.show_event:
                        self.time_event_setup(*event01_list)
                        self.show_event = True
                    else:
                        self.show_event = False
                if event.key == pygame.K_p:
                    if self.pause is True:
                        self.pause = False
                    else:
                        self.pause = True
            # RMB cancels build mode for buildings, killing the sprite
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for sprite in self.tempbuildings:
                    sprite.kill()
                self.currently_selected_building = None
            # LMB
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.currently_selected_building == 1:
                    pygame.event.post(self.build_testcenter_event)
                elif self.currently_selected_building == 2:
                    pygame.event.post(self.build_hospital_event)
                elif self.currently_selected_building == 3:
                    pygame.event.post(self.build_vaccinecenter_event)
            # if event.type == TIMEEVENT:
            #     self.timeEventsetup(*event)
            elif event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False
            elif event.type == self.BUILD_TESTCENTER:
                if self.money >= 1:
                    t = TestCenter(self)
                else:
                    self.not_enough_money = True
            elif event.type == self.BUILD_HOSTPITAL:
                if self.money >= 1:
                    h = Hospital(self)
                else:
                    self.not_enough_money = True
            elif event.type == self.BUILD_VACCINECENTER:
                if self.money >= 1:
                    v = VaccineCenter(self)
                else:
                    self.not_enough_money = True

    # --------------------------------------------

    def eventtriggercheck(self):
        month = self.months[self.date_tracker]
        year = self.year
        week = self.week_counter

        # EVENT 2
        if month == "Januar" and year == 2020 and week == 2:
            self.time_event_setup(*event02_list)
            self.show_event = True

        # EVENT 2
        # if self.date_tracker == 2 and self.year == 2020:
        #     self.timeEventsetup(*event02_list)
        #     self.show_event = True
        #
        #     self.money -= 100

    # --------------------------------------------

    # --------------------------------------------
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.gamewindow, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.gamewindow, BLACK, (0, y), (WIDTH, y))

    def draw(self):
        # self.gamewindow.fill(GREY50)
        self.gamewindow.blit(self.map_img, (self.camera_x, self.camera_y))
        # self.draw_grid()
        self.all_sprites.draw(self.gamewindow)

        for building in self.building_icons:
            building.drawinfotext()  # mouseover

        for building in self.buildings:
            building.draw_range()
        for building in self.tempbuildings:
            building.draw_range()

        # Events draw

        # show FPS
        if SHOW_FPS:
            fps = self.font_munro_small.render("FPS: " + str(int(self.clock.get_fps())),
                                               False, pygame.Color(BLACK))
            self.gamewindow.blit(fps, ((WIDTH - 100), 5))
        # print how many infected
        count_inf = len(self.infected.sprites())
        count_hum = len(self.humans.sprites())
        count_trt = len(self.ill.sprites())
        if SHOW_INFECTED:
            perc_inf = self.font_munro_small.render((str(count_inf) + " of " +
                                                     str(count_hum) + " infected (" +
                                                     str(int(count_inf / count_hum * 100)) +
                                                     " %)"), False, pygame.Color(BLACK))
            self.gamewindow.blit(perc_inf, (25, HEIGHT - 60))
            # print how many in need of medical treatment
            perc_trt = self.font_munro_small.render((str(count_trt) + " of " +
                                                     str(count_hum) +
                                                     " in need of medical treatment (" +
                                                     str(int(count_trt / count_hum * 100)) +
                                                     " %)"), False, pygame.Color(BLACK))
            self.gamewindow.blit(perc_trt, (25, HEIGHT - 35))

        # show event_text
        if self.show_event:
            self.time_event()

        # draw dated
        self.gamewindow.blit(self.currentdate, (5, 5))

        # draw money & not not_enough_money warning
        self.gamewindow.blit(self.currentmoney, (WIDTH / 2 - 30, 5))
        if self.not_enough_money:
            x, y = pygame.mouse.get_pos()
            self.gamewindow.blit(self.not_enough_money_text, (x + 30, y + 10))
            self.not_enough_money_timer += 1
            if self.not_enough_money_timer == (1 * FPS):
                self.not_enough_money = False
                self.not_enough_money_timer = 0

        # draw pause symbol
        if self.pause:
            pygame.draw.rect(self.gamewindow, WHITE, (WIDTH / 2 - 80, HEIGHT / 2, 50, 100))
            pygame.draw.rect(self.gamewindow, WHITE, (WIDTH / 2, HEIGHT / 2, 50, 100))

        pygame.display.flip()

    # --------------------------------------------
    def show_start_screen(self):
        pass

    # --------------------------------------------
    def show_gameover_screen(self):
        pass


g = Game()

while g.running:
    g.new()
    g.show_gameover_screen()

pygame.quit()
