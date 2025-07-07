import sys
from pathlib import Path

# Asegúrate de poder importar el paquete `domain`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from domain.space import Space  # noqa: E402  (import después de añadir a sys.path)


def main() -> None:
    game = Space()  # Usa valores por defecto (800×600, 60 FPS)
    game.run()


if __name__ == "__main__":
    main()
