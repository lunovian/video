from manim import *

class WhatIsNeuralNetwork(Scene):
    def construct(self):
        # Title
        title = Text("What is a Neural Network?", font_size=40)
        subtitle = Text("(in baby language)", font_size=32, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        title.to_edge(UP)
        self.play(SpinInFromNothing(title))
        self.wait(1)
        
        self.play(FadeIn(subtitle))
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))

        # Create the friend analogy text
        explanation = Text(
            "Imagine you and your friends trying to identify \n a kitty or a puppy...",
            font_size=32
        ).to_edge(UP)
        
        # Create neural network structure with good spacing
        input_text = ["Pointy Ears", "Fluffy Tail", "Wet Nose"]
        input_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.4, color=BLUE)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.8)
        
        # Create and position feature labels with more space
        input_labels = VGroup(*[
            Text(text, font_size=20)
            for text in input_text
        ])
        
        # Position each label to the left of its node with specific spacing
        for label, node in zip(input_labels, input_layer):
            label.next_to(node, LEFT, buff=0.5)  # Increased buffer space

        # Create a group for input layer and its labels
        input_group = VGroup(input_layer, input_labels)

        # Position everything else
        hidden_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.4, color=GREEN)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.8)

        output_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0.4, color=RED)
            for _ in range(2)
        ]).arrange(DOWN, buff=1.2)

        # Position all layers with more space between them
        layers = VGroup(input_group, hidden_layer, output_layer).arrange(RIGHT, buff=3)
        
        # Create connections
        connections = VGroup()
        for i in input_layer:
            for h in hidden_layer:
                connections.add(Line(
                    start=i.get_right(),
                    end=h.get_left(),
                    stroke_opacity=0.3
                ))
        for h in hidden_layer:
            for o in output_layer:
                connections.add(Line(
                    start=h.get_right(),
                    end=o.get_left(),
                    stroke_opacity=0.3
                ))

        # Animation sequence
        self.play(Write(explanation))
        self.wait()
        
        # Show network components
        self.play(
            Create(input_layer),
            Create(hidden_layer),
            Create(output_layer),
            Write(input_labels),
        )
        # Slower connection animation with higher run_time
        self.play(
            Create(connections, lag_ratio=0.1),  # Added lag_ratio for smoother animation
            run_time=3  # Increased from default to 3 seconds
        )

        # Animate information flow
        for _ in range(2):
            # Highlight each input feature
            for i, label in enumerate(input_labels):
                highlight = label.copy().set_color(YELLOW)
                self.play(Transform(label, highlight), run_time=0.5)
                
                # Create and move square through connections
                square = Square(side_length=0.2, fill_opacity=0.8, color=BLUE)
                square.move_to(input_layer[i])
                
                self.play(
                    square.animate.move_to(hidden_layer[i]),
                    run_time=0.5
                )
                self.play(FadeOut(square))
        
        # Final decision animation
        decision = Text("It's a puppy!", font_size=36, color=YELLOW)
        decision.to_edge(DOWN)
        self.play(Write(decision))
        
        self.wait(2)
