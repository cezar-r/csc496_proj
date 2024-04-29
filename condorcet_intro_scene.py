from manim import *

class CondorcetIntroScene(Scene):
    def generate_pw_table(self, pw_scores):
        return [[" ", "A", "B", "C"],
                 ["A", "X", str(pw_scores["A"]["B"]), str(pw_scores["A"]["C"])],
                 ["B", str(pw_scores["B"]["A"]), "X", str(pw_scores["B"]["C"])],
                 ["C", str(pw_scores["C"]["A"]), str(pw_scores["C"]["B"]), "X"]]
        
    def construct(self):
        table_data = [
            ["Ballot", "Count"],
            ["BCA", "8"],
            ["ABC", "6"],
            ["CBA", "6"],
            ["ACB", "4"],
            ["BAC", "3"]
        ]

        table = Table(
            table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        cond_text = Text("Condorcet", font_size=48).scale(0.8).next_to(table, UP, buff=0.5)

        self.play(FadeIn(cond_text))

        self.wait(4)
        steps_text = VGroup(
            Text("1) Compute pairwise scores for every candidate", font_size=24),
            Text("2) Find the winner for each pairwise comparison", font_size=24),
            Text("3) If a candidate beats all other candidates, they are the winner", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cond_text, DOWN, buff=0.5).shift(RIGHT*4)

        for step in steps_text:
            self.play(FadeIn(step))
            self.wait(3)
        self.wait(6)

        self.play(FadeOut(cond_text), FadeOut(steps_text), FadeIn(table))

        pw_scores = {"A": {"B": 0, "C": 0},
                     "B": {"A": 0, "C": 0},
                     "C": {"A": 0, "B": 0}}
        pw_table_data = self.generate_pw_table(pw_scores)
        pw_table = Table(
            pw_table_data,
            include_outer_lines=True
        ).scale(0.6).to_edge(LEFT).next_to(table).shift(RIGHT*5)

        self.play(FadeIn(pw_table))
        self.wait(8)

        for i in range(5):
            ballot_entry = table.get_rows()[i+1][0]
            ballot_entry_count = table.get_rows()[i+1][1]
            ballot_text = table_data[i+1][0]
            ballot_count = int(table_data[i+1][1])

            # highlight ballot entry and count
            self.play(
                ballot_entry.animate.set_color(YELLOW),
                ballot_entry_count.animate.set_color(YELLOW)
            )

            # animate B > C \n B > A \n C > A
            first = ballot_text[0]
            second = ballot_text[1]
            third = ballot_text[2]

            if first == "A":
                first_idx = 1
            elif first == "B":
                first_idx = 2
            else:
                first_idx = 3

            if second == "A":
                second_idx = 1
            elif second == "B":
                second_idx = 2
            else:
                second_idx = 3

            if third == "A":
                third_idx = 1
            elif third == "B":
                third_idx = 2
            else:
                third_idx = 3

            comp_1 = f"{first} > {second}"
            comp_2 = f"{first} > {third}"
            comp_3 = f"{second} > {third}"


            comp_text = VGroup(
                Text(comp_1, font_size=30, color=RED),
                Text(comp_2, font_size=30, color=BLUE),
                Text(comp_3, font_size=30, color=GREEN)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(table).shift(RIGHT*2)
            self.play(FadeIn(comp_text))
            if i == 0:
                self.wait(5)

            # change values in pw_scores
            pw_scores[first][second] += ballot_count
            pw_scores[first][third] += ballot_count
            pw_scores[second][third] += ballot_count


            # update pw_table_data 
            new_pw_table_data = self.generate_pw_table(pw_scores)
            new_pw_table = Table(
                new_pw_table_data,
                include_outer_lines=True
            ).scale(0.6).to_edge(LEFT).next_to(table).shift(RIGHT*5)

            self.play(FadeOut(pw_table), FadeIn(new_pw_table))

            # highlight the entries in pw_table
            entry_1 = new_pw_table.get_rows()[first_idx][second_idx]
            entry_2 = new_pw_table.get_rows()[first_idx][third_idx]
            entry_3 = new_pw_table.get_rows()[second_idx][third_idx]

            self.play(
                entry_1.animate.set_color(YELLOW),
                entry_2.animate.set_color(YELLOW),
                entry_3.animate.set_color(YELLOW),
            )
            if i == 0:
                self.wait(1)

            # unhighlight ballot entry and count
            self.play(
                ballot_entry.animate.set_color(WHITE),
                ballot_entry_count.animate.set_color(WHITE),
                entry_1.animate.set_color(WHITE),
                entry_2.animate.set_color(WHITE),
                entry_3.animate.set_color(WHITE),
                FadeOut(comp_text)
            )
            pw_table = new_pw_table
            pw_table_data = new_pw_table_data
            self.wait(0.5)

        self.wait(5)

        pairs = ["AB", "AC", "BC"]
        for pair in pairs:
            cand1 = pair[0]
            cand2 = pair[1]

            if cand1 == "A":
                first_idx = 1
            elif cand1 == "B":
                first_idx = 2
            else:
                first_idx = 3

            if cand2 == "A":
                second_idx = 1
            elif cand2 == "B":
                second_idx = 2
            else:
                second_idx = 3
            
            comp_text = Text(f"({cand1}, {cand2})", font_size=36, color=BLUE).next_to(table).shift(RIGHT*2)
            self.play(FadeIn(comp_text))
            
            entry_1 = pw_table.get_rows()[first_idx][second_idx]
            entry_2 = pw_table.get_rows()[second_idx][first_idx]
            self.play(
                entry_1.animate.set_color(YELLOW),
                entry_2.animate.set_color(YELLOW),
            )
            self.wait(4)
            
            if pw_scores[cand1][cand2] > pw_scores[cand2][cand1]:
                pw_scores[cand1][cand2] = 1
                pw_scores[cand2][cand1] = 0
            else:
                pw_scores[cand1][cand2] = 0
                pw_scores[cand2][cand1] = 1
            
            new_pw_table_data = self.generate_pw_table(pw_scores)
            new_pw_table = Table(
                new_pw_table_data,
                include_outer_lines=True
            ).scale(0.6).to_edge(LEFT).next_to(table).shift(RIGHT*5)
            entry_1 = new_pw_table.get_rows()[first_idx][second_idx]
            entry_2 = new_pw_table.get_rows()[second_idx][first_idx]

            self.play(FadeOut(pw_table), 
                      FadeIn(new_pw_table),  
                      entry_1.animate.set_color(YELLOW),
                      entry_2.animate.set_color(YELLOW))
            
            self.wait(4)
            self.play(entry_1.animate.set_color(WHITE),
                      entry_2.animate.set_color(WHITE),
                      FadeOut(comp_text))
            
            pw_table = new_pw_table
            pw_table_data = new_pw_table_data
            self.wait(4)

        self.wait(4)
        entry_1 = pw_table.get_rows()[2][1]
        entry_2 = pw_table.get_rows()[2][3]
        self.play(
            entry_1.animate.set_color(YELLOW),
            entry_2.animate.set_color(YELLOW)
        )
        self.wait(4)

        cond_winner_text = Text("Condorcet Winner = Betty", color=BLUE, font_size=36)
        cond_winner_text.next_to(table, DOWN, buff=1).shift(RIGHT*3)
        self.play(Write(cond_winner_text), run_time=2)
        self.wait(4)

        self.play(
            entry_1.animate.set_color(WHITE),
            entry_2.animate.set_color(WHITE)
        )

        self.wait(2)

        self.play(
            FadeOut(table),
            FadeOut(cond_winner_text),
            pw_table.animate.shift(LEFT*8)
        )

        vertices = ["A", "B", "C"]
        edges = [("A", "B"), ("C", "B"), ("A", "C")]

        edge_config = {
            "stroke_width": 2,
            "tip_config": {"tip_length": 0.2, "tip_width": 0.2}
        }

        vertex_config = {
            "A": {"fill_color": RED},
            "B": {"fill_color": BLUE},
            "C": {"fill_color": GREEN}
        }

        g = DiGraph(
            vertices,
            edges,
            labels=True,
            edge_config=edge_config,
            vertex_config=vertex_config
        ).next_to(pw_table, RIGHT).shift(RIGHT*4)

        self.play(Create(g))
        self.wait(2)

        a_vertex = g.vertices["A"]
        a_ring = Circle(radius=0.4, color=YELLOW).move_to(a_vertex)

        self.play(Create(a_ring))

        # Scale up vertices B and C
        b_vertex = g.vertices["B"]
        c_vertex = g.vertices["C"]
        self.play(
            b_vertex.animate.scale(1.2),
            c_vertex.animate.scale(1.2)
        )
        self.wait(1)
        self.play(
            b_vertex.animate.scale(1/1.2),
            c_vertex.animate.scale(1/1.2)
        )

        # Reset edges to white and remove the ring
        self.play(FadeOut(a_ring))
        self.wait(2)

        c_vertex = g.vertices["C"]
        c_ring = Circle(radius=0.4, color=YELLOW).move_to(c_vertex)

        self.play(Create(c_ring))

        # Scale up vertex B
        b_vertex = g.vertices["B"]
        self.play(b_vertex.animate.scale(1.2))
        self.wait(1)
        self.play(b_vertex.animate.scale(1/1.2))

        # Reset edges to white and remove the ring
        self.play(FadeOut(c_ring))
        self.wait(2)

        self.play(
            FadeOut(pw_table),
            g.animate.shift(LEFT*4).scale(1.4)
        )
        self.wait(4)

        '''
        in the next video we'll look at how we can use these graphs for other, more complex RCV algorithms
        until next time
        '''
        tbc = Text("To Be Continued...", font_size=48).to_edge(UP).shift(DOWN*4)
        self.play(Uncreate(g))
        self.play(Write(tbc))


