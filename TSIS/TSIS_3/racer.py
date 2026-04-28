import pygame, sys, random
from pygame.locals import *

SCREEN_W, SCREEN_H = 400, 600
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (220, 0,   0)
GREEN  = (0,   200, 0)
BLUE   = (0,   100, 220)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GRAY   = (150, 150, 150)
DARK   = (60,  60,  60)
PURPLE = (160, 0,   200)

CAR_COLORS = {"red": RED, "blue": BLUE, "green": GREEN}

DIFFICULTY = {
    "easy":   {"speed": 3, "enemies": 2},
    "medium": {"speed": 5, "enemies": 3},
    "hard":   {"speed": 7, "enemies": 5},
}


def _load(path, size):
    """Load image or fall back to a gray rectangle."""
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill(GRAY)
        return surf


# ── Sprites ──────────────────────────────────────────────────────────────────

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.color = CAR_COLORS.get(color_name, BLUE)
        img = _load("my_car.png", (60, 100))
        # tint the fallback rectangle with chosen color
        if img.get_at((0, 0)) == (*GRAY, 255):
            img.fill(self.color)
        self.image = img
        self.rect  = self.image.get_rect(center=(160, 520))
        self.shield    = False
        self.oil_timer = 0   # ms of slow-debuff remaining

    def move(self):
        keys = pygame.key.get_pressed()
        spd  = 2 if self.oil_timer > 0 else 5
        if self.rect.left  > 0         and keys[K_LEFT]:
            self.rect.move_ip(-spd, 0)
        if self.rect.right < SCREEN_W  and keys[K_RIGHT]:
            self.rect.move_ip(spd, 0)

    def tick(self, dt):
        if self.oil_timer > 0:
            self.oil_timer = max(0, self.oil_timer - dt)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        img = _load("enemy_car.png", (60, 100))
        if img.get_at((0, 0)) == (*GRAY, 255):
            img.fill(RED)
        self.image = img
        self.rect  = self.image.get_rect()
        self.speed = speed
        self._place(top=True)

    def _place(self, top=False):
        y = random.randint(-300, -60) if not top else random.randint(-600, -60)
        self.rect.center = (random.randint(40, SCREEN_W - 40), y)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_H:
            self._place()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed, worth=1):
        super().__init__()
        self.worth = worth
        self.speed = speed
        if worth == 1:
            img = _load("coin.png", (36, 36))
            if img.get_at((0, 0)) == (*GRAY, 255):
                img = pygame.Surface((36, 36), pygame.SRCALPHA)
                pygame.draw.circle(img, YELLOW, (18, 18), 18)
        else:
            # diamond visual
            img = pygame.Surface((44, 44), pygame.SRCALPHA)
            pygame.draw.polygon(img, (0, 200, 255),
                                [(22, 0), (44, 22), (22, 44), (0, 22)])
        self.image = img
        self.rect  = self.image.get_rect()
        self._place()

    def _place(self):
        self.rect.center = (random.randint(30, SCREEN_W - 30),
                            random.randint(-300, -40))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_H:
            self._place()


class OilSpill(pygame.sprite.Sprite):
    """Slow the player for 2 seconds."""
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((80, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (20, 20, 20, 200), (0, 0, 80, 28))
        self.rect = self.image.get_rect()
        self._place()

    def _place(self):
        self.rect.center = (random.randint(50, SCREEN_W - 50),
                            random.randint(-600, -100))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_H:
            self._place()


class Pothole(pygame.sprite.Sprite):
    """Instant game-over hazard unless player has shield."""
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((50, 24), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (40, 25, 10, 220), (0, 0, 50, 24))
        self.rect = self.image.get_rect()
        self._place()

    def _place(self):
        self.rect.center = (random.randint(40, SCREEN_W - 40),
                            random.randint(-800, -200))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_H:
            self._place()


class SpeedBump(pygame.sprite.Sprite):
    """Road event: brief slow when crossed."""
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((SCREEN_W - 40, 14))
        self.image.fill(DARK)
        self.rect = self.image.get_rect()
        self._place()

    def _place(self):
        self.rect.center = (SCREEN_W // 2, random.randint(-900, -300))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_H:
            self._place()


class NitroStrip(pygame.sprite.Sprite):
    """Road event: brief speed boost when crossed."""
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((120, 16))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self._place()

    def _place(self):
        self.rect.center = (SCREEN_W // 2, random.randint(-700, -200))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_H:
            self._place()


class MovingBarrier(pygame.sprite.Sprite):
    """Road event: moves left-right, kills unless shield."""
    def __init__(self, speed):
        super().__init__()
        self.vspeed = speed
        self.hspeed = 3
        self.image = pygame.Surface((70, 18))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self._place()

    def _place(self):
        self.rect.center = (random.randint(80, SCREEN_W - 80),
                            random.randint(-600, -100))

    def update(self):
        self.rect.move_ip(self.hspeed, self.vspeed)
        if self.rect.left < 0 or self.rect.right > SCREEN_W:
            self.hspeed *= -1
        if self.rect.top > SCREEN_H:
            self._place()


class PowerUp(pygame.sprite.Sprite):
    """Collectible power-up that disappears after 8 seconds if not grabbed."""
    COLORS = {"nitro": YELLOW, "shield": BLUE, "repair": GREEN}
    LABELS = {"nitro": "N",    "shield": "S",  "repair": "R"}

    def __init__(self, ptype, speed):
        super().__init__()
        self.ptype  = ptype
        self.speed  = speed
        self.age    = 0        # ms alive
        self.image  = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.COLORS[ptype], (20, 20), 20)
        lbl = pygame.font.SysFont("Verdana", 18, bold=True).render(
            self.LABELS[ptype], True, BLACK)
        self.image.blit(lbl, lbl.get_rect(center=(20, 20)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_W - 30),
                            random.randint(-200, -60))

    def update(self, dt=16):
        self.rect.move_ip(0, self.speed)
        self.age += dt
        if self.rect.top > SCREEN_H or self.age > 8000:
            self.kill()


# ── Main game session ─────────────────────────────────────────────────────────

def run_game(screen, settings, username):
    """
    Run one game. Returns (score, distance, coins).
    score = coins + distance//10
    """
    clock  = pygame.time.Clock()
    diff   = DIFFICULTY[settings.get("difficulty", "medium")]
    speed0 = diff["speed"]
    sound  = settings.get("sound", True)

    font_s = pygame.font.SysFont("Verdana", 20)
    font_m = pygame.font.SysFont("Verdana", 28)

    # Background
    try:
        bg = pygame.transform.scale(
            pygame.image.load("AnimatedStreet.jpg"), (SCREEN_W, SCREEN_H))
    except:
        bg = None
    bg_y = 0

    # Create sprites
    player   = Player(settings.get("car_color", "blue"))
    enemies  = pygame.sprite.Group(
        *[Enemy(speed0) for _ in range(diff["enemies"])])
    coins    = pygame.sprite.Group(Coin(speed0))
    oils     = pygame.sprite.Group(OilSpill(speed0))
    holes    = pygame.sprite.Group(Pothole(speed0))
    bumps    = pygame.sprite.Group(SpeedBump(speed0))
    nstrips  = pygame.sprite.Group(NitroStrip(speed0))
    barriers = pygame.sprite.Group(MovingBarrier(speed0))
    powerups = pygame.sprite.Group()

    hazard_groups = [enemies, oils, holes, bumps, nstrips, barriers]
    all_moving    = [enemies, coins, oils, holes, bumps, nstrips, barriers, powerups]

    # Event timers
    DIAMOND_EV = pygame.USEREVENT + 1
    POWERUP_EV = pygame.USEREVENT + 2
    pygame.time.set_timer(DIAMOND_EV, 5000)
    pygame.time.set_timer(POWERUP_EV, 7000)

    COINS        = 0
    distance     = 0
    active_pu    = None   # "nitro" | "shield" | "repair" | None
    nitro_timer  = 0      # ms remaining for nitro boost
    road_nitro   = 0      # ms remaining for road nitro strip boost

    running = True
    while running:
        # dt in seconds (e.g., 0.016)
        dt = clock.tick(60) / 1000.0 
        # distance increases smoothly
        distance += 10 * dt  #
        distance = round(distance, 1) #fixed bug by rounding number to 1 and multiplicating to 10

        speed = speed0 + COINS // 10 #starting to increase speed when we gain 10 coins
        if nitro_timer > 0 or road_nitro > 0:
            speed = int(speed * 1.6)

        # ── Events ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == DIAMOND_EV:
                d = Coin(speed, worth=5)
                coins.add(d)
            if event.type == POWERUP_EV:
                pu = PowerUp(random.choice(["nitro", "shield", "repair"]), speed)
                powerups.add(pu)

        # ── Update timers & player ────────────────────────────────────────────
        if nitro_timer > 0:
            nitro_timer = max(0, nitro_timer - dt)
            if nitro_timer == 0:
                active_pu = None
        if road_nitro > 0:
            road_nitro = max(0, road_nitro - dt)

        player.tick(dt)
        player.move()

        # Sync speed on all moving sprites
        for grp in all_moving:
            for s in grp:
                s.speed = speed

        # Update all moving sprites (pass dt to powerups)
        for grp in [enemies, coins, oils, holes, bumps, nstrips, barriers]:
            for s in grp:
                s.update()
        for pu in list(powerups):
            pu.update(dt)

        # ── Draw ─────────────────────────────────────────────────────────────
        if bg:
            bg_y = (bg_y + speed) % SCREEN_H
            screen.blit(bg, (0, bg_y - SCREEN_H))
            screen.blit(bg, (0, bg_y))
        else:
            screen.fill((50, 50, 50))
            for y in range(bg_y % 80, SCREEN_H, 80):
                pygame.draw.rect(screen, WHITE, (195, y, 10, 50))

        for grp in [oils, holes, bumps, nstrips, barriers, coins, powerups, enemies]:
            grp.draw(screen)
        screen.blit(player.image, player.rect)

        # Shield indicator ring
        if player.shield:
            pygame.draw.circle(screen, BLUE, player.rect.center, 38, 3)

        # HUD bar
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_W, 38))
        screen.blit(font_s.render(
            f"Coins:{COINS}  Dist:{distance}m  Spd:{speed}", True, WHITE), (5, 10))
        if active_pu == "nitro":
            screen.blit(font_s.render(
                f"NITRO {nitro_timer//1000+1}s", True, YELLOW), (SCREEN_W-100, 10))
        elif player.shield:
            screen.blit(font_s.render("SHIELD", True, BLUE), (SCREEN_W-80, 10))

        # ── Collision checks ─────────────────────────────────────────────────

        def fatal_hit(sprite_group):
            """Return True (and handle shield) if player collides with group."""
            hits = pygame.sprite.spritecollide(player, sprite_group, False)
            if hits:
                if player.shield:
                    player.shield = False
                    for h in hits:
                        h._place()   # push hazard away
                    return False
                return True
            return False

        if fatal_hit(enemies) or fatal_hit(holes) or fatal_hit(barriers):
            if sound:
                try:
                    pygame.mixer.Sound('crash.mpeg').play()
                    pygame.time.wait(500)
                except:
                    pass
            pygame.time.set_timer(DIAMOND_EV, 0)
            pygame.time.set_timer(POWERUP_EV, 0)
            score = COINS + distance // 10
            return score, distance, COINS

        # Oil spill → slow
        if pygame.sprite.spritecollideany(player, oils):
            player.oil_timer = max(player.oil_timer, 2000)

        # Speed bump → brief slow
        if pygame.sprite.spritecollideany(player, bumps):
            player.oil_timer = max(player.oil_timer, 500)

        # Nitro strip → speed boost
        if pygame.sprite.spritecollideany(player, nstrips):
            road_nitro = max(road_nitro, 2000)

        # Coin / diamond collection
        for coin in pygame.sprite.spritecollide(player, coins, False):
            COINS += coin.worth
            coin._place()

        # Power-up collection
        for pu in pygame.sprite.spritecollide(player, powerups, True):
            if pu.ptype == "nitro":
                nitro_timer = 4000
                active_pu   = "nitro"
            elif pu.ptype == "shield":
                player.shield = True
                active_pu     = "shield"
            elif pu.ptype == "repair":
                if player.oil_timer > 0:
                    player.oil_timer = 0   # clear slow debuff
                else:
                    player.shield = True   # act as shield
                active_pu = "repair"

        pygame.display.update()

    pygame.time.set_timer(DIAMOND_EV, 0)
    pygame.time.set_timer(POWERUP_EV, 0)
    score = COINS + distance // 10
    return score, distance, COINS
