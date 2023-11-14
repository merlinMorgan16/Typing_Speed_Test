import pygame
from pygame.locals import *
import sys
import time
import random


class Game:
    timeStart: int

    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.inputText = ''
        self.word = ''
        self.timeStart = 0
        self.totalTime = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (11, 3, 160)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (2, 56, 46)

        pygame.init()
        self.open_img = pygame.image.load('TypingSpeedTestCover.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('GlossyBackground.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.w, self.h))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed test')

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if not self.end:
            # Calculate time only if the player started typing
            if self.active:
                self.totalTime = time.time() - self.timeStart

            # Calculate accuracy and words per minute
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.inputText[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            # Calculate words per minute only if the player started typing
            if self.active:
                self.wpm = len(self.inputText) * 60 / (5 * self.totalTime)

            self.end = True
            print(self.totalTime)

            self.results = (
                'Time: '
                + str(round(self.totalTime))
                + " secs   Accuracy: "
                + str(round(self.accuracy))
                + "%"
                + '   Wpm: '
                + str(round(self.wpm))
            )

            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (2, 3, 56))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.inputText, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.inputText = ''
                        self.timeStart = time.time()
                    # position of reset box
                    if 310 <= x <= 510 and y >= 390 and self.end:
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.inputText)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.inputText = self.inputText[:-1]
                        else:
                            try:
                                self.inputText += event.unicode
                            except:
                                pass

            pygame.display.update()

        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        time.sleep(1)

        self.reset = False
        self.end = False

        self.inputText = ''
        self.word = ''
        self.timeStart = 0
        self.totalTime = 0
        self.wpm = 0

        # Get random sentence
        self.word = self.get_sentence()
        if not self.word:
            self.reset_game()
        # drawing heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()


Game().run()

