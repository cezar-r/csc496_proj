from manim import *

class Intro(Scene):
    def construct(self):
        t1 = Text("Election Math Episode 1", font_size=36)
        t2 = Text("Intro to RCV Algorithms", font_size=48).next_to(t1, DOWN).shift(DOWN * 0.5)
        
        t_group = VGroup(t1, t2).center()
        
        self.play(Write(t_group))
        self.wait(2)
        self.play(FadeOut(t_group))
        