import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
ui_height = 100
screen = pygame.display.set_mode((width, height + ui_height))
pygame.display.set_caption("Dynamic Boid Simulation")

# Colors
BACKGROUND_COLOR = (0, 0, 20)
TRAIL_COLOR = (0, 0, 30)
UI_BACKGROUND_COLOR = (30, 30, 30)
SLIDER_COLOR = (200, 200, 200)
HANDLE_COLOR = (100, 100, 100)
TEXT_COLOR = (0, 0, 0)
BOID_COLORS = [
    (255, 102, 102),  # Light Red
    (255, 178, 102),  # Light Orange
    (255, 255, 102),  # Light Yellow
    (178, 255, 102),  # Light Green
    (102, 255, 178),  # Turquoise
    (102, 178, 255),  # Light Blue
    (178, 102, 255),  # Light Purple
    (255, 102, 255),  # Light Pink
]

# Grid size for spatial partitioning
grid_size = 120

# UI Slider class
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.handle_rect = pygame.Rect(x, y, w * ((initial_val - min_val) / (max_val - min_val)), h)
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_rect.x = min(max(event.pos[0], self.rect.x), self.rect.x + self.rect.width - self.handle_rect.width)
                self.value = self.min_val + (self.handle_rect.x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

    def draw(self, screen):
        pygame.draw.rect(screen, SLIDER_COLOR, self.rect, border_radius=10)
        pygame.draw.rect(screen, HANDLE_COLOR, self.handle_rect, border_radius=10)
        font = pygame.font.SysFont(None, 24)
        label_surface = font.render(f"{self.label}: {self.value:.2f}", True, TEXT_COLOR)
        screen.blit(label_surface, (self.rect.x + 5, self.rect.y + (self.rect.height // 2 - label_surface.get_height() // 2)))

# Boid class
class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, width), random.randint(0, height))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(random.uniform(2, 4))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_force = 0.05
        self.max_speed = 4
        self.size = 8  # Increased size
        self.vision_radius = 100
        self.color = random.choice(BOID_COLORS)  # Randomly assign a color from the list
        self.memory = []  # List to store past positions
        self.memory_size = 50  # Limit the memory size

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

        # Store the current position in memory
        self.memory.append(pygame.Vector2(self.position))
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

    def apply_behaviour(self, boids, food_positions, alignment_weight, cohesion_weight, separation_weight, attraction_weight, boundary_avoidance_weight, current_weight, memory_weight):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        attraction = self.attract_to_food(food_positions)
        boundary_avoidance = self.avoid_boundaries()
        current = self.apply_current()
        memory = self.move_away_from_memory()

        self.acceleration += alignment * alignment_weight
        self.acceleration += cohesion * cohesion_weight
        self.acceleration += separation * separation_weight
        self.acceleration += attraction * attraction_weight
        self.acceleration += boundary_avoidance * boundary_avoidance_weight
        self.acceleration += current * current_weight
        self.acceleration += memory * memory_weight

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_vec = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < 50:
                avg_vec += boid.velocity
                total += 1
        if total > 0:
            avg_vec /= total
            avg_vec.scale_to_length(self.max_speed)
            steering = avg_vec - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohesion(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        center_of_mass = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < 50:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            vec_to_com = center_of_mass - self.position
            if vec_to_com.length() > 0:
                vec_to_com.scale_to_length(self.max_speed)
            steering = vec_to_com - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separation(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_vector = pygame.Vector2(0, 0)
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if self != boid and distance < 25:
                diff = self.position - boid.position
                if distance > 0:
                    diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            if avg_vector.length() > 0:
                avg_vector.scale_to_length(self.max_speed)
            steering = avg_vector - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def attract_to_food(self, food_positions):
        closest_food = None
        min_distance = float('inf')
        for food in food_positions:
            distance = self.position.distance_to(food)
            if distance < min_distance:
                min_distance = distance
                closest_food = food

        if closest_food:
            attraction = pygame.Vector2(closest_food) - self.position
            if attraction.length() > 0:
                attraction.scale_to_length(self.max_speed)
            steering = attraction - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
            return steering
        return pygame.Vector2(0, 0)

    def avoid_boundaries(self):
        steering = pygame.Vector2(0, 0)
        if self.position.x < self.vision_radius:
            steering += pygame.Vector2(self.max_speed, 0)
        elif self.position.x > width - self.vision_radius:
            steering += pygame.Vector2(-self.max_speed, 0)
        if self.position.y < self.vision_radius:
            steering += pygame.Vector2(0, self.max_speed)
        elif self.position.y > height - self.vision_radius:
            steering += pygame.Vector2(0, -self.max_speed)

        if steering.length() > 0:
            steering.scale_to_length(self.max_speed)
            steering = steering - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def apply_current(self):
        current_strength = 0.03
        current = pygame.Vector2(math.sin(self.position.y / 50.0), math.cos(self.position.x / 50.0))
        current.scale_to_length(current_strength)
        return current

    def move_away_from_memory(self):
        steering = pygame.Vector2(0, 0)
        for memory_pos in self.memory:
            distance = self.position.distance_to(memory_pos)
            if distance < 50:
                diff = self.position - memory_pos
                if distance > 0:
                    diff /= distance
                steering += diff
        if steering.length() > 0:
            steering.scale_to_length(self.max_speed)
            steering = steering - self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def edges(self):
        if self.position.x > width:
            self.position.x = width
            self.velocity.x *= -1
        elif self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -1
        if self.position.y > height:
            self.position.y = height
            self.velocity.y *= -1
        elif self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -1

    def draw(self, screen):
        angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        points = [
            self.position + self.velocity.normalize() * self.size,
            self.position + pygame.Vector2(-self.size / 2, self.size / 2).rotate(angle),
            self.position + pygame.Vector2(-self.size / 2, -self.size / 2).rotate(angle)
        ]
        pygame.draw.polygon(screen, self.color, points)

# Create boids
num_boids = 350
boids = [Boid() for _ in range(num_boids)]

# List to store food positions
food_positions = []

# Spatial partitioning grid
def create_grid():
    return [[[] for _ in range((height // grid_size) + 1)] for _ in range((width // grid_size) + 1)]

def get_grid_position(boid):
    return int(boid.position.x // grid_size), int(boid.position.y // grid_size)

def add_boid_to_grid(grid, boid):
    x, y = get_grid_position(boid)
    grid[x][y].append(boid)

def get_nearby_boids(grid, boid):
    x, y = get_grid_position(boid)
    nearby_boids = []
    for i in range(max(0, x-1), min(len(grid), x+2)):
        for j in range(max(0, y-1), min(len(grid[0]), y+2)):
            nearby_boids.extend(grid[i][j])
    return nearby_boids

# Sliders
sliders = [
    Slider(10, height + 10, 200, 20, 0.0, 5.0, 1.0, "Alignment"),
    Slider(220, height + 10, 200, 20, 0.0, 5.0, 1.0, "Cohesion"),
    Slider(430, height + 10, 200, 20, 0.0, 5.0, 1.5, "Separation"),
    Slider(640, height + 10, 200, 20, 0.0, 5.0, 1.5, "Attraction"),
    Slider(850, height + 10, 200, 20, 0.0, 5.0, 3.0, "Boundary Avoidance"),
    Slider(1060, height + 10, 200, 20, 0.0, 5.0, 0.3, "Current"),
    Slider(10, height + 50, 200, 20, 0.0, 5.0, 0.5, "Memory")
]

# Main game loop
running = True
clock = pygame.time.Clock()

# Background surface for trail effect
background = pygame.Surface((width, height))
background.set_alpha(30)
background.fill(TRAIL_COLOR)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < height:
                food_positions.append(pygame.Vector2(event.pos))

        for slider in sliders:
            slider.handle_event(event)

    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))

    grid = create_grid()
    for boid in boids:
        add_boid_to_grid(grid, boid)

    for boid in boids:
        nearby_boids = get_nearby_boids(grid, boid)
        boid.apply_behaviour(nearby_boids, food_positions, sliders[0].value, sliders[1].value, sliders[2].value, sliders[3].value, sliders[4].value, sliders[5].value, sliders[6].value)
        boid.update()
        boid.edges()
        boid.draw(screen)

    # Draw food
    for food in food_positions:
        pygame.draw.circle(screen, (255, 255, 255), (int(food.x), int(food.y)), 3)

    # Remove food once a boid reaches it
    for boid in boids:
        for food in food_positions:
            if boid.position.distance_to(food) < 5:
                food_positions.remove(food)

    # Draw UI
    pygame.draw.rect(screen, UI_BACKGROUND_COLOR, (0, height, width, ui_height))
    for slider in sliders:
        slider.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
