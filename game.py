import pygame

class AchievementPopup:
    def __init__(self, name, name2, width, height):
        self.name = name
        self.name2 = name2
        self.width = width
        self.height = height

        self.x = (1225 - width) // 2
        self.y = -height
        self.target_y = 20
        self.speed = 6

        self.timer = 0
        self.state = "enter"

    def draw_it(self, screen, font, small_font, smaller_font):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=0)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=0)

        title_surf = font.render("Achievement Unlocked!", True, (218, 165, 32))
        name_surf = small_font.render(self.name, True, (0, 0, 0))
        desc_surf = smaller_font.render(self.name2, True, (0,0,0))
        screen.blit(
            title_surf,
            (self.x + (self.width - title_surf.get_width()) // 2,
             self.y + 8)
        )

        screen.blit(
            name_surf,
            (self.x + (self.width - name_surf.get_width()) // 2,
             self.y + 8 + title_surf.get_height())
        )

        screen.blit(
            desc_surf,
            (self.x + (self.width - desc_surf.get_width()) // 2,
             self.y + 8 + title_surf.get_height() + name_surf.get_height())
        )
    def update(self):
        if self.state == "enter":
            self.y += self.speed
            if self.y >= self.target_y:
                self.y = self.target_y
                self.state = "stay"

        elif self.state == "stay":
            self.timer += 1
            if self.timer > 180:  # ~3 seconds at 60 FPS
                self.state = "exit"

        elif self.state == "exit":
            self.y -= self.speed
            if self.y < -self.height:
                return False  # popup finished

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

    def draw(self, screen, font=None):
        if self.image:
            img = self.pressed_image if self.pressed and self.pressed_image else self.image
            screen.blit(img, self.rect)
        elif self.color is not None:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

        # Draw the border if border_color is set
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width,
                             border_radius=self.border_radius)

        if not self.text or not font:
            return

        color = self.pressed_text_color if self.pressed else self.text_color

        if isinstance(self.text, list) and isinstance(font, tuple):
            font_top, font_bottom = font
            surf_top = font_top.render(self.text[0], False, color)
            surf_bottom = font_bottom.render(self.text[1], False, color)
            spacing = 4
            total_height = surf_top.get_height() + spacing + surf_bottom.get_height()
            start_y = self.rect.centery - total_height // 2
            rect_top = surf_top.get_rect(centerx=self.rect.centerx, y=start_y)
            rect_bottom = surf_bottom.get_rect(
                centerx=self.rect.centerx,
                y=start_y + surf_top.get_height() + spacing
            )
            screen.blit(surf_top, rect_top)
            screen.blit(surf_bottom, rect_bottom)
        elif isinstance(self.text, list):
            line_height = font.get_height()
            total_height = line_height * len(self.text)
            start_y = self.rect.centery - total_height // 2
            for i, line in enumerate(self.text):
                surf = font.render(line, False, color)
                rect = surf.get_rect(
                    centerx=self.rect.centerx,
                    y=start_y + i * line_height
                )
                screen.blit(surf, rect)
        else:
            surf = font.render(self.text, False, color)
            screen.blit(surf, surf.get_rect(center=self.rect.center))