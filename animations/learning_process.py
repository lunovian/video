from manim import *
from manim.utils.rate_functions import ease_out_bounce, smooth, ease_in_out_sine

class LearningProcess(Scene):
    def construct(self):
        # Title
        title = Text("How Do Neural Networks Learn?", font_size=40)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5, rate_func=smooth)

        # Create simple network structure
        network = self.create_network()
        network.scale(0.7).shift(DOWN)
        
        # Show sections with smooth transitions
        self.show_training_process(network, title)
        self.wait(0.5)  # Brief pause between sections
        self.show_data_input(network, title)
        self.wait(0.5)  # Brief pause between sections
        self.show_feedback_loop(network, title)
        
        # Smooth fade out at the end
        self.play(
            FadeOut(network),
            FadeOut(title),
            run_time=1.5,
            rate_func=ease_in_out_sine
        )
        self.wait(1)

    def create_network(self):
        # Similar network creation as before but with unfilled circles
        input_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0, color=BLUE, stroke_width=2)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.8)
        
        hidden_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0, color=GREEN, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.8)
        
        output_layer = VGroup(*[
            Circle(radius=0.3, fill_opacity=0, color=RED, stroke_width=2)
            for _ in range(2)
        ]).arrange(DOWN, buff=0.8)

        all_layers = VGroup(input_layer, hidden_layer, output_layer).arrange(RIGHT, buff=3)
        
        # Create connections
        connections = VGroup()
        for i in input_layer:
            for h in hidden_layer:
                conn = Line(
                    start=i.get_right(),
                    end=h.get_left(),
                    stroke_opacity=0.2,
                    stroke_width=1
                )
                connections.add(conn)
        
        for h in hidden_layer:
            for o in output_layer:
                conn = Line(
                    start=h.get_right(),
                    end=o.get_left(),
                    stroke_opacity=0.2,
                    stroke_width=1
                )
                connections.add(conn)

        labels = VGroup(
            Text("Input", font_size=20).next_to(input_layer, UP),
            Text("Hidden", font_size=20).next_to(hidden_layer, UP),
            Text("Output", font_size=20).next_to(output_layer, UP)
        )
        
        return VGroup(all_layers, connections, labels)

    def show_training_process(self, network, title):
        training_text = Text("Training Process", font_size=32, color=YELLOW)
        training_text.next_to(title, DOWN, buff=0.5)
        
        # Smooth fade in of elements
        self.play(
            Write(training_text, run_time=1, rate_func=smooth),
            Create(network, run_time=2, rate_func=smooth)
        )
        
        # Gentle pulse for hidden layer
        self.play(
            Indicate(network[0][1], 
                    color=GREEN, 
                    scale_factor=1.1, 
                    run_time=1.5,
                    rate_func=smooth)
        )
        
        # Smoother data flow animation
        for _ in range(2):
            dot = Dot(color=BLUE, radius=0.1)
            dot.move_to(network[0][0][0])
            
            self.play(FadeIn(dot, run_time=0.3, rate_func=smooth))
            
            # Smooth movement through layers
            self.play(
                dot.animate.move_to(network[0][1][0]),
                run_time=1.2,
                rate_func=smooth
            )
            
            self.play(
                dot.animate.move_to(network[0][2][0]),
                run_time=1,
                rate_func=smooth
            )
            
            self.play(FadeOut(dot, run_time=0.3, rate_func=smooth))
        
        self.play(FadeOut(training_text, run_time=0.8, rate_func=smooth))

    def show_data_input(self, network, title):
        data_text = Text("Data Input", font_size=32, color=YELLOW)
        data_text.next_to(title, DOWN, buff=0.5)
        
        # Load and scale images
        cat_img = ImageMobject("media/images/learning_process/cat.png")
        dog_img = ImageMobject("media/images/learning_process/dog.jpg")
        
        # Scale and position images
        for img in [cat_img, dog_img]:
            img.scale(0.4)  # Make images smaller
        
        # Position images on the left side
        image_group = Group(cat_img, dog_img).arrange(DOWN, buff=1)
        image_group.next_to(network[0][0], LEFT, buff=2)
        
        # Add labels next to images
        labels = VGroup(
            Text("Cat", font_size=16, color=BLUE),
            Text("Dog", font_size=16, color=RED)
        )
        
        # Position labels next to corresponding images
        for label, img in zip(labels, [cat_img, dog_img]):
            label.next_to(img, RIGHT, buff=0.2)
        
        # Smoother transitions for images and labels
        self.play(
            Write(data_text, run_time=1, rate_func=smooth),
            FadeIn(image_group, run_time=1, rate_func=smooth),
            Write(labels, run_time=1, rate_func=smooth)
        )
        
        for i, (img, color) in enumerate([(cat_img, BLUE), (dog_img, RED)]):
            packet = Square(side_length=0.2, fill_opacity=0.8, color=color)
            packet.move_to(img.get_center())
            
            # Smoother image to packet transition
            self.play(
                img.animate.set_opacity(0.5),
                FadeIn(packet),
                run_time=0.8,
                rate_func=smooth
            )
            
            # Smooth movement to input layer
            input_node = network[0][0][i]
            self.play(
                packet.animate.move_to(input_node),
                run_time=1,
                rate_func=smooth
            )
            
            # Smoother fan-out animation
            hidden_dots = VGroup()
            for node in network[0][1]:
                new_packet = packet.copy()
                new_packet.set_color(GREEN)
                new_packet.move_to(node)
                hidden_dots.add(new_packet)
            
            self.play(
                Transform(packet, hidden_dots[0]),
                *[FadeIn(dot, rate_func=smooth) for dot in hidden_dots[1:]],
                run_time=1
            )
            
            # Smooth convergence to output
            output_packet = Square(
                side_length=0.2,
                fill_opacity=0.8,
                color=RED
            ).move_to(network[0][2][i])
            
            self.play(
                *[
                    Transform(
                        dot,
                        output_packet.copy(),
                        remover=True,
                        rate_func=smooth
                    )
                    for dot in hidden_dots
                ],
                run_time=1
            )
            
            # Smooth final packet animation
            final_packet = output_packet.copy()
            self.play(
                FadeIn(final_packet, run_time=0.5, rate_func=smooth),
                img.animate.set_opacity(1),
                run_time=0.8,
                rate_func=smooth
            )
            self.play(FadeOut(final_packet, run_time=0.5, rate_func=smooth))
        
        # Smooth cleanup
        self.play(
            FadeOut(image_group),
            FadeOut(labels),
            FadeOut(data_text),
            run_time=1,
            rate_func=smooth
        )

    def show_feedback_loop(self, network, title):
        feedback_text = Text("Feedback Loop", font_size=32, color=YELLOW)
        feedback_text.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(feedback_text, run_time=1, rate_func=smooth))
        
        # Smoother arrow animations
        arrows = []
        # Add arrows to connections from output to hidden
        for conn in network[1][len(network[1])//2:]:  # Second half of connections (hidden to output)
            arrow = Arrow(
                start=conn.point_from_proportion(0.7),
                end=conn.point_from_proportion(0.3),
                color=RED,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1,
                buff=0.1
            )
            arrows.append(arrow)
        
        # Add arrows to connections from hidden to input
        for conn in network[1][:len(network[1])//2]:  # First half of connections (input to hidden)
            arrow = Arrow(
                start=conn.point_from_proportion(0.7),
                end=conn.point_from_proportion(0.3),
                color=RED,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1,
                buff=0.1
            )
            arrows.append(arrow)

        # Animate arrows with smooth timing
        self.play(
            *[GrowArrow(arrow, rate_func=smooth) for arrow in arrows],
            run_time=2.5,
            lag_ratio=0.05  # Smaller lag ratio for smoother sequence
        )
        
        # Smooth cleanup
        self.play(
            FadeOut(feedback_text),
            *[FadeOut(arrow) for arrow in arrows],
            run_time=1,
            rate_func=smooth
        )
