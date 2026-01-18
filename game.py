import pygame

class AchievementPopup:
    def __init__(self, name, name2, width, height, font, small_font, smaller_font):
        self.name = name
        self.name2 = name2
        self.width = width
        self.height = height

        self.x = (1225 - width) // 2
        self.y = -height
        self.target_y = 20
        self.speed = 6

        self.title_surf = font.render("Achievement Unlocked!", True, (218, 165, 32))
        self.name_surf = small_font.render(name, True, (0, 0, 0))
        self.desc_surf = smaller_font.render(name2, True, (0, 0, 0))

        self.start_time = pygame.time.get_ticks()

    def draw_it(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        screen.blit(
            self.title_surf,
            (self.x + (self.width - self.title_surf.get_width()) // 2, self.y + 8)
        )
        screen.blit(
            self.name_surf,
            (self.x + (self.width - self.name_surf.get_width()) // 2,
             self.y + 8 + self.title_surf.get_height())
        )
        screen.blit(
            self.desc_surf,
            (self.x + (self.width - self.desc_surf.get_width()) // 2,
             self.y + 8 + self.title_surf.get_height() + self.name_surf.get_height())
        )

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        if elapsed < 400:  # slide in
            self.y = -self.height + (elapsed / 400) * (self.target_y + self.height)
        elif elapsed < 2400:  # stay
            self.y = self.target_y
        elif elapsed < 3000:  # slide out
            t = (elapsed - 2400) / 600
            self.y = self.target_y - t * (self.height + 20)
        else:
            return False

        return True


class Achievement:
    def __init__(self, name, description, criterion, stat):
        self.name = name
        self.description = description
        self.criterion = criterion
        self.met = False
        self.stat = stat
        self.triggered_time = None
    def check(self, value):
        if not self.met and value >= self.criterion:
            self.met = True
            return True
        return False

class Button:
    def __init__(
            self,
            rect,
            text="",
            color=(255, 255, 255),  # button background
            text_color=(0, 0, 0),  # normal text color
            pressed_text_color=(180, 180, 180),  # text when pressed
            image=None,
            pressed_image=None,
            action=None,
            border_radius=10,
            border_color=None,  # NEW: color of the border
            border_width=2  # NEW: thickness of the border
    ):
        self.rect = rect
        self.text = text
        self.color = color
        self.text_color = text_color
        self.pressed_text_color = pressed_text_color
        self.image = image
        self.pressed_image = pressed_image
        self.action = action
        self.pressed = False
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.action:
                    self.action()
                return True

            self.pressed = False

        return False

    def draw(self, screen, font):
        # 1. Draw Background (Image or Color)
        if self.image:
            img = self.pressed_image if self.pressed and self.pressed_image else self.image
            screen.blit(img, self.rect)
        elif self.color is not None:
            button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            fill_color = (*self.color, 255) if len(self.color) == 3 else self.color
            pygame.draw.rect(button_surface, fill_color, button_surface.get_rect(), border_radius=self.border_radius)
            screen.blit(button_surface, self.rect.topleft)

        # 2. Draw Border
        if self.border_color and self.border_width > 0:
            border_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (*self.border_color, 255), border_surface.get_rect(),
                             width=self.border_width, border_radius=self.border_radius)
            screen.blit(border_surface, self.rect.topleft)

        # 3. Draw Multi-line Text
        if not self.text or not font:
            return

        color = self.pressed_text_color if self.pressed else self.text_color

        # Convert text to a list of strings (handles \n)
        if isinstance(self.text, str):
            lines = self.text.split('\n')
        else:
            lines = self.text

        rendered_lines = []

        # Logic for multiple fonts (e.g., Header font and Subtitle font)
        if isinstance(font, (tuple, list)) and len(lines) >= 2:
            # Render first line with font[0], second with font[1]
            rendered_lines.append(font[0].render(str(lines[0]), True, color))
            rendered_lines.append(font[1].render(str(lines[1]), True, color))
            # If there are more lines but only 2 fonts, use the second font for the rest
            for extra_line in lines[2:]:
                rendered_lines.append(font[1].render(str(extra_line), True, color))
        else:
            # Standard case: Use the same font for every line
            # This handles if 'font' is just a single pygame.font.Font object
            current_font = font[0] if isinstance(font, (tuple, list)) else font
            rendered_lines = [current_font.render(str(line), True, color) for line in lines]

        # Calculate total height of all lines combined for vertical centering
        spacing = 4
        total_height = sum(surf.get_height() for surf in rendered_lines) + (spacing * (len(rendered_lines) - 1))

        # Start drawing from this Y coordinate to keep the block centered
        current_y = self.rect.centery - (total_height // 2)

        for surf in rendered_lines:
            line_rect = surf.get_rect(centerx=self.rect.centerx, top=current_y)
            screen.blit(surf, line_rect)
            current_y += surf.get_height() + spacing