"""
Asset Integration Example
Demonstrates how to use the asset loader in the game.

This example shows how to integrate art assets into existing scenes.
"""

import pygame
from src.asset_loader import asset_loader
from src.data_loader import data_loader


class AssetIntegrationExample:
    """Example of integrating assets into the game."""
    
    def __init__(self, screen):
        self.screen = screen
        
        # Load UI assets
        self.load_ui_assets()
        
        # Load item images
        self.load_item_assets()
        
        # Load fonts
        self.load_fonts()
        
        # Load sounds
        self.load_sounds()
    
    def load_ui_assets(self):
        """Load UI-related assets."""
        print("Loading UI assets...")
        
        # These will return None if files don't exist yet
        self.button_image = asset_loader.load_image('ui/button.png')
        self.button_hover_image = asset_loader.load_image('ui/button_hover.png')
        self.panel_image = asset_loader.load_image('ui/panel.png')
        
        if self.button_image:
            print("✓ Button image loaded")
        else:
            print("✗ Button image not found (place in assets/images/ui/button.png)")
    
    def load_item_assets(self):
        """Load food item images."""
        print("\nLoading item assets...")
        
        # Get item names from configuration
        items = data_loader.get('items', 'ingredients')
        
        self.item_images = {}
        for item_name in items.keys():
            # Convert "Instant Noodles" to "instant_noodles.png"
            filename = item_name.lower().replace(' ', '_') + '.png'
            image_path = f'items/{filename}'
            
            image = asset_loader.load_image(image_path)
            if image:
                self.item_images[item_name] = image
                print(f"✓ Loaded {item_name} image")
            else:
                print(f"✗ {item_name} image not found (place in assets/images/{image_path})")
    
    def load_fonts(self):
        """Load custom fonts."""
        print("\nLoading fonts...")
        
        # Load custom fonts (will fall back to default if not found)
        self.title_font = asset_loader.load_font('title_font.ttf', 48)
        self.normal_font = asset_loader.load_font('game_font.ttf', 24)
        self.small_font = asset_loader.load_font('game_font.ttf', 18)
        
        print("✓ Fonts loaded (using default if custom fonts not found)")
    
    def load_sounds(self):
        """Load sound effects."""
        print("\nLoading sounds...")
        
        self.click_sound = asset_loader.load_sound('sfx/click.wav')
        self.purchase_sound = asset_loader.load_sound('sfx/purchase.wav')
        self.cooking_sound = asset_loader.load_sound('sfx/cooking.wav')
        
        if self.click_sound:
            print("✓ Click sound loaded")
        else:
            print("✗ Click sound not found (place in assets/sounds/sfx/click.wav)")
    
    def draw_example(self):
        """Draw example UI with loaded assets."""
        self.screen.fill((50, 50, 50))
        
        # Draw title
        title_text = self.title_font.render("Asset Integration Example", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.screen.get_width() // 2, y=50)
        self.screen.blit(title_text, title_rect)
        
        # Draw panel if loaded
        if self.panel_image:
            self.screen.blit(self.panel_image, (100, 150))
        else:
            # Draw placeholder
            pygame.draw.rect(self.screen, (100, 100, 100), (100, 150, 400, 300))
            text = self.normal_font.render("Panel Image Placeholder", True, (200, 200, 200))
            self.screen.blit(text, (150, 280))
        
        # Draw item images
        x = 100
        y = 500
        for item_name, image in self.item_images.items():
            # Draw item image (scaled down if needed)
            scaled_image = pygame.transform.scale(image, (64, 64))
            self.screen.blit(scaled_image, (x, y))
            
            # Draw item name
            name_text = self.small_font.render(item_name[:10], True, (255, 255, 255))
            self.screen.blit(name_text, (x, y + 70))
            
            x += 80
            if x > 800:
                x = 100
                y += 100
        
        # Draw instructions
        instructions = [
            "Press SPACE to play click sound",
            "Press P to play purchase sound",
            "Press ESC to exit"
        ]
        
        y = self.screen.get_height() - 100
        for instruction in instructions:
            text = self.small_font.render(instruction, True, (150, 150, 150))
            self.screen.blit(text, (20, y))
            y += 25
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.click_sound:
                self.click_sound.play()
                print("Playing click sound")
            elif event.key == pygame.K_p and self.purchase_sound:
                self.purchase_sound.play()
                print("Playing purchase sound")
            elif event.key == pygame.K_ESCAPE:
                return False
        return True


def main():
    """Run the asset integration example."""
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Asset Integration Example")
    
    # Create example instance
    example = AssetIntegrationExample(screen)
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not example.handle_event(event):
                running = False
        
        example.draw_example()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == '__main__':
    print("="*60)
    print("Asset Integration Example")
    print("="*60)
    print("\nThis example demonstrates how to use the asset loader.")
    print("Most assets will show placeholders until you add actual files.\n")
    print("To add assets:")
    print("1. Place image files in assets/images/")
    print("2. Place sound files in assets/sounds/")
    print("3. Place font files in assets/fonts/")
    print("="*60)
    print()
    
    main()
