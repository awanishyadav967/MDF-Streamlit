import streamlit as st
from modeci_mdf.mdf import *
from modeci_mdf.utils import simple_connect
from modeci_mdf.execution_engine import EvaluableGraph
import numpy as np
import matplotlib.pyplot as plt

def app():
    st.title("Spring-Mass-Damper System Simulation")
    st.write("Click the button below to run the simulation.")

    if st.button("Run Simulation"):
        execute_model()

def execute_model():
    # Create a new Model
    model = Model(id="SpringMassSystem")

    # Create a Graph inside the Model
    graph = Graph(id="system_graph")

    # Append the Graph object to the Model
    model.graphs.append(graph)

    # Create nodes
    node1 = Node(id="Mass", metadata={"color": "0 .8 0"})
    node2 = Node(id="Spring", metadata={"color": ".8 0 0"})
    node3 = Node(id="Damper", metadata={"color": "0 0 .8"})

    # Add parameters and ports to nodes
    # Mass node
    node1.parameters.extend([
        Parameter(id="position", value=1.0),
        Parameter(id="velocity", value=0.0)
    ])
    node1.output_ports.append(OutputPort(id="position_output", value="position"))
    node1.input_ports.append(InputPort(id="force"))

    # Spring node
    node2.parameters.extend([
        Parameter(id="position", value=0.0),
        Parameter(id="stiffness", value=1.0)  # Spring constant
    ])
    node2.output_ports.append(OutputPort(id="force_output", value="stiffness * position"))
    node2.input_ports.append(InputPort(id="position"))

    # Damper node
    node3.parameters.extend([
        Parameter(id="velocity", value=0.0),
        Parameter(id="damping", value=0.1)  # Damping coefficient
    ])
    node3.output_ports.append(OutputPort(id="force_output", value="damping * velocity"))
    node3.input_ports.append(InputPort(id="velocity"))

    # Add nodes to the graph
    graph.nodes.extend([node1, node2, node3])

    # Connect nodes
    simple_connect(node1, node2, graph)
    simple_connect(node1, node3, graph)

    # Generate a graph image
    model.to_graph_image(engine="dot", output_format="png", filename_root="SpringMassSystem", is_horizontal=True)

    # Execute the graph over time
    eg = EvaluableGraph(graph, verbose=False)
    dt = 0.01  # Time step
    duration = 10  # Simulation duration
    t = 0
    times = []
    position_values = []

    while t <= duration:
        times.append(t)
        eg.evaluate(time_increment=dt)
        position_values.append(eg.enodes["Mass"].evaluable_outputs["position_output"].curr_value)  # Accessing position output port value

        # Update the position of the mass based on a sinusoidal motion
        omega = 2 * np.pi  # Angular frequency (radians per second)
        amplitude = 0.5  # Amplitude of the sinusoidal motion
        offset = 1.0  # Offset from the equilibrium position
        node1.parameters[0].value = amplitude * np.sin(omega * t) + offset  # Accessing position parameter value

        t += dt

    # Display the graph image in Streamlit
    st.title("Spring-Mass-Damper System")
    st.image("SpringMassSystem.png")

    # Display the time evolution of the system in Streamlit
    st.subheader("Time Evolution")
    st.write("Time (t)")
    st.write(times)
    st.write("Position of the Mass (x)")
    st.write(position_values)

    # Plot the time evolution
    plt.figure(figsize=(10, 6))
    plt.plot(times, position_values)
    plt.xlabel('Time (t)')
    plt.ylabel('Position of the Mass (x)')
    plt.title('Time Evolution of Spring-Mass-Damper System')
    plt.grid(True)
    st.pyplot(plt)



