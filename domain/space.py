import pygame
from domain.ship import Ship


class Space:
    """
    Ventana básica completamente negra.
    Usa `run()` para lanzar el bucle principal.
    """

    def __init__(self, width: int = 800, height: int = 600, fps: int = 60) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Space")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.ship = Ship((width // 2, height // 2))

    # --- Lógica interna -------------------------------------------------
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self) -> None:
        dt = self.clock.get_time() / 1000  # segundos
        self.ship.update(dt, self.screen.get_rect())

    def _draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.ship.draw(self.screen)

    # --- API pública ----------------------------------------------------
    def run(self) -> None:
        """Inicia el loop principal (bloqueante)."""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
