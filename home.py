import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modeci_mdf.mdf import *
from modeci_mdf.utils import simple_connect
from modeci_mdf.execution_engine import EvaluableGraph
import graphviz
from graphviz import Source
#import os
#os.environ["PATH"] += os.pathsep + 'C:/path/to/graphviz/bin'


def app():
    st.title('MDF Model')


    def create_model(x_val=1.0, y_val=2.0, z_val=3.0):
        model = Model(id="DynamicalSystem")
        graph = Graph(id="system_graph")
        model.graphs.append(graph)

        node1 = Node(id="Node1", metadata={"color": "0 .8 0"})
        node2 = Node(id="Node2", metadata={"color": ".8 0 0"})
        node3 = Node(id="Node3", metadata={"color": "0 0 .8"})

        node1.parameters.append(Parameter(id="x", value=x_val))
        node1.output_ports.append(OutputPort(id="x", value="x"))

        node2.parameters.append(Parameter(id="y", value=y_val))
        node2.parameters.append(Parameter(id="dy_dt", value="-x * y**2"))
        node2.input_ports.append(InputPort(id="x"))
        node2.output_ports.append(OutputPort(id="y", value="y"))
        node2.output_ports.append(OutputPort(id="dy_dt", value="dy_dt"))

        node3.parameters.append(Parameter(id="z", value=z_val))
        node3.parameters.append(Parameter(id="dz_dt", value="x * y - z"))
        node3.input_ports.append(InputPort(id="x"))
        node3.input_ports.append(InputPort(id="y"))
        node3.output_ports.append(OutputPort(id="z", value="z"))
        node3.output_ports.append(OutputPort(id="dz_dt", value="dz_dt"))

        graph.nodes.append(node1)
        graph.nodes.append(node2)
        graph.nodes.append(node3)

        simple_connect(node1, node2, graph)
        simple_connect(node1, node3, graph)
        simple_connect(node2, node3, graph)

        return model

    # Model parameters in the main section
    st.markdown("## Model Parameters")
    x_val = st.number_input("Initial value of x", min_value=0.1, max_value=10.0, value=1.0)
    y_val = st.number_input("Initial value of y", min_value=0.1, max_value=10.0, value=2.0)
    z_val = st.number_input("Initial value of z", min_value=0.1, max_value=10.0, value=3.0)

    # Button to execute the model
    if st.button("Execute Model"):
        # Create the model with user-selected parameters
        model = create_model(x_val, y_val, z_val)

        # Evaluate the model
        eg = EvaluableGraph(model.graphs[0], verbose=False)

        progress_bar = st.progress(0)  # Create a progress bar
        for i in range(100):
            eg.evaluate(time_increment=0.1)
            progress_bar.progress(i + 1)  # Update the progress bar

        # Display output
        x = eg.enodes["Node1"].evaluable_outputs["x"].curr_value
        y = eg.enodes["Node2"].evaluable_outputs["y"].curr_value
        z = eg.enodes["Node3"].evaluable_outputs["z"].curr_value

        st.write(f"Output of Node1: x = {x}")
        st.write(f"Output of Node2: y = {y}")
        st.write(f"Output of Node3: z = {z}")

        # Plot the output in real-time
        time_points = np.linspace(0, 10, 100)
        x_values = []
        y_values = []
        z_values = []

        fig, ax = plt.subplots()
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title("MDF Model Output")

        for t in time_points:
            eg.evaluate(time_increment=0.1)
            x_values.append(eg.enodes["Node1"].evaluable_outputs["x"].curr_value)
            y_values.append(eg.enodes["Node2"].evaluable_outputs["y"].curr_value)
            z_values.append(eg.enodes["Node3"].evaluable_outputs["z"].curr_value)

        ax.plot(time_points, x_values, label="x")
        ax.plot(time_points, y_values, label="y")
        ax.plot(time_points, z_values, label="z")
        ax.legend()

        st.pyplot(fig)


         # Generate a graph image with absolute path to Graphviz executables
       # model.to_graph_image(
       # engine="dot",
       # output_format="png",
       # filename_root="DynamicalSystem",
       # is_horizontal=True,

       # )
