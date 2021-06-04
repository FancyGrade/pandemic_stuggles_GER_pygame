# define variables for final stats
percent_vacced = None
percent_infected = None
percent_need_treatment = None


# No Money
EVENT_MN_BACKGROUND = "assets/alert_bg.png"
EVENT_MN_HEADLINE = " Budget aufgebraucht! "
EVENT_MN_TEXT = "Das Gesundheitsministerium hat nur ein begrenztes Budget. \
Du findest es oben mittig auf deinem Bildschirm. Du bekommst jede Woche \
einen festen Betrag gutgeschrieben, aber wenn dein Budget unter \
0 fällt, kannst du keine weiteren Gebäude mehr bauen. \
Einige Ereignisse können sich negativ auf dein Einkommen auswirken, \
stell also sicher, \
dass du immer noch eine eiserne Reserve für Notfälle übriglässt."
EVENT_MN_PICTURE = "assets/eventicons/info_icon.png"
eventMN_list = [EVENT_MN_BACKGROUND, EVENT_MN_HEADLINE,
                EVENT_MN_TEXT, EVENT_MN_PICTURE]

# Hospitalunlock
EVENT_HOSUNLOCK_BACKGROUND = "assets/alert_bg.png"
EVENT_HOSUNLOCK_HEADLINE = " Infektion entdeckt! "
EVENT_HOSUNLOCK_TEXT = """Eins deiner Testzentren hat eine kranke Person entdeckt. Du erkennst kranke Personen an ihrer roten Farbe. Baue ein Krankenhaus, um die Person zu heilen. Aber pass auf: Das Gesundheitsministerium hat nur ein begrenztes Budget. 

Beachte: Menschen können schwer erkranken, wenn sie infiziert sind und längere Zeit nicht behandelt werden. Schwer Erkrankte erkennst du an ihrer dunkleren Farbe. Du kannst sie in einem Krankenhaus heilen. Schwer erkrankte Personen wirken sich nur auf deine End-Statistiken aus.

Effekt: Krankenhaus freigeschaltet."""
EVENT_HOSUNLOCK_PICTURE = "assets/buildingicons/hospital_scaled.png"
event_HOSUNLOCK_list = [EVENT_HOSUNLOCK_BACKGROUND, EVENT_HOSUNLOCK_HEADLINE,
                EVENT_HOSUNLOCK_TEXT, EVENT_HOSUNLOCK_PICTURE]

# Welcome message
EVENT_WLCM_BACKGROUND = "assets/alert_bg.png"
EVENT_WLCM_HEADLINE = " Willkommen! "
EVENT_WLCM_TEXT = """Du bist von der Bundesregierung beauftragt worden die Coronapandemie in Deutschland einzudämmen. Achte darauf, dass alle Menschen (Kreise) gesund bleiben. Im Laufe der Pandemie wird es regelmäßig Ereignisse geben, die dir bei der Bekämpfung der Pandemie helfen oder dich dabei behindern können.

Bitte beachte: Die Zeiträume dieser Ereignisse wurden in einigen Fällen aus Gameplay-Gründen leicht angepasst.

Steuerung: WASD für die Kamera, ESC für das Pause Menü, Hotkeys 1-3 für Gebäude (nachdem sie freigeschaltet wurden)"""
EVENT_WLCM_PICTURE = "assets/eventicons/info_icon.png"
eventWLCM_list = [EVENT_WLCM_BACKGROUND, EVENT_WLCM_HEADLINE,
                  EVENT_WLCM_TEXT, EVENT_WLCM_PICTURE]


# 01
EVENT_01_BACKGROUND = "assets/alert_bg.png"
EVENT_01_HEADLINE = " Erste Infektionen "
EVENT_01_TEXT = """Die Gerüchte aus dem Ausland sind wahr: Es wurden die ersten Infektionen in den Nachbarländern festgestellt. Vermutlich ist auch die deutsche Bevölkerung betroffen. Ein Team des Deutschen Zentrums für Infektionsforschung hat ein Testverfahren entwickelt, welches allerdings noch sehr kostspielig ist.
Baue Testzentren, um Infektionsherde in einzelnen Regionen zu lokalisieren.

Effekt: Testzentrum freigeschaltet."""
EVENT_01_PICTURE = "assets/buildingicons/testcenter_scaled.png"
event01_list = [EVENT_01_BACKGROUND, EVENT_01_HEADLINE,
                EVENT_01_TEXT, EVENT_01_PICTURE]

# 02
EVENT_02_BACKGROUND = "assets/alert_bg.png"
EVENT_02_HEADLINE = " Schulbetrieb geschlossen "
EVENT_02_TEXT = """Die Infektionen breiten sich weiter aus. Der Schulbetrieb wird in einigen Bundesländern ausgesetzt. Andere Länder werden demnächst nachziehen.

Effekt: Die Infektionsgefahr sinkt leicht."""
EVENT_02_PICTURE = "assets/eventicons/school_chair.png"
event02_list = [EVENT_02_BACKGROUND, EVENT_02_HEADLINE,
                EVENT_02_TEXT, EVENT_02_PICTURE]

# 03
EVENT_03_BACKGROUND = "assets/alert_bg.png"
EVENT_03_HEADLINE = " Maskenkauf unter der Hand "
EVENT_03_TEXT = """Die Wissenschaft ist sich inzwischen einig: FFP2 Masken schützen nachweislich vor einem Infekt mit dem Virus. Da die Nachfrage hoch ist, kauft das Gesundheitsministerium ca. 60 Millionen Masken. Einige Beteiligte sahen die Chance, sich an der Pandemie zu bereichern und bestellten weitere 67 Millionen Masken ohne das Angebot vorher öffentlich auszuschreiben. "Zufällig" waren diese 67 Millionen Masken auch deutlich teurer im Einkauf. 

Effekt: Einige der Mehrkosten werden auf dein Budget umgewälzt, du verlierst 150€."""
EVENT_03_PICTURE = "assets/eventicons/mask_icon.png"
event03_list = [EVENT_03_BACKGROUND, EVENT_03_HEADLINE,
                EVENT_03_TEXT, EVENT_03_PICTURE]


# 04
EVENT_04_BACKGROUND = "assets/alert_bg.png"
EVENT_04_HEADLINE = " Schuloeffnungen als Experiment "
EVENT_04_TEXT = """Laut Einschätzungen des RKI wird das Virus in Schulen durch den engen Kontakt zwischen Lehrern und Schülern verbreitet. Genaue Studien dazu fehlen allerdings noch. Trotzdem entscheiden sich Landesregierungen dazu, den Schulbetrieb größtenteils wieder aufzunehmen, auch die bevorstehenden Abiturprüfungen sollen stattfinden. Was kann schon schiefgehen? Sind doch nur Kinder.

Effekt: Die Infektionsgefahr steigt leicht."""
EVENT_04_PICTURE = "assets/eventicons/school_chair.png"
event04_list = [EVENT_04_BACKGROUND, EVENT_04_HEADLINE,
                EVENT_04_TEXT, EVENT_04_PICTURE]

# 05
EVENT_05_BACKGROUND = "assets/alert_bg.png"
EVENT_05_HEADLINE = " Keine Masken fuer Sozialschwache "
EVENT_05_TEXT = """Im ÖPNV herrscht Maskenpflicht. Die Masken wirken auch nachweislich, allerdings werden Geringverdiener und ALG-Empfänger nicht unterstützt. Gerade diese Bevölkerungsschicht ist besonders auf den ÖPNV angewiesen. Die Pandemie betrifft sozialschwächere Menschen besonders stark, sie erkranken im Vergleich häufiger. Korrelation oder Kausalität? Interessiert die Bundesregierung auf Nachfrage wenig."""
EVENT_05_PICTURE = "assets/eventicons/mask_icon.png"
event05_list = [EVENT_05_BACKGROUND, EVENT_05_HEADLINE,
                EVENT_05_TEXT, EVENT_05_PICTURE]

# 06
EVENT_06_BACKGROUND = "assets/alert_bg.png"
EVENT_06_HEADLINE = " Schulexperiment gescheitert "
EVENT_06_TEXT = """Es stellt sich heraus: Das Virus verbreitet sich tatsächlich in den Klassenräumen. Zwar zeigen die Schüler nur selten Symptome, aber dafür werden die Eltern und Lehrer infiziert. Die Schulen frühzeitig zu öffnen, das war wohl keine so gute Idee. 

Effekt: Die Infektionsgefahr steigt weiter."""
EVENT_06_PICTURE = "assets/eventicons/school_chair.png"
event06_list = [EVENT_06_BACKGROUND, EVENT_06_HEADLINE,
                EVENT_06_TEXT, EVENT_06_PICTURE]

# 07
EVENT_07_BACKGROUND = "assets/alert_bg.png"
EVENT_07_HEADLINE = " Voll in die Nuesse "
EVENT_07_TEXT = """Die Maskenaffäre ist größer als gedacht: CSU-Politiker Nüsslein und Sauter sollten für diverse Maskendeals mit privaten Unternehmen nach aktuellen Angaben 11,5 Millionen Euro Provision bekommen. Die Provision wurde in klassischer CSU-Manier durch diverse Offshore-Konten geleitet. Während sich andere an der Pandemie bereichern, stehst du weiterhin vor der Herausforderung, Menschenleben mit deinem Budget zu retten. 

Effekt: Aufgrund der Mehrkosten werden dir 200€ abgezogen (Nüsslein und Sauter richten ihren Dank aus)."""
EVENT_07_PICTURE = "assets/eventicons/peanut_icon.png"
event07_list = [EVENT_07_BACKGROUND, EVENT_07_HEADLINE,
                EVENT_07_TEXT, EVENT_07_PICTURE]

# 08
EVENT_08_BACKGROUND = "assets/alert_bg.png"
EVENT_08_HEADLINE = " Corona-Warn-App "
EVENT_08_TEXT = """Endlich! Die Corona-Warn-App wurde nach einiger (berechtigter) Kritik angepasst und eingeführt. 

Effekt: Erhöht die Test-Reichweite dank der App deutlich."""
EVENT_08_PICTURE = "assets/eventicons/Corona-Warn-App_Logo.png"
event08_list = [EVENT_08_BACKGROUND, EVENT_08_HEADLINE,
                EVENT_08_TEXT, EVENT_08_PICTURE]

# 09
EVENT_09_BACKGROUND = "assets/alert_bg.png"
EVENT_09_HEADLINE = " Corona-Warn-App Part 2"
EVENT_09_TEXT = """Die Corona-Warn-App wird aus unerklärlichen Gründen von einem Teil der Bevölkerung abgelehnt. Einige Spitzenpolitiker wie Sahra Wagenknecht sprechen sich öffentlich gehen sie aus, angeblich sind sie besorgt um den Datenschutz. Der Datenschutz der Open Source App wurde allerdings ausführlich von mehreren unabhängigen Parteien überprüft und als sehr gut eingestuft. Uninformierte Politiker wie Wagenknecht lösen unbegründete Sorge in der Bevölkerung aus.

Effekt: Die Test-Reichweite sinkt leicht."""
EVENT_09_PICTURE = "assets/eventicons/Corona-Warn-App_Logo.png"
event09_list = [EVENT_09_BACKGROUND, EVENT_09_HEADLINE,
                EVENT_09_TEXT, EVENT_09_PICTURE]

# 10
EVENT_10_BACKGROUND = "assets/alert_bg.png"
EVENT_10_HEADLINE = " Weitere Schliessungen "
EVENT_10_TEXT = """Aufgrund der steigenden Zahlen wurde die Gastronomie und Tourismusbranche wieder weitgehend geschlossen. Auch die Schulen werden aufgrund der gestiegenen Zahlen wieder geschlossen.

Effekt: Die Infektionsgefahr sinkt."""
EVENT_10_PICTURE = "assets/eventicons/school_chair.png"
event10_list = [EVENT_10_BACKGROUND, EVENT_10_HEADLINE,
                EVENT_10_TEXT, EVENT_10_PICTURE]

# 11
EVENT_11_BACKGROUND = "assets/alert_bg.png"
EVENT_11_HEADLINE = " Laenger Party "
EVENT_11_TEXT = """Diverse Bundesländer haben eine Ausgangssperre ab 21 Uhr verhängt. Illegale Partys müssen jetzt mindestens bis 5 Uhr gehen, damit es keiner merkt. Genial. 

Effekt: Die nötigen Polizeikontrollen sind sehr kostenaufwendig, dein Budget wird um 3€ pro Woche gekürzt."""
EVENT_11_PICTURE = "assets/eventicons/party_emoji.png"
event11_list = [EVENT_11_BACKGROUND, EVENT_11_HEADLINE,
                EVENT_11_TEXT, EVENT_11_PICTURE]

# 12
EVENT_12_BACKGROUND = "assets/alert_bg.png"
EVENT_12_HEADLINE = " Erste Impfungen! "
EVENT_12_TEXT = """Endlich ein Ende in Sicht: Die ersten Impfstoffe sind verfügbar. Noch ist der Impfstoff aber rar. 

Effekt: Impfzentrum freigeschaltet. Ein Impfzentrum kostet 200€."""
EVENT_12_PICTURE = "assets/buildingicons/vacc_scaled.png"
event12_list = [EVENT_12_BACKGROUND, EVENT_12_HEADLINE,
                EVENT_12_TEXT, EVENT_12_PICTURE]

# 13
EVENT_13_BACKGROUND = "assets/alert_bg.png"
EVENT_13_HEADLINE = " Guenstigere Impfungen "
EVENT_13_TEXT = """Die Impfungen laufen langsam an. Inzwischen sind mehrere Impfstoffe verfügbar, und die Kosten für ein Impfzentrum sinken auf 100€"""
EVENT_13_PICTURE = "assets/buildingicons/vacc_scaled.png"
event13_list = [EVENT_13_BACKGROUND, EVENT_13_HEADLINE,
                EVENT_13_TEXT, EVENT_13_PICTURE]

# 14
EVENT_14_BACKGROUND = "assets/alert_bg.png"
EVENT_14_HEADLINE = " Bleib der Corona-Warn-App Troy "
EVENT_14_TEXT = """Der Rapper Smudo startet eine Werbekampagne für einen zweifelhaften Klon der Corona App aus privater Hand. Sie heißt "Luca App". Niemand würde so einen Quatsch ernst nehmen, oder? Oder...?!"""
EVENT_14_PICTURE = "assets/eventicons/luca_app_logo.png"
event14_list = [EVENT_14_BACKGROUND, EVENT_14_HEADLINE,
                EVENT_14_TEXT, EVENT_14_PICTURE]

# 15
EVENT_15_BACKGROUND = "assets/alert_bg.png"
EVENT_15_HEADLINE = " AstraZeneca ausgesetzt "
EVENT_15_TEXT = """Die Impfung mit AstraZeneca wurde ausgesetzt. In einigen seltenen Fällen hat die Impfung eine potentiell tödliche Thrombose ausgelöst. Das Gesundheitsministerium hat sich entschieden den Impfstoff vorerst nicht mehr zu verimpfen.

Effekt: Impfzentren sind 50% teurer, da weniger Impfstoff verfügbar ist."""
EVENT_15_PICTURE = "assets/buildingicons/testcenter_scaled.png"
event15_list = [EVENT_15_BACKGROUND, EVENT_15_HEADLINE,
                EVENT_15_TEXT, EVENT_15_PICTURE]

# 16
EVENT_16_BACKGROUND = "assets/alert_bg.png"
EVENT_16_HEADLINE = " Die App Da!?! "
EVENT_16_TEXT = """Die Luca App geht durch die Decke. Obwohl sie potentiell Code von anderen Projekten geklaut hat, ohne die Herkunft auszuweisen, und obwohl sie aus einer privaten Hand stammt. Obwohl sie Datenschutztechnisch weit hinter der offiziellen Corona App hinterherhinkt und personenbezogene Daten verarbeitet. Mehrere Bundesländer schließen Verträge mit den Herstellern ab und investieren Millionen. Was Smudo gefällt, kann doch nur gut sein.

Effekt: Durch die Mehrausgaben sinkt dein Budget, dir werden 100€ abgezogen. Und die Reichweite der Testcenter steigt leicht, aber zu welchem Preis...? """
EVENT_16_PICTURE = "assets/eventicons/luca_app_logo.png"
event16_list = [EVENT_16_BACKGROUND, EVENT_16_HEADLINE,
                EVENT_16_TEXT, EVENT_16_PICTURE]

# 17
EVENT_17_BACKGROUND = "assets/alert_bg.png"
EVENT_17_HEADLINE = " Zweifelhafte Freigabe von AstraZeneca "
EVENT_17_TEXT = """AstraZeneca ist wieder freigegeben. Die genaue Ursache für die Thrombose ist zwar noch nicht klar, aber der Nutzen überwiegt das Risiko. Die Thrombose tritt hauptsächlich bei Menschen unter 60 auf, deswegen empfiehlt das RKI und die ständige Impfkommission den Impfstoff erst ab 60 Jahren. In der Regierung hat sich vermutlich jemand verlesen, denn aus unerklärlichen Gründen wird dieser Impfstoff als erster auch für Menschen ab 18 Jahren komplett freigegeben.

Effekt: Der Preis für ein Impfzentrum sinkt auf 70€."""
EVENT_17_PICTURE = "assets/buildingicons/testcenter_scaled.png"
event17_list = [EVENT_17_BACKGROUND, EVENT_17_HEADLINE,
                EVENT_17_TEXT, EVENT_17_PICTURE]

# 18
EVENT_18_BACKGROUND = "assets/alert_bg.png"
EVENT_18_HEADLINE = " Goldgraeberstimmung! "
EVENT_18_TEXT = """Überall in Deutschland sprießen kleine Testzentren aus dem Boden. Der Grund: Pro Test erhalten die Betreiber 18 Euro. Nachweise über die durchgeführten Tests sind nicht nötig. Fuck, yeah! Endlich auch für Privatpersonen eine Chance sich an der Pandemie zu bereichern. Bisher war dieses Privileg ja Politikern vorbehalten. Selbst in kleinsten Testzentren werden tausende Tests pro Tag gemeldet, der Spiegel berichtet von großangelegtem Betrug, aber das Gesundheitsministerium ist sich keiner Schuld bewusst.

Effekt: Testzentren kosten jetzt 18 Euro. Außerdem fallen massive Nachzahlungen für die diversen unabhängigen Testzentren an, deinem Budget werden 80€ abgezogen."""
EVENT_18_PICTURE = "assets/eventicons/party_emoji.png"
event18_list = [EVENT_18_BACKGROUND, EVENT_18_HEADLINE,
                EVENT_18_TEXT, EVENT_18_PICTURE]

# MOVED TO MAIN BECAUSE OF INCLUDED VARIABLES
# # 19
# EVENT_19_BACKGROUND = "assets/alert_bg.png"
# EVENT_19_HEADLINE = " Ende? "
# EVENT_19_TEXT = str("Dies ist das Ende des Spiels. Du hast insgesamt " + str(percent_vacced) + """% der Menschen erfolgreich geimpft. Hoffentlich konntest du trotz der Patzer der Regierung dein Budget so einteilen, dass möglichst viele Menschen geimpft wurden.
#
# Leider ist die Realität kein Spiel. Die deutsche Bundesregierung hat durch Profitgier Einzelner und durch unverständliche Entscheidungen anderer viele fatale Fehler gemacht. Viele Menschen sind aufgrund dieser Ereignisse erkrankt und einige davon vermutlich verstorben. Jedes Leben verdient es gerettet zu werden. In einer Krisenzeit wie dieser wünsche ich mir mehr Sorgfalt in den politischen Entscheidungen.""")
# EVENT_19_PICTURE = "assets/eventicons/info_icon.png"
# event19_list = [EVENT_19_BACKGROUND, EVENT_19_HEADLINE,
#                 EVENT_19_TEXT, EVENT_19_PICTURE]
#
# def collect_end_stats(vacced_sprites, human_sprites, infected_sprites, ill_sprites):
#     count_vacc = len(vacced_sprites)
#     count_hum = len(human_sprites)
#     count_inf = len(infected_sprites)
#     count_need_treatment = len(ill_sprites)
#
#     global percent_vacced
#     global percent_infected
#     global percent_need_treatment
#
#     percent_vacced = int(count_vacc / count_hum * 100)
#     percent_infected = int(count_inf / count_hum * 100)
#     percent_need_treatment = int(count_need_treatment / count_hum * 100)
#
# # final stats
# EVENT_END_BACKGROUND = "assets/alert_bg.png"
# EVENT_END_HEADLINE = " Statistiken "
# EVENT_END_TEXT = str("Geimpft: " + str(percent_vacced) + """%
# Infiziert: """ + str(percent_infected) + """%
# Schwer erkrankt: """ + str(percent_need_treatment) + "%")
# EVENT_END_PICTURE = "assets/eventicons/info_icon.png"
# eventEND_list = [EVENT_END_BACKGROUND, EVENT_END_HEADLINE,
#                 EVENT_END_TEXT, EVENT_END_PICTURE]