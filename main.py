# import
import pygame
import random
from os import path
from settings import *
from sprites import *
from tilemap import *
from events import *
import pytmx
import sys

# fix for the windows scaling problem in pygame
import ctypes
ctypes.windll.user32.SetProcessDPIAware()


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
        self.mouseover_building_icons = False

        # load fonts
        self.font_munro_small = pygame.font.Font("assets/fonts/munro-small.ttf", 30)
        self.font_munro = pygame.font.Font("assets/fonts/munro.ttf", 70)
        self.font_munro_headline = pygame.font.Font("assets/fonts/munro.ttf", 50)
        self.font_comic_sans = pygame.font.SysFont("Comic Sans MS", 22)

        # load load_data
        self.running = True
        self.pause_setup()
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
        self.infect_multiplyer = 10
        self.testcenter_range_multiplyer = 1.0
        self.vaccinecenter_price = VACCINECENTER_PRICE
        self.testcenter_price = TESTCENTER_PRICE
        self.show_endscreen = False

        # economy setup
        self.money = STARTMONEY
        self.oldmoney = STARTMONEY
        self.moneyearning = MONEYEARNING
        self.currentmoney = self.font_munro.render((" " + str(self.money) +
                                                    "€ "), False, pygame.Color(WHITE), pygame.Color(GREY50))
        self.moneywidth = self.currentmoney.get_width()

        # date tracker setup
        self.months = ["Januar", "Februar", "Maerz", "April",
                       "Mai", "Juni", "Juli", "August", "September",
                       "Oktober", "November", "Dezember"]
        self.year = 2020
        self.date_tracker = 2
        self.time_tracker = 0
        self.week_duration = int(TIMEOFMONTH / 4)
        self.week_tracker = 0
        self.week_counter = 1
        self.currentdate = self.font_munro_small.render((" " + str(self.months[self.date_tracker]) + " " +
                                                         str(self.year) + " Woche " + str(self.week_counter) + " "),
                                                        False, pygame.Color(BLACK), pygame.Color(WHITE))

        self.pause = False
        self.show_menu = True

        # building setup
        self.testcenterimage = "assets/buildingicons/testcenter_scaled.png"
        self.hospitalimage = "assets/buildingicons/hospital_scaled.png"
        self.vaccineimage = "assets/buildingicons/vacc_scaled.png"
        self.currently_selected_building = None
        self.hospitalunlocked = False
        self.hospitalunlocked_event_shown = False
        self.testcenter_unlocked = False
        self.hospital_unlocked = False
        self.vaccinecenter_unlocked = False

        # sound setup
        self.allsounds_list = []

        self.plop_sound = pygame.mixer.Sound("assets/soundfiles/plop.mp3")
        self.plop_sound.set_volume(DEFAULTVOLUME)
        self.allsounds_list.append(self.plop_sound)

        self.eventsound_sound = pygame.mixer.Sound("assets/soundfiles/whoosh.mp3")
        self.eventsound_sound.set_volume(DEFAULTVOLUME)
        self.allsounds_list.append(self.eventsound_sound)

        self.bgmusic_sound = pygame.mixer.Sound("assets/soundfiles/262259__shadydave__snowfall-final.mp3")
        self.bgmusic_sound.set_volume(DEFAULTVOLUME)
        self.allsounds_list.append(self.bgmusic_sound)

        self.bgmusic_sound.play(-1)

        self.change_master_sound()

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
        tileset_assets_folder = path.join(game_folder, "assets/tileset_assets")
        self.map = TiledMap(path.join(tileset_assets_folder, "tileset_map.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # borders laden
        self.borders = pygame.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "unpassable_border":
                Border(self, tile_object.x, tile_object.y,
                       tile_object.width, tile_object.height)

    # --------------------------------------------
    def time_event_setup(self, bg, event_headline, event_text, event_picture):
        # deselect buldings before setup
        for sprite in self.tempbuildings:
            sprite.kill()
        self.currently_selected_building = None

        headlinefont = self.font_munro_headline
        textfont = self.font_comic_sans

        self.event_background = pygame.image.load(bg)
        event_background_rect = self.event_background.get_rect()

        self.event_background_x = self.event_background.get_width()
        self.event_background_y = self.event_background.get_height()

        # render headline
        headline = headlinefont.render(event_headline, False,
                                          pygame.Color(BLACK), pygame.Color(WHITE))
        headline_rect = headline.get_rect()
        headline_rect.center = self.event_background_x / 2, self.event_background_y / 2 - 220

        picture = pygame.image.load(event_picture)
        self.current_picture_x = picture.get_width()
        self.current_picture_y = picture.get_height()

        # rotate pictures and create rotated copys
        self.picture_rotated_right = pygame.transform.rotate(picture, 10)
        self.picture_rotated_right_rect = self.picture_rotated_right.get_rect()
        self.picture_rotated_right_rect.center = WIDTH / 2, HEIGHT / 2 + self.event_background_y / 2 - 137
        self.picture_rotated_left = pygame.transform.rotate(picture, -10)
        self.picture_rotated_left_rect = self.picture_rotated_left.get_rect()
        self.picture_rotated_left_rect.center = WIDTH / 2, HEIGHT / 2 + self.event_background_y / 2 - 137

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
        space = textfont.size(" ")[0]
        max_width, max_height = self.current_surface.get_size()
        max_width -= 50
        pos = self.event_background_x / 2 - 440, self.event_background_y / 3 - 40
        x, y = pos
        for line in words:
            for word in line:
                word_surface = textfont.render(word, False,
                                                            pygame.Color(WHITE))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                self.current_surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

        # play sound!
        self.eventsound_sound.play()

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
        exitbutton = pygame.Rect(WIDTH / 2 + 280, HEIGHT / 2 - 340, 230, 100)
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
                if not self.moneytooltip_shown and not self.show_event:
                    self.time_event_setup(*eventMN_list)
                    self.moneytooltip_shown = True
                    self.show_event = True
            else:
                colour = WHITE
            self.currentmoney = self.font_munro.render((" " + str(self.money) +
                                                        "€ "), False, pygame.Color(colour), pygame.Color(GREY50))
            self.moneywidth = self.currentmoney.get_width()
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
        self.vacced = pygame.sprite.Group()
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

        g.gameloop()

    # --------------------------------------------
    def gameloop(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            if not self.show_menu:
                self.draw()
            else:
                self.draw_pause()
            self.camera()
            self.moneytracker()
            self.mouseovercursor()

    # --------------------------------------------
    def update(self):
        if not self.show_event and not self.pause and not self.show_menu:
            self.all_sprites.update()
            self.time_tracker_function()

    # --------------------------------------------
    # camera function is copied from a tutorial
    # "Tile-based game Part 4: Scrolling Map / Camera" https://youtu.be/3zV2ewk-IGU
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
    def change_master_sound(self):
        for sound in self.allsounds_list:
            sound.set_volume(self.master_volume)

    # --------------------------------------------
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = not self.show_menu
                    self.show_credits = False
                    self.show_settings = False
                    self.startup_screen_shown = True
                    self.option_continue.update_text(" Spiel fortsetzen ")
                elif event.key == pygame.K_1:
                    if self.testcenter_unlocked:
                        for sprite in self.tempbuildings:
                            sprite.kill()
                        self.currently_selected_building = None
                        b = BuildingIconShadow(self, self.testcenterimage,
                                               int(TESTCENTER_RANGE * self.testcenter_range_multiplyer))
                        self.currently_selected_building = 1
                elif event.key == pygame.K_2:
                    if self.hospital_unlocked:
                        for sprite in self.tempbuildings:
                            sprite.kill()
                        self.currently_selected_building = None
                        b = BuildingIconShadow(self, self.hospitalimage, HOSPITAL_RANGE)
                        self.currently_selected_building = 2
                elif event.key == pygame.K_3:
                    if self.vaccinecenter_unlocked:
                        for sprite in self.tempbuildings:
                            sprite.kill()
                        self.currently_selected_building = None
                        b = BuildingIconShadow(self, self.vaccineimage, VACCINECENTER_RANGE)
                        self.currently_selected_building = 3
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
            elif event.type == self.BUILD_TESTCENTER and not self.mouseover_building_icons:
                if self.money >= 1:
                    t = TestCenter(self)
                else:
                    self.not_enough_money = True
            elif event.type == self.BUILD_HOSTPITAL and not self.mouseover_building_icons:
                if self.money >= 1:
                    h = Hospital(self)
                else:
                    self.not_enough_money = True
            elif event.type == self.BUILD_VACCINECENTER and not self.mouseover_building_icons:
                if self.money >= 1:
                    v = VaccineCenter(self)
                else:
                    self.not_enough_money = True

    # --------------------------------------------
    def eventtriggercheck(self):
        month = self.months[self.date_tracker]
        year = self.year
        week = self.week_counter

        # EVENT 1
        if month == "Maerz" and year == 2020 and week == 2:
            self.time_event_setup(*event01_list)
            self.show_event = True
            # effect
            testcentericon = BuildingIcon(self, "testcenter", 200)
            self.testcenter_unlocked = True

        # EVENT 2
        if month == "Maerz" and year == 2020 and week == 4:
            self.time_event_setup(*event02_list)
            self.show_event = True
            # effect
            self.infect_multiplyer -= 3

        # EVENT 3
        if month == "April" and year == 2020 and week == 1:
            self.time_event_setup(*event03_list)
            self.show_event = True
            # effect
            self.money -= 150

        # EVENT 4
        if month == "April" and year == 2020 and week == 3:
            self.time_event_setup(*event04_list)
            self.show_event = True
            # effect
            self.infect_multiplyer += 2

        # EVENT 5
        if month == "April" and year == 2020 and week == 4:
            self.time_event_setup(*event05_list)
            self.show_event = True
            # effect
            pass

        # EVENT 6
        if month == "Mai" and year == 2020 and week == 1:
            self.time_event_setup(*event06_list)
            self.show_event = True
            # effect
            self.infect_multiplyer += 3

        # EVENT 7
        if month == "Mai" and year == 2020 and week == 3:
            self.time_event_setup(*event07_list)
            self.show_event = True
            # effect
            self.money -= 200

        # EVENT 8
        if month == "Juni" and year == 2020 and week == 2:
            self.time_event_setup(*event08_list)
            self.show_event = True
            # effect
            self.testcenter_range_multiplyer += 0.8

        # EVENT 9
        if month == "Juni" and year == 2020 and week == 4:
            self.time_event_setup(*event09_list)
            self.show_event = True
            # effect
            self.testcenter_range_multiplyer -= 0.2

        # EVENT 10
        if month == "November" and year == 2020 and week == 1:
            self.time_event_setup(*event10_list)
            self.show_event = True
            # effect
            self.infect_multiplyer -= 4

        # EVENT 11
        if month == "Dezember" and year == 2020 and week == 2:
            self.time_event_setup(*event11_list)
            self.show_event = True
            # effect
            self.moneyearning -= 3

        # EVENT 12
        if month == "Dezember" and year == 2020 and week == 4:
            self.time_event_setup(*event12_list)
            self.show_event = True
            # effect
            self.vaccinecenter_unlocked = True
            vaccicon = BuildingIcon(self, "vacc", -200)

        # EVENT 13
        if month == "Februar" and year == 2021 and week == 1:
            self.time_event_setup(*event13_list)
            self.show_event = True
            # effect
            self.vaccinecenter_price = 100
            for sprite in self.building_icons:
                sprite.update_mouseover_text()

        # EVENT 14
        if month == "Maerz" and year == 2021 and week == 1:
            self.time_event_setup(*event14_list)
            self.show_event = True
            # effect
            pass

        # EVENT 15
        if month == "Maerz" and year == 2021 and week == 2:
            self.time_event_setup(*event15_list)
            self.show_event = True
            # effect
            self.vaccinecenter_price = 150
            for sprite in self.building_icons:
                sprite.update_mouseover_text()

        # EVENT 16
        if month == "Maerz" and year == 2021 and week == 3:
            self.time_event_setup(*event16_list)
            self.show_event = True
            # effect
            self.money -= 100
            self.testcenter_range_multiplyer += 0.4

        # EVENT 17
        if month == "April" and year == 2021 and week == 4:
            self.time_event_setup(*event17_list)
            self.show_event = True
            # effect
            self.vaccinecenter_price = 70
            for sprite in self.building_icons:
                sprite.update_mouseover_text()

        # EVENT 18
        if month == "Mai" and year == 2021 and week == 2:
            self.time_event_setup(*event18_list)
            self.show_event = True
            # effect
            self.testcenter_price = 18
            for sprite in self.building_icons:
                sprite.update_mouseover_text()
            self.money -= 80

        # EVENT 19
        if month == "Juni" and year == 2021 and week == 1:
            count_vacc = len(self.vacced.sprites())
            count_hum = len(self.humans.sprites())
            count_inf = len(self.infected.sprites())
            count_need_treatment = len(self.ill.sprites())

            self.percent_vacced = int(count_vacc / count_hum * 100)
            self.percent_infected = int(count_inf / count_hum * 100)
            self.percent_need_treatment = int(count_need_treatment / count_hum * 100)

            EVENT_19_BACKGROUND = "assets/alert_bg.png"
            EVENT_19_HEADLINE = " Ende? "
            EVENT_19_TEXT = str("Dies ist das Ende des Spiels. Du hast insgesamt " + str(self.percent_vacced) + """% \
der Menschen erfolgreich geimpft. Hoffentlich konntest du trotz der Patzer der Regierung dein Budget so \
einteilen, dass möglichst viele Menschen geimpft wurden. 

Leider ist die Realität kein Spiel. Die deutsche Bundesregierung hat durch Profitgier Einzelner und durch \
unverständliche Entscheidungen Anderer viele fatale Fehler gemacht. Viele Menschen sind aufgrund dieser \
Ereignisse erkrankt und einige davon verstorben. Jedes Leben verdient es gerettet zu werden. \
In einer Krisenzeit wie dieser wünsche ich mir mehr Sorgfalt in den politischen Entscheidungen.
(Gleich werden dir weitere Spielstatistiken angezeigt.)""")
            EVENT_19_PICTURE = "assets/eventicons/info_icon.png"
            event19_list = [EVENT_19_BACKGROUND, EVENT_19_HEADLINE,
                            EVENT_19_TEXT, EVENT_19_PICTURE]

            self.time_event_setup(*event19_list)
            self.show_event = True
            # effect
            self.show_endscreen = True

        if self.show_endscreen and not self.show_event:

            EVENT_END_BACKGROUND = "assets/alert_bg.png"
            EVENT_END_HEADLINE = " Statistiken "
            EVENT_END_TEXT = str("Geimpft: " + str(self.percent_vacced) + """%
Infiziert: """ + str(self.percent_infected) + """%
Schwer erkrankt: """ + str(self.percent_need_treatment) + """%

Das Spiel ist zuende. Drücke entweder ESC und beende es, oder spiele im Endlos-Modus weiter.""")
            EVENT_END_PICTURE = "assets/eventicons/info_icon.png"
            eventEND_list = [EVENT_END_BACKGROUND, EVENT_END_HEADLINE,
                             EVENT_END_TEXT, EVENT_END_PICTURE]

            self.time_event_setup(*eventEND_list)
            self.show_event = True
            self.show_endscreen = False

        if self.hospitalunlocked:
            if not self.hospitalunlocked_event_shown:
                self.hospitalunlocked_event_shown = True
                self.time_event_setup(*event_HOSUNLOCK_list)
                self.show_event = True
                hospitalicon = BuildingIcon(self, "hospital", 0)
                self.hospital_unlocked = True

    # --------------------------------------------
    def draw(self):
        self.gamewindow.blit(self.map_img, (self.camera_x, self.camera_y))
        self.humans.draw(self.gamewindow)
        for building in self.buildings:
            building.draw_range()
        for building in self.tempbuildings:
            building.draw_range()
        self.buildings.draw(self.gamewindow)
        self.building_icons.draw(self.gamewindow)
        self.tempbuildings.draw(self.gamewindow)

        for building in self.building_icons:
            building.drawinfotext()  # mouseover


        # show FPS
        if self.show_fps:
            fps = self.font_munro_small.render("FPS: " + str(int(self.clock.get_fps())),
                                               False, pygame.Color(BLACK))
            self.gamewindow.blit(fps, ((WIDTH - 100), 5))

        # draw infect_multiplyer
        multiplyer = self.font_munro_small.render(" Infekt-Multiplikator: x" + str(self.infect_multiplyer / 10) + " ",
                                                  False, pygame.Color(RED), pygame.Color(WHITE))
        self.gamewindow.blit(multiplyer, (25, HEIGHT - 35))

        # draw how many infected
        count_inf = len(self.infected.sprites())
        count_hum = len(self.humans.sprites())
        count_trt = len(self.ill.sprites())
        if self.show_infected:
            perc_inf = self.font_munro_small.render(" " + (str(count_inf) + " of " +
                                                     str(count_hum) + " infected (" +
                                                     str(int(count_inf / count_hum * 100)) +
                                                     " %)"), False, pygame.Color(BLACK))
            self.gamewindow.blit(perc_inf, (25, HEIGHT - 90))
            # print how many in need of medical treatment
            perc_trt = self.font_munro_small.render(" " + (str(count_trt) + " of " +
                                                     str(count_hum) +
                                                     " in need of medical treatment (" +
                                                     str(int(count_trt / count_hum * 100)) +
                                                     " %)"), False, pygame.Color(BLACK))
            self.gamewindow.blit(perc_trt, (25, HEIGHT - 65))

        # show event_text
        if self.show_event:
            self.time_event()

        # draw dated
        self.gamewindow.blit(self.currentdate, (5, 5))

        # draw money & not not_enough_money warning
        self.gamewindow.blit(self.currentmoney, (WIDTH / 2 - self.moneywidth / 2, 5))
        if self.not_enough_money:
            x, y = pygame.mouse.get_pos()
            self.gamewindow.blit(self.not_enough_money_text, (x + 30, y + 10))
            self.not_enough_money_timer += 1
            if self.not_enough_money_timer == (1 * FPS):
                self.not_enough_money = False
                self.not_enough_money_timer = 0

        pygame.display.flip()

    # --------------------------------------------
    def pause_setup(self):
        self.menu_button_list = []
        self.master_volume = DEFAULTVOLUME

        # startup screen
        self.startup_screen_shown = False
        self.title_logo = pygame.image.load("assets/title_logo.png")
        self.title_logo = pygame.transform.scale(self.title_logo, (WIDTH, HEIGHT))
        self.title_logo_rect = self.title_logo.get_rect()
        self.title_logo_rect.center = WIDTH / 2, HEIGHT / 2

        # pause menu
        self.option_default_colour = GREY222
        self.option_highlight_colour = BLACK
        self.option_background_colour = DARKPURPLE

        self.option_continue = Menuoptions(self, " Neues Spiel starten ",0, 0)
        self.option_settings = Menuoptions(self, " Einstellungen ",0, 100)
        self.option_credits = Menuoptions(self, " Credits ", 0, 200)
        self.option_quit = Menuoptions(self, " Spiel Beenden ", 0, 300)

        self.menu_button_list.append(self.option_continue)
        self.menu_button_list.append(self.option_settings)
        self.menu_button_list.append(self.option_credits)
        self.menu_button_list.append(self.option_quit)

        # credits
        self.show_credits = False
        self.creditA = Menuoptions(self, " Ein Spiel von: @FancyGrade ", 0, -100)
        self.creditB = Menuoptions(self, " Mit Musik von: ShadyDave ", 0, 0)
        self.creditC = Menuoptions(self, " Veroeffentlicht: 2021 ", 0, 100)
        self.creditD = Menuoptions(self, " Bildrechte: siehe LICENSE.txt ", 0, 200)

        self.option_back_to_menu = Menuoptions(self, " Zurueck zum Menue ", 0, 400)

        self.menu_button_list.append(self.creditA)
        self.menu_button_list.append(self.creditB)
        self.menu_button_list.append(self.creditC)
        self.menu_button_list.append(self.creditD)
        self.menu_button_list.append(self.option_back_to_menu)

        # setting_values
        self.show_infected = SHOW_INFECTED
        self.show_fps = SHOW_FPS

        # settings
        self.show_settings = False
        self.settingA = Menuoptions(self, " Zeige Infect-Stats: "+ str(self.show_infected) + " ", 0, -200)
        self.settingB = Menuoptions(self, " Zeige FPS: "+ str(self.show_fps) + " ", 0, -100)
        self.settingC = Menuoptions(self, " Lautstaerke: "+ str(round(self.master_volume * 100)) + "% ", 0, 0)
        self.settingC_A = Menuoptions(self, """ << """, self.settingC.get_textobject_rect()[0] *-1 / 2 - 20, 0)
        self.settingC_B = Menuoptions(self, """ >> """, self.settingC.get_textobject_rect()[0] / 2 + 20, 0)
        self.settingD = Menuoptions(self, " Cheat: gebe dir 1000€ ", 0, 100)

        self.menu_button_list.append(self.settingA)
        self.menu_button_list.append(self.settingB)
        self.menu_button_list.append(self.settingC)
        self.menu_button_list.append(self.settingC_A)
        self.menu_button_list.append(self.settingC_B)
        self.menu_button_list.append(self.settingD)

    def draw_pause(self):
        self.gamewindow.blit(self.map_img, (self.camera_x, self.camera_y))
        self.humans.draw(self.gamewindow)
        for building in self.buildings:
            building.draw_range()
        for building in self.tempbuildings:
            building.draw_range()
        self.buildings.draw(self.gamewindow)
        self.tempbuildings.draw(self.gamewindow)

        # draw background only at first start
        if not self.startup_screen_shown:
            self.gamewindow.fill(GREY50)
            self.gamewindow.blit(self.title_logo, self.title_logo_rect)

        if not self.show_credits and not self.show_settings:
            if self.option_continue.draw_text():
                if not self.startup_screen_shown:
                    self.option_continue.update_text(" Spiel fortsetzen ")
                    # show welcome event
                    self.time_event_setup(*eventWLCM_list)
                    self.show_event = True
                    self.startup_screen_shown = True
                self.show_menu = not self.show_menu

            if self.option_settings.draw_text():
                self.show_settings = True

            if self.option_credits.draw_text():
                self.show_credits = True

            if self.option_quit.draw_text():
                pygame.quit()
                sys.exit()

        elif self.show_credits:
            self.gamewindow.blit(self.creditA.get_textobject(), self.creditA.get_textobject_rect())
            self.gamewindow.blit(self.creditB.get_textobject(), self.creditB.get_textobject_rect())
            self.gamewindow.blit(self.creditC.get_textobject(), self.creditC.get_textobject_rect())
            self.gamewindow.blit(self.creditD.get_textobject(), self.creditD.get_textobject_rect())

        elif self.show_settings:
            if self.settingA.draw_text():
                self.show_infected = not self.show_infected
                self.settingA.update_text(" Zeige Infect-Stats: "+ str(self.show_infected) + " ")

            if self.settingB.draw_text():
                self.show_fps = not self.show_fps
                self.settingB.update_text(" Zeige FPS: " + str(self.show_fps) + " ")

            self.gamewindow.blit(self.settingC.get_textobject(), self.settingC.get_textobject_rect())
            self.gamewindow.blit(self.settingC_B.get_textobject(), self.settingC_B.get_textobject_rect())

            if self.settingC_A.draw_text():
                if self.master_volume > 0:
                    self.master_volume = round(self.master_volume - 0.05, 2)
                    self.change_master_sound()
                self.settingC.update_text(" Lautstaerke: "+ str(round(self.master_volume * 100)) + "% ")

            if self.settingC_B.draw_text():
                if self.master_volume < 1:
                    self.master_volume = round(self.master_volume + 0.05, 2)
                    self.change_master_sound()
                self.settingC.update_text(" Lautstaerke: "+ str(round(self.master_volume * 100)) + "% ")

            if self.settingD.draw_text():
                self.money += 1000

        if self.show_settings or self.show_credits:
            if self.option_back_to_menu.draw_text():
                self.show_credits = False
                self.show_settings = False

        pygame.display.flip()

    # --------------------------------------------
    def show_gameover_screen(self):  # TODO: add end screen
        pass


g = Game()

while g.running:
    g.new()
    g.show_gameover_screen()

pygame.quit()
sys.exit()
