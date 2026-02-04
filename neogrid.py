#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 Elijah Gordon (NitrixXero) <nitrixxero@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame
import random
import os

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.FULLSCREEN | pygame.NOFRAME
)

black = (0, 0, 0)
current_color = (0, 255, 0)
matrix_font_size = 36
font_path = os.path.join("font", "MS Mincho.ttf")


def initialize_characters():
    return [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'ァ', 'ア', 'ィ', 'イ', 'ゥ', 'ウ', 'ェ', 'エ', 'ォ',
        'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ', 'ゲ',
        'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ', 'ス', 'ズ', 'セ',
        'ゼ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ヂ', 'ッ', 'ツ',
        'ヅ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ',
        'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ',
        'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ',
        'ム', 'メ', 'モ', 'ャ', 'ヤ', 'ュ', 'ユ', 'ョ', 'ヨ',
        'ラ', 'リ', 'ル', 'レ', 'ロ', 'ヮ', 'ワ', 'ヰ', 'ヱ',
        'ヲ', 'ン', 'ヴ', 'ヵ', 'ヶ', 'ヷ', 'ヸ', 'ヹ', 'ヺ',
        '・', 'ー', 'ヽ', 'ヾ'
    ]


class Matorikkusu:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.chars = initialize_characters()
        self.char_size = matrix_font_size
        self.line_length = random.randint(14, 26)
        self.line = [random.choice(self.chars) for _ in range(self.line_length)]
        self.vertical_step = 10
        self.alpha = 255
        self.trail_length = 4
        self.trail = []

    def draw(self, screen):
        if self.y < screen_height:
            self.y += self.vertical_step * (self.line_length / 20)
            distance_to_bottom = screen_height - self.y
            fade_range = 200
            if distance_to_bottom < fade_range:
                self.alpha = int((distance_to_bottom / fade_range) * 255)
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)
            for i in range(self.line_length):
                if random.random() < 0.08:
                    self.line[i] = random.choice(self.chars)
        else:
            self.y = -40 * random.randrange(1, 5)
            self.alpha = 255
            self.trail = []

        char_font = pygame.font.Font(font_path, self.char_size)

        for i, char in enumerate(self.line):
            flicker_alpha = random.randint(180, 255)
            fade_distance = screen_height - self.y - i * 30
            fade_distance = max(0, fade_distance)
            fade_alpha = int((1 - fade_distance / screen_height) * self.alpha)
            final_alpha = min(fade_alpha, flicker_alpha)

            char_surface = char_font.render(char, True, self.color)
            char_surface.set_alpha(final_alpha)
            screen.blit(char_surface, (self.x, self.y + i * 36))

            for j, trail_pos in enumerate(reversed(self.trail)):
                trail_alpha = int((1 - j / self.trail_length) * final_alpha)
                trail_surface = char_font.render(char, True, self.color)
                trail_surface.set_alpha(trail_alpha)
                screen.blit(trail_surface, (trail_pos[0], trail_pos[1] + i * 36))

    def set_color(self, color):
        self.color = color

    def decrease_speed(self):
        self.vertical_step = max(self.vertical_step - 5, 5)

    def increase_speed(self):
        self.vertical_step = min(self.vertical_step + 5, 100)


def change_color(key):
    colors = {
        pygame.K_b: (0, 0, 255),
        pygame.K_c: (0, 255, 255),
        pygame.K_d: (110, 75, 38),
        pygame.K_e: (255, 121, 77),
        pygame.K_f: (246, 74, 138),
        pygame.K_g: (0, 255, 0),
        pygame.K_h: (223, 115, 255),
        pygame.K_r: (255, 0, 0),
        pygame.K_w: (255, 255, 255),
        pygame.K_y: (255, 255, 0),
        pygame.K_m: (255, 0, 255),
        pygame.K_o: (128, 128, 0),
        pygame.K_t: (0, 128, 128),
    }
    return colors.get(key)


def main():
    window = screen
    screen_width = window.get_width()

    try:
        pygame.mixer.init()
        audio = pygame.mixer.Sound('audio/audio.wav')
        audio.play(-1)
    except Exception:
        pass

    matrix_symbols = [
        Matorikkusu(x, random.randint(0, screen_height), current_color)
        for x in range(0, screen_width, matrix_font_size)
    ]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    for s in matrix_symbols:
                        s.decrease_speed()
                elif event.key == pygame.K_RIGHT:
                    for s in matrix_symbols:
                        s.increase_speed()
                else:
                    color = change_color(event.key)
                    if color:
                        global current_color
                        current_color = color
                        for s in matrix_symbols:
                            s.set_color(current_color)

        window.fill(black)
        for symbol in matrix_symbols:
            symbol.draw(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
