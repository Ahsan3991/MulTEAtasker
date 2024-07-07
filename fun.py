import pygame
import random
import time 

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 2000
PLAYER_SIZE = 120
ITEM_SIZE = 80
FPS = 60
POWER_DECREASE_INTERVAL = 2 * 1000  # 1 second(s) in milliseconds

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MulTEAtasker")


# Load images
player_image = pygame.image.load('images/player.png')
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
page_image = pygame.image.load('images/page.png')
page_image = pygame.transform.scale(page_image, (ITEM_SIZE, ITEM_SIZE))
chai_image = pygame.image.load('images/chai.png')
chai_image = pygame.transform.scale(chai_image, (ITEM_SIZE, ITEM_SIZE))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.tasks = 0
        self.power = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= random.randint(3, 20)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
             self.rect.x += random.randint(3, 20)
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += random.randint(3, 20)
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= random.randint(3, 20)

# Item class
class Item(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ITEM_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ITEM_SIZE)

    def update(self):
        self.rect.y += 5
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - ITEM_SIZE)

# Function to display the title screen
def show_title_screen(screen):
    font = pygame.font.SysFont(None, 100)
    title_text = font.render("MulTEAtasker", True, (0, 250, 0))
    start_text = pygame.font.SysFont(None, 50).render("Press any key to start", True, (0, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # Wait for key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Initialize player and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
pages = pygame.sprite.Group()
chais = pygame.sprite.Group()


# Create items
for _ in range(1):
    page = Item(page_image)
    pages.add(page)
    all_sprites.add(page)


# Show the title screen
show_title_screen(screen)

# Initialize salary, hit counter and power timer
salary = 500
page_hits_counter = 0
last_power_decrease_time = pygame.time.get_ticks()

# Game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Randomly generate new items
        if random.randint(1, 800) == 1:  # Random chance for new page
            page = Item(page_image)
            pages.add(page)
            all_sprites.add(page)
        
        if random.randint(1, 1100) == 1:  # Random chance for new tea (2.5 times less frequent than pages)
            chai = Item(chai_image)
            chais.add(chai)
            all_sprites.add(chai)

        # Update
        all_sprites.update()

        # Check for collisions
        page_hits = pygame.sprite.spritecollide(player, pages, True)
        chai_hits = pygame.sprite.spritecollide(player, chais, True)

        for hit in page_hits:
            print("document collected, task done")
            player.tasks += 1
            page_hits_counter += 1
            if page_hits_counter % 30 == 0:
                salary += 250
            page = Item(page_image)
            pages.add(page)
            all_sprites.add(page)

        for hit in chai_hits:
            print("Drank chai! Power up")
            player.power += 10
            chai = Item(chai_image)
            chais.add(chai)
            all_sprites.add(chai)
            
            
        # Decrease player power every minute
        current_time = pygame.time.get_ticks()
        if current_time - last_power_decrease_time >= POWER_DECREASE_INTERVAL:
            player.power = max(0, player.power - 10)  # Ensure power does not go below 0
            last_power_decrease_time = current_time
            
        # Check if player's power is zero
        if player.power == 0:
            game_over = True
            
        # Draw / render
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Show player's power level
        font = pygame.font.SysFont(None, 54)
        tasks_done_text = font.render(f"tasks: {player.tasks}", True, (255, 255, 255))
        power_text = font.render(f"Power: {player.power}", True, (255, 255, 255))
        salary_text = font.render(f"Salary: ${salary}", True, (255, 255, 255))
        screen.blit(power_text, (10, 10))
        screen.blit(tasks_done_text, (300, 10))
        screen.blit(salary_text, (1640, 10))

    else:
        # Display "GAME OVER" message
        font = pygame.font.SysFont(None, 84)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 500))

        font = pygame.font.SysFont(None, 65)
        game_over2_text = font.render("Your employee is promoted to next life!", True, (255, 255, 255))
        screen.blit(game_over2_text, (SCREEN_WIDTH // 2 - game_over2_text.get_width() // 2, SCREEN_HEIGHT // 20))

        # Display additional messages
        font_small = pygame.font.SysFont(None, 65)
        final_score_text = font_small.render(f"Final Salary: ${salary}", True, (255, 255, 255))
        final_score_text2 = font_small.render(f"Tasks Completed: {player.tasks}", True, (255, 255, 255))
        restart_text = font_small.render("Press ENTER to restart", True, (255, 255, 255))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 5 + 50))
        screen.blit(final_score_text2, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 5 + 100))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 10))

        pygame.display.flip()

        # Wait for Enter key press to restart
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
                        waiting = False
                        # Reset the game
                        player.power = 100
                        salary = 500
                        page_hits_counter = 0
                        last_power_decrease_time = pygame.time.get_ticks()
                        game_over = False
                        # Clear existing items and create new ones
                        pages.empty()
                        teas.empty()
                        all_sprites.empty()
                        all_sprites.add(player)
                        for _ in range(10):
                            page = Item(page_image)
                            pages.add(page)
                            all_sprites.add(page)
    # Flip the display
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

pygame.quit()

