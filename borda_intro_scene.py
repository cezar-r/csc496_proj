from manim import *

class BordaIntroScene(Scene):

    def get_new_cand_table(self, cum_scores):
        table = [["Candidate", "Borda Score"]]
        
        for k, v in cum_scores.items():
            table.append([k, str(v)])
        return table

    def construct(self):
        table_data = [
            ["Ballot", "Count"],
            ["BCA", "8"],
            ["ABC", "6"],
            ["CBA", "5"],
            ["ACB", "4"],
            ["BAC", "2"]
        ]

        table = Table(
            table_data,
            include_outer_lines=True
        ).scale(0.5).to_edge(LEFT)

        # Create the "Borda Count" text
        borda_count_text = Text("Borda Count", font_size=48).scale(0.8).next_to(table, UP, buff=0.5)
        borda_score_text = Text("\"Borda Score\"", color=BLUE, font_size=36).next_to(table, RIGHT, buff=1).shift(UP*1.75)


        # Fade in and out the "Borda Count" text
        self.play(FadeIn(borda_count_text))
        self.wait(4)
        self.play(FadeOut(borda_count_text))

        # Fade in the table
        self.play(FadeIn(table))
        self.wait(8)

        self.play(FadeIn(borda_score_text))
        self.wait(2)
        
        # Create the candidate scores table
        candidate_scores_data = [
            ["Candidate", "Borda Score"],
            ["A", "0"],
            ["B", "0"],
            ["C", "0"]
        ]

        candidate_scores_table = Table(
            candidate_scores_data,
            include_outer_lines=True
        ).scale(0.4).next_to(borda_score_text, DOWN*5, buff=0.5).shift(RIGHT*2)

        self.play(FadeIn(candidate_scores_table))
        self.wait(2)
        self.play(FadeOut(borda_score_text))

        cumulative_scores = {"A": 0, "B": 0, "C": 0}

        def smooth(t, inflection=10.0, speed_factor=1):
            error = sigmoid(-inflection / 2)
            return np.clip(
                (sigmoid(inflection * (speed_factor * t - 0.5)) - error) / (1 - 2 * error),
                0, 1
            )

        def sigmoid(x):
            return 1 / (1 + np.exp(-x))
        
        for i in range(5):
            if i == 0:
                rate_func = smooth
            else:
                rate_func = lambda t, speed_factor=32: smooth(t, speed_factor=speed_factor)

            ballot_entry = table.get_rows()[i+1][0]
            ballot_text = table_data[i+1][0]
            ballot_letters = VGroup(*[Text(char, font_size=36) for char in ballot_text])
            ballot_letters.arrange(RIGHT, buff=3).next_to(borda_score_text, UP*.5, buff=0.5).shift(RIGHT*2.25)
            
            self.play(
                TransformFromCopy(ballot_entry, ballot_letters),
                rate_func = rate_func
            )
            if i == 0:
                self.wait(1)
            line = Line(ballot_letters.get_left(), ballot_letters.get_right(), color=RED).next_to(ballot_letters, DOWN, buff=0.2)
            arrow = Arrow(line.get_left(), line.get_left() + LEFT * 0.5, buff=0, color=RED)
            ticks = VGroup(*[Line(UP * 0.1, DOWN * 0.1, color=RED).next_to(letter, DOWN, buff=0.4) for letter in ballot_letters])

            self.play(Create(line), GrowArrow(arrow), Create(ticks), rate_func = rate_func)
            if i == 0:
                self.wait(2)

            if i == 0:
                n_labels = VGroup(
                    Text("n-1", font_size=30, color = WHITE).next_to(ticks[0], DOWN, buff=0.2),
                    Text("n-2", font_size=30, color = WHITE).next_to(ticks[1], DOWN, buff=0.2),
                    Text("0", font_size=30, color = WHITE).next_to(ticks[2], DOWN, buff=0.2)
                )
                self.play(FadeIn(n_labels), rate_func = rate_func)
                self.wait(4)

                # replace the ticks
                point_labels = VGroup(
                    Text("2", font_size=30, color = WHITE).next_to(ticks[0], DOWN, buff=0.2),
                    Text("1", font_size=30, color = WHITE).next_to(ticks[1], DOWN, buff=0.2),
                    Text("0", font_size=30, color = WHITE).next_to(ticks[2], DOWN, buff=0.2)
                )

                self.play(ReplacementTransform(n_labels, point_labels), rate_func = rate_func)
                self.wait(4)
            else:
                point_labels = VGroup(
                    Text("2", font_size=30, color = WHITE).next_to(ticks[0], DOWN, buff=0.2),
                    Text("1", font_size=30, color = WHITE).next_to(ticks[1], DOWN, buff=0.2),
                    Text("0", font_size=30, color = WHITE).next_to(ticks[2], DOWN, buff=0.2)
                )
                self.play(FadeIn(point_labels), rate_func = rate_func)
                self.wait(1)

            ballot_entry.animate.set_color(YELLOW)
            ballot_count = table.get_rows()[i+1][1]
            ballot_count_num = int(table_data[i+1][1])
            
            for j in range(3):
                
                b_points = point_labels[j]
                points_num = 2 - j
                letter = ballot_text[j]
                borda_score_text_b = MathTex(fr"\text{{borda\_score}}({letter}, {ballot_text}) = ", font_size=36).move_to(
                    (line.get_center() + candidate_scores_table.get_top()) / 2 + DOWN * 0.5
                ).shift(LEFT*2)

                self.play(Write(borda_score_text_b), rate_func = rate_func)
                if i == 0:
                    self.wait(1)

                self.play(
                    ballot_count.animate.set_color(YELLOW),
                    b_points.animate.set_color(YELLOW),
                    rate_func = rate_func
                )

                if i == 0:
                    self.wait(1)

                ballot_count_copy = MathTex(fr"{ballot_count_num}", font_size=36, color=YELLOW)
                b_points_copy = MathTex(fr"{points_num}", font_size=36, color=YELLOW)

                self.play(
                    TransformFromCopy(ballot_count, ballot_count_copy.next_to(borda_score_text_b, RIGHT)),
                    TransformFromCopy(b_points, b_points_copy.next_to(ballot_count_copy, RIGHT, buff=0.6)),
                    FadeToColor(ballot_count, WHITE),
                    FadeToColor(b_points, WHITE),
                    rate_func = rate_func
                )

                multiplication_sign = MathTex(r"\times", font_size=36).next_to(ballot_count_copy, RIGHT, buff=0.2)

                self.play(Write(multiplication_sign), rate_func = rate_func)
                if i == 0:
                    self.wait(2)

                # Add equal sign and result
                equal_sign = MathTex(r"=", font_size=36).next_to(b_points_copy, RIGHT, buff=0.2)
                result = MathTex(fr"{points_num*ballot_count_num}", font_size=36, color=YELLOW).next_to(equal_sign, RIGHT, buff=0.2)


                self.play(Write(equal_sign), Write(result), rate_func = rate_func)
                if i == 0:
                    self.wait(1)

                self.play(result.animate.set_color(YELLOW), rate_func = rate_func)
                if i == 0:
                    self.wait(1)

                # Update the Borda score in the candidate scores table
                if letter == 'B':
                    idx = 5
                elif letter == 'A':
                    idx = 3
                else:
                    idx = 7

                prev_score = cumulative_scores[letter]
                new_score = prev_score + points_num*ballot_count_num
                cumulative_scores[letter] = new_score

                b_score = candidate_scores_table.get_entries_without_labels()[idx]
                result_copy = result.copy()

                new_table_data = self.get_new_cand_table(cumulative_scores)
                new_candidate_scores_table = Table(
                    new_table_data,
                    include_outer_lines=True
                ).scale(0.4).next_to(borda_score_text, DOWN*5, buff=0.5).shift(RIGHT*2)

                self.play(
                    result_copy.animate.move_to(b_score).shift(RIGHT*.5),
                    rate_func=rate_func
                )
                self.play(
                    FadeOut(result_copy),
                    FadeOut(candidate_scores_table),
                    FadeIn(new_candidate_scores_table),
                    rate_func=rate_func
                    )
                self.wait(2)

                self.play(
                    FadeOut(borda_score_text_b),
                    FadeOut(ballot_count_copy),
                    FadeOut(b_points_copy),
                    FadeOut(multiplication_sign),
                    FadeOut(equal_sign),
                    FadeOut(result),
                    rate_func = rate_func
                )
                if i == 0:
                    self.wait(2)

                candidate_scores_table = new_candidate_scores_table

            self.play(
                FadeOut(ballot_letters),
                FadeOut(line),
                FadeOut(ticks),
                FadeOut(arrow),
                FadeOut(point_labels),
                rate_func = rate_func
            )

        new_candidate_scores_data = self.get_new_cand_table(cumulative_scores)

        new_candidate_scores_table = Table(
            new_candidate_scores_data,
            include_outer_lines=True
        ).scale(0.4).next_to(borda_score_text, DOWN*5, buff=0.5).shift(RIGHT*2)

        self.play(
            FadeOut(candidate_scores_table),
            FadeIn(new_candidate_scores_table)
            )
        self.wait(2)

        self.play(
            new_candidate_scores_table.animate.shift(UP * 2).scale(1.5),
            run_time=2
        )
        self.wait(1)

        # Highlight the "B" entry and its score
        b_entry = new_candidate_scores_table.get_entries_without_labels()[4]
        b_score = new_candidate_scores_table.get_entries_without_labels()[5]
        self.play(
            b_entry.animate.set_color(YELLOW),
            b_score.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(1)

        # Reset the colors
        self.play(
            b_entry.animate.set_color(WHITE),
            b_score.animate.set_color(WHITE),
            run_time=1
        )

        # # Display the "Borda Winner" text
        borda_winner_text = Text("Borda Winner = Betty", color=BLUE, font_size=36)
        borda_winner_text.next_to(new_candidate_scores_table, DOWN, buff=1)
        self.play(Write(borda_winner_text), run_time=2)
        self.wait(2)


# subtract 2 seconds from line 39
# add 4 to line 105