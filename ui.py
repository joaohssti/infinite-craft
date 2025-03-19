import pygame
import json

# Configurações iniciais
WIDTH, HEIGHT = 1600, 800
BG_COLOR = (30, 30, 30)
NODE_COLOR = (200, 50, 50)
SELECTED_NODE_COLOR = (50, 200, 50)
TEXT_COLOR = (255, 255, 255)
ARROW_COLOR = (255, 255, 255)
SELECTED_ARROW_COLOR = (50, 200, 50)
FONT_SIZE = 20
NODE_SPACING_X = 150
NODE_SPACING_Y = 100

class GraphVisualizer:
    def __init__(self, nodes):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.scroll_x, self.scroll_y = 0, 0
        self.nodes = nodes
        self.node_positions = {}
        self.selected_nodes = set()
        self.levels = self.organize_levels()

    def organize_levels(self):
        levels = {}
        for node in self.nodes:
            level = node["nivel"]
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        return levels

    def draw_arrow(self, start, end, color):
        pygame.draw.line(self.screen, color, start, end, 2)
        pygame.draw.polygon(self.screen, color, [(end[0], end[1]), (end[0]-5, end[1]-10), (end[0]+5, end[1]-10)])

    def get_parents(self, item):
        parents = set()
        for node in self.nodes:
            if node["item"] == item:
                if node["comb1"]:
                    parents.add(node["comb1"])
                    parents.update(self.get_parents(node["comb1"]))
                if node["comb2"]:
                    parents.add(node["comb2"])
                    parents.update(self.get_parents(node["comb2"]))
        return parents

    def select_item(self, item):
        self.selected_nodes.clear()
        self.selected_nodes.add(item)
        self.selected_nodes.update(self.get_parents(item))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.scroll_x += 20
                elif event.key == pygame.K_RIGHT:
                    self.scroll_x -= 20
                elif event.key == pygame.K_UP:
                    self.scroll_y += 20
                elif event.key == pygame.K_DOWN:
                    self.scroll_y -= 20
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for node, (x, y) in self.node_positions.items():
                    if (x - 40 <= mx <= x + 40) and (y - 40 <= my <= y + 40):
                        self.select_item(node)
        return True

    def update_positions(self):
        for level, nodes_at_level in self.levels.items():
            for i, node in enumerate(nodes_at_level):
                x = (i + 1) * NODE_SPACING_X + self.scroll_x
                y = level * NODE_SPACING_Y + 50 + self.scroll_y
                self.node_positions[node["item"]] = (x, y)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.update_positions()
        
        for node in self.nodes:
            if node["comb1"] and node["comb2"] and node["comb1"] in self.node_positions and node["comb2"] in self.node_positions:
                start_pos = self.node_positions[node["item"]]
                end_pos1 = self.node_positions[node["comb1"]]
                end_pos2 = self.node_positions[node["comb2"]]
                color = SELECTED_ARROW_COLOR if node["item"] in self.selected_nodes else ARROW_COLOR
                self.draw_arrow(start_pos, end_pos1, color)
                self.draw_arrow(start_pos, end_pos2, color)
        
        for node in self.nodes:
            x, y = self.node_positions[node["item"]]
            color = SELECTED_NODE_COLOR if node["item"] in self.selected_nodes else NODE_COLOR
            pygame.draw.circle(self.screen, color, (x, y), 40)
            text = self.font.render(node["item"], True, TEXT_COLOR)
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))        
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    with open("nodes.json", "r", encoding="utf-8") as file:
        nodes = json.load(file)
    
    app = GraphVisualizer(nodes)
    app.run()
