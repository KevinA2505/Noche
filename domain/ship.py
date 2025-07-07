import pygame
from math import radians


class Ship(pygame.sprite.Sprite):
    """
    Nave con deriva e inercia.
    Norte (arriba) es el ángulo 0°.
    ↑  Impulsa hacia el frente.
    ◄/► Girar.
    """

    def __init__(
        self,
        pos: tuple[int, int],
        image: pygame.Surface | None = None,
        max_speed: float = 5.0,
        friction: float = 0.98,
    ) -> None:
        super().__init__()

        # ─ Imagen ───────────────────────────────────────────────────────
        self.original_image = image or self._create_default_image()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)

        # ─ Cinemática ───────────────────────────────────────────────────
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0.0  # 0° ≡ norte (-Y)

        # ─ Parámetros de control ────────────────────────────────────────
        self.rotation_speed = 180  # grados/segundo
        self.thrust = 0.2
        self.max_speed = max_speed
        self.friction = friction

        # ─ Estela ───────────────────────────────────────────────────────
        self.trail: list[tuple[pygame.Vector2, float]] = []  # (posición, vida)
        self.trail_max_life = 0.6  # s

    # ─ Interfaz pública ────────────────────────────────────────────────
    def update(self, dt: float, screen_rect: pygame.Rect) -> None:
        self._handle_input(dt)
        self._physics_step()
        self._wrap(screen_rect)
        self._update_trail(dt)
        self._apply_rotation()

    def draw(self, surface: pygame.Surface) -> None:
        self._draw_trail(surface)
        surface.blit(self.image, self.rect)

    # ─ Lógica interna ──────────────────────────────────────────────────
    def _handle_input(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.angle -= self.rotation_speed * dt
        if keys[pygame.K_d]:
            self.angle += self.rotation_speed * dt

        # Mantén el ángulo dentro de 0-360 para evitar overflow
        self.angle %= 360

        if keys[pygame.K_w]:
            # Vector norte (0,-1) rotado "angle" grados (horario positivo)
            direction = pygame.Vector2(0, -1).rotate(self.angle)
            self.vel += direction * self.thrust
            if self.vel.length() > self.max_speed:
                self.vel.scale_to_length(self.max_speed)

    def _physics_step(self) -> None:
        self.pos += self.vel
        self.vel *= self.friction
        self.rect.center = self.pos

    def _wrap(self, screen_rect: pygame.Rect) -> None:
        if self.pos.x < 0:
            self.pos.x = screen_rect.width
        elif self.pos.x > screen_rect.width:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = screen_rect.height
        elif self.pos.y > screen_rect.height:
            self.pos.y = 0

    def _update_trail(self, dt: float) -> None:
        self.trail.append((self.pos.copy(), self.trail_max_life))
        self.trail = [(p, t - dt) for p, t in self.trail if t - dt > 0]

    def _draw_trail(self, surface: pygame.Surface) -> None:
        for pos, life in self.trail:
            alpha = int(255 * (life / self.trail_max_life))
            radius = 3 + 6 * (life / self.trail_max_life)
            size = int(radius * 4)
            bubble = pygame.Surface((size, size), pygame.SRCALPHA)
            center = size // 2
            outer_color = (180, 200, 255, alpha // 2)
            inner_color = (255, 255, 255, alpha)
            pygame.draw.circle(bubble, outer_color, (center, center), center)
            pygame.draw.circle(bubble, inner_color, (center, center), int(radius))
            surface.blit(
                bubble, (pos.x - center, pos.y - center), special_flags=pygame.BLEND_ADD
            )

    def _apply_rotation(self) -> None:
        # Rotozoom gira antihorario; pasamos –angle para que el sprite apunte a “angle”
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1.0)
        self.rect = self.image.get_rect(center=self.rect.center)

    # ─ Utilidades ──────────────────────────────────────────────────────
    @staticmethod
    def _create_default_image() -> pygame.Surface:
        surf = pygame.Surface((20, 30), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (200, 220, 255), [(10, 0), (0, 30), (20, 30)])
        return surf
