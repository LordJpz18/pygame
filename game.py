import pygame
import random

# --- Paramètres du jeu ---
WIDTH, HEIGHT = 800, 600
GAME_DURATION = 30  # durée d'une partie en secondes

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Attrape les objets - Timer & High Score")
clock = pygame.time.Clock()

# Couleurs
BACKGROUND = (20, 20, 30)
PLAYER_COLOR = (0, 180, 255)
OBJECT_COLOR = (255, 120, 120)
TEXT_COLOR = (255, 255, 255)
TEXT_DIM = (160, 160, 160)

# Joueur
player = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 40, 80, 20)
player_speed = 7

# Objets
objects = []

# Score
score = 0
high_score = 0

# Police
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# Timer
start_time = pygame.time.get_ticks()  # en millisecondes
playing = True  # True = partie en cours, False = fin (on attend un restart)


def reset_game():
    """Réinitialise une partie (sauf le high_score)."""
    global score, objects, player, start_time, playing

    score = 0
    objects.clear()
    player.x = WIDTH // 2 - player.width // 2
    player.y = HEIGHT - 40
    start_time = pygame.time.get_ticks()
    playing = True


running = True
while running:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Gestion des entrées selon l'état du jeu ---
    if playing:
        # Déplacement du joueur
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        # Empêcher de sortir de l'écran
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH

        # Création d'objets aléatoires
        if random.random() < 0.03:
            size = random.randint(15, 30)
            x = random.randint(0, WIDTH - size)
            rect = pygame.Rect(x, -size, size, size)
            speed = random.randint(2, 6)
            objects.append({"rect": rect, "speed": speed})

        # Mise à jour des objets (chute + collisions)
        for obj in objects[:]:
            obj["rect"].y += obj["speed"]

            if obj["rect"].colliderect(player):
                objects.remove(obj)
                score += 1
            elif obj["rect"].top > HEIGHT:
                objects.remove(obj)

        # Gestion du temps restant
        current_time_ms = pygame.time_get_ticks() if hasattr(pygame, "time_get_ticks") else pygame.time.get_ticks()
        elapsed_ms = current_time_ms - start_time
        elapsed_sec = elapsed_ms // 1000
        remaining_time = max(0, GAME_DURATION - elapsed_sec)

        if remaining_time <= 0:
            # Fin de la partie
            playing = False
            # Mettre à jour le meilleur score
            if score > high_score:
                high_score = score
    else:
        # Partie terminée : on attend que le joueur appuie sur ESPACE pour relancer
        if keys[pygame.K_SPACE]:
            reset_game()

        # On garde le temps restant à 0 pour l'affichage
        remaining_time = 0

    # Si on est en train de jouer, il faut calculer remaining_time
    if playing:
        current_time_ms = pygame.time.get_ticks()
        elapsed_ms = current_time_ms - start_time
        elapsed_sec = elapsed_ms // 1000
        remaining_time = max(0, GAME_DURATION - elapsed_sec)
    else:
        remaining_time = 0

    # --- Dessin ---
    screen.fill(BACKGROUND)

    # Joueur
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # Objets
    for obj in objects:
        pygame.draw.rect(screen, OBJECT_COLOR, obj["rect"])

    # Texte : score, meilleur score, timer
    score_text = font.render(f"Score : {score}", True, TEXT_COLOR)
    high_score_text = font.render(f"Meilleur : {high_score}", True, TEXT_COLOR)
    timer_text = font.render(f"Temps : {remaining_time:2d}s", True, TEXT_COLOR if remaining_time > 5 else (255, 80, 80))

    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

    # Message de fin quand la partie est terminée
    if not playing:
        msg = "Temps écoulé !"
        msg2 = "Appuie sur ESPACE pour rejouer"
        msg_surf = big_font.render(msg, True, TEXT_COLOR)
        msg2_surf = font.render(msg2, True, TEXT_DIM)

        screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(msg2_surf, (WIDTH // 2 - msg2_surf.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

