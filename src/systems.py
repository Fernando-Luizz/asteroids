
# ASTEROIDE SINGLEPLAYER v1.0
# This file coordinates world state, spawning, collisions, scoring, and progression.

import math
from random import uniform
import random
import pygame as pg

import config as C
from sprites import Asteroid, Explosion, ShieldPickup, Ship, UFO, WeaponPickup
from utils import Vec, rand_edge_pos, rand_unit_vec


class World:
    # Initialize the world state, entity groups, timers, and player progress.
    def __init__(self):
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2))
        self.bullets = pg.sprite.Group()
        self.ufo_bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        self.pickups = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group(self.ship)
        self.weapon_pickups = pg.sprite.Group()
        self._weapon_spawn_cap = C.WEAPON_MAX_PICKUPS
        self.score = 0
        self.lives = C.START_LIVES
        self.wave = 0
        self.wave_cool = C.WAVE_DELAY
        self.safe = C.SAFE_SPAWN_TIME
        self.ufo_timer = C.UFO_SPAWN_EVERY
        self.game_over = False  # Sinaliza fim de jogo para a cena principal
        self.combo_timer = 0.0
        self.combo_chain = 0
        self._shield_quota_remaining = 0
        self._shield_spawn_cap = 2
        self._shield_spawn_timer = 0.0
        

    def start_wave(self):
        # Spawn a new asteroid wave with difficulty based on the current round.
        self.wave += 1
        count = 3 + self.wave
        for _ in range(count):
            pos = rand_edge_pos()
            while (pos - self.ship.pos).length() < 150:
                pos = rand_edge_pos()
            ang = uniform(0, math.tau)
            speed = uniform(C.AST_VEL_MIN, C.AST_VEL_MAX)
            vel = Vec(math.cos(ang), math.sin(ang)) * speed
            self.spawn_asteroid(pos, vel, "L")
        self._shield_quota_remaining = 1 if self.wave <= 3 else 2
        self._shield_spawn_cap = 1 if self.wave <= 3 else C.SHIELD_MAX_PICKUPS
        self._shield_spawn_timer = uniform(
            C.SHIELD_SPAWN_DELAY_MIN, C.SHIELD_SPAWN_DELAY_MAX
        )

    def _random_shield_pickup_pos(self) -> Vec | None:
        others = [p.pos for p in self.pickups]
        for _ in range(100):
            pos = Vec(uniform(60, C.WIDTH - 60), uniform(60, C.HEIGHT - 60))
            if (pos - self.ship.pos).length() < 160:
                continue
            if all((pos - op).length() >= C.SHIELD_PICKUP_SEPARATION for op in others):
                return pos
        return None

    def _spawn_one_shield_pickup(self) -> bool:
        pos = self._random_shield_pickup_pos()
        if pos is None:
            return False
        p = ShieldPickup(pos)
        self.pickups.add(p)
        self.all_sprites.add(p)
        return True

    def _tick_shield_pickup_spawns(self, dt: float):
        if self._shield_quota_remaining <= 0:
            return
        self._shield_spawn_timer -= dt
        if self._shield_spawn_timer > 0:
            return
        if len(self.pickups) >= self._shield_spawn_cap:
            self._shield_spawn_timer = 0.25
            return
        if not self._spawn_one_shield_pickup():
            self._shield_spawn_timer = 0.35
            return
        self._shield_quota_remaining -= 1
        if self._shield_quota_remaining > 0:
            self._shield_spawn_timer = uniform(
                C.SHIELD_SPAWN_DELAY_MIN, C.SHIELD_SPAWN_DELAY_MAX
            )
    def _try_spawn_weapon_pickup(self, pos: Vec):
        # Tries to drop a WeaponPickup near the specified coordinates upon Large asteroid destruction.
        import random
        if random.random() > C.WEAPON_PICKUP_CHANCE:
            return
        if len(self.weapon_pickups) >= self._weapon_spawn_cap:
            return
        # Verifica separação mínima
        for p in self.weapon_pickups:
            if (p.pos - pos).length() < C.WEAPON_PICKUP_SEPARATION:
                return
        wp = WeaponPickup(pos)
        self.weapon_pickups.add(wp)
        self.all_sprites.add(wp)

    def spawn_asteroid(self, pos: Vec, vel: Vec, size: str, explosive: bool = False):
        # Create an asteroid and register it in the world groups.

        if not explosive and size in ("L", "M"):
            explosive = random.random() < C.EXPLOSIVE_CHANCE
        a = Asteroid(pos, vel, size, explosive=explosive)
        self.asteroids.add(a)
        self.all_sprites.add(a)

    def _trigger_explosion(self, pos: Vec):
        # Triggers a shockwave explosion at the given position.
        exp = Explosion(pos)
        self.explosions.add(exp)
        self.all_sprites.add(exp)
        for ast in list(self.asteroids):
            if (ast.pos - pos).length() < C.EXPLOSION_RADIUS:
                self.split_asteroid(ast)
        # Dano na nave (sem escudo)
        if (self.ship.pos - pos).length() < C.EXPLOSION_RADIUS:
            if self.ship.invuln <= 0 and self.ship.shield_time <= 0 and self.safe <= 0:
                self.ship_die()
    def spawn_ufo(self):
        # Spawn a single UFO at a screen edge and send it across the playfield.
        if self.ufos:
            return
        small = uniform(0, 1) < 0.5
        y = uniform(0, C.HEIGHT)
        x = 0 if uniform(0, 1) < 0.5 else C.WIDTH
        ufo = UFO(Vec(x, y), small)
        ufo.dir.xy = (1, 0) if x == 0 else (-1, 0)
        self.ufos.add(ufo)
        self.all_sprites.add(ufo)

    def ufo_try_fire(self):
        # Let every active UFO attempt to fire at the ship.
        for ufo in self.ufos:
            bullet = ufo.fire_at(self.ship.pos)
            if bullet:
                self.ufo_bullets.add(bullet)
                self.all_sprites.add(bullet)

    def try_fire(self):
        # Fire a player bullet when the bullet cap allows it.
        max_b = (C.WEAPON_RAPID_MAX_BULLETS
                if self.ship.weapon_mode == "rapid"
                else C.MAX_BULLETS)
        if len(self.bullets) >= max_b:
            return
        bullets = self.ship.fire()
        for b in bullets:
            self.bullets.add(b)
            self.all_sprites.add(b)

    def hyperspace(self):
        # Trigger the ship hyperspace action and apply its score penalty.
        self.ship.hyperspace()
        self.score = max(0, self.score - C.HYPERSPACE_COST)
        self._reset_combo()

    def _reset_combo(self):
        self.combo_timer = 0.0
        self.combo_chain = 0

    def _add_combo_kill_score(self, base: int) -> None:
        if self.combo_timer > 0:
            self.combo_chain += 1
        else:
            self.combo_chain = 1
        self.combo_chain = min(self.combo_chain, C.COMBO_MAX_MULT)
        self.combo_timer = C.COMBO_WINDOW
        self.score += base * self.combo_chain

    def _weapon_pickup_collisions(self):
        for wp in list(self.weapon_pickups):
            if (wp.pos - self.ship.pos).length() < (wp.r + self.ship.r):
                self.ship.apply_weapon(wp.mode)
                wp.kill()
    def update(self, dt: float, keys):
        # Update the world simulation, timers, enemy behavior, and progression.
        self.ship.control(keys, dt)
        self.all_sprites.update(dt)
        if self.safe > 0:
            self.safe -= dt
            self.ship.invuln = 0.5
        if self.ufos:
            self.ufo_try_fire()
        else:
            self.ufo_timer -= dt
        if not self.ufos and self.ufo_timer <= 0:
            self.spawn_ufo()
            self.ufo_timer = C.UFO_SPAWN_EVERY

        self.handle_collisions()
        self._pickup_collisions()
        self._weapon_pickup_collisions()
        self._tick_shield_pickup_spawns(dt)

        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self._reset_combo()

        if not self.asteroids and self.wave_cool <= 0:
            self.start_wave()
            self.wave_cool = C.WAVE_DELAY
        elif not self.asteroids:
            self.wave_cool -= dt

    def handle_collisions(self):
        # Resolve collisions between bullets, asteroids, UFOs, and the ship.
        hits = pg.sprite.groupcollide(
            self.asteroids,
            self.bullets,
            False,
            True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r,
        )
        for ast, _ in hits.items():
            self.split_asteroid(ast)

        ufo_hits = pg.sprite.groupcollide(
            self.asteroids,
            self.ufo_bullets,
            False,
            True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r,
        )
        for ast, _ in ufo_hits.items():
            self.split_asteroid(ast)

        if self.ship.invuln <= 0 and self.safe <= 0 and self.ship.shield_time <= 0:
            for ast in self.asteroids:
                if (ast.pos - self.ship.pos).length() < (ast.r + self.ship.r):
                    self.ship_die()
                    break
            for ufo in self.ufos:
                if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                    self.ship_die()
                    break
            for bullet in self.ufo_bullets:
                if (bullet.pos - self.ship.pos).length() < (bullet.r + self.ship.r):
                    bullet.kill()
                    self.ship_die()
                    break

        for ufo in list(self.ufos):
            for b in list(self.bullets):
                if (ufo.pos - b.pos).length() < (ufo.r + b.r):
                    score = (C.UFO_SMALL["score"] if ufo.small
                             else C.UFO_BIG["score"])
                    self._add_combo_kill_score(score)
                    ufo.kill()
                    b.kill()

    def _pickup_collisions(self):
        for p in list(self.pickups):
            if (p.pos - self.ship.pos).length() < (p.r + self.ship.r):
                self.ship.shield_time = max(self.ship.shield_time, C.SHIELD_DURATION)
                p.kill()

    def split_asteroid(self, ast: Asteroid):
        # Destroy an asteroid, award score, and spawn its smaller fragments.
        self._add_combo_kill_score(C.AST_SIZES[ast.size]["score"])
        split = C.AST_SIZES[ast.size]["split"]
        pos = Vec(ast.pos)
        was_explosive = ast.explosive
        ast.kill()
        for s in split:
            dirv = rand_unit_vec()
            speed = uniform(C.AST_VEL_MIN, C.AST_VEL_MAX) * 1.2
            self.spawn_asteroid(pos, dirv * speed, s)
        if was_explosive:
            self._trigger_explosion(pos)
        if ast.size == "L":                     
            self._try_spawn_weapon_pickup(pos)  

    def ship_die(self):
        # Remove uma vida; sinaliza game over ou reposiciona a nave.
        self._reset_combo()
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True  # Game.run() detecta e muda de cena
            return
        self.ship.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
        self.ship.vel.xy = (0, 0)
        self.ship.angle = -90
        self.ship.shield_time = 0.0
        self.ship.invuln = C.SAFE_SPAWN_TIME
        self.safe = C.SAFE_SPAWN_TIME

    def draw(self, surf: pg.Surface, font: pg.font.Font):
        # Draw all world entities and the current HUD information.
        for spr in self.all_sprites:
            spr.draw(surf)

        pg.draw.line(surf, (60, 60, 60), (0, 50), (C.WIDTH, 50), width=1)
        txt = f"SCORE {self.score:06d}   LIVES {self.lives}   WAVE {self.wave}"
        label = font.render(txt, True, C.WHITE)
        surf.blit(label, (10, 10))

        if self.combo_chain >= 2 and self.combo_timer > 0:
            cl = font.render(f"COMBO x{self.combo_chain}", True, C.COMBO_COLOR)
            surf.blit(cl, (10, 28))
            bw = max(1, int(100 * (self.combo_timer / C.COMBO_WINDOW)))
            pg.draw.rect(surf, C.COMBO_COLOR, (10, 48, bw, 4))

        # HUD do power-up de arma
        if self.ship.weapon_mode and self.ship.weapon_time > 0:
            mode_names = {"double": "DUPLO", "triple": "TRIPLO", "rapid": "RAPIDO"}
            name = mode_names.get(self.ship.weapon_mode, "")
            wl = font.render(f"ARMA: {name}  {self.ship.weapon_time:.1f}s",
                            True, C.WEAPON_PICKUP_COLOR)
            surf.blit(wl, (C.WIDTH - wl.get_width() - 10, 10))
            bw = max(1, int(150 * (self.ship.weapon_time / C.WEAPON_DURATION)))
            pg.draw.rect(surf, C.WEAPON_PICKUP_COLOR,
                        (C.WIDTH - bw - 10, 48, bw, 4))