import streamlit as st
from modeci_mdf.mdf import *
from modeci_mdf.utils import simple_connect
from modeci_mdf.execution_engine import EvaluableGraph
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as PILImage
#from IPython.display import Image

def app():
    st.title("Multi-Mass System Simulation")
    st.write("Click the button below to run the simulation.")

    if st.button("Run Simulation"):
        execute_model()

def execute_model():
    # Define system parameters
    m1 = 1.0  # mass of the first object (kg)
    m2 = 2.0  # mass of the second object (kg)
    m3 = 1.5  # mass of the third object (kg)
    k1 = 10.0  # spring constant for the first spring (N/m)
    k2 = 15.0  # spring constant for the second spring (N/m)

    # Create a new Model
    multi_mass_model = Model(id="MultiMass_Model")

    # Create a Graph inside the Model
    multi_mass_graph = Graph(id="MultiMass_Graph")
    multi_mass_model.graphs.append(multi_mass_graph)

    # Parameters for the masses and springs
    mass1_param = Parameter(id="mass1", value=m1)
    mass2_param = Parameter(id="mass2", value=m2)
    mass3_param = Parameter(id="mass3", value=m3)
    spring1_param = Parameter(id="spring1", value=k1)
    spring2_param = Parameter(id="spring2", value=k2)

    # Node for the first mass
    mass1_node = Node(id="Mass1_Node")

    # Adding parameters to the first mass node
    mass1_node.parameters.append(mass1_param)

    # Output port for the first mass node
    mass1_output_port = OutputPort(id="mass1_output_port", value="mass1")
    mass1_node.output_ports.append(mass1_output_port)

    # Node for the second mass
    mass2_node = Node(id="Mass2_Node")

    # Adding parameters to the second mass node
    mass2_node.parameters.append(mass2_param)

    # Output port for the second mass node
    mass2_output_port = OutputPort(id="mass2_output_port", value="mass2")
    mass2_node.output_ports.append(mass2_output_port)

    # Node for the third mass
    mass3_node = Node(id="Mass3_Node")

    # Adding parameters to the third mass node
    mass3_node.parameters.append(mass3_param)

    # Output port for the third mass node
    mass3_output_port = OutputPort(id="mass3_output_port", value="mass3")
    mass3_node.output_ports.append(mass3_output_port)

    # Add nodes to the graph
    multi_mass_graph.nodes.extend([mass1_node, mass2_node, mass3_node])

    # Define edges representing the springs between masses
    spring1_edge = Edge(id="spring1_edge", sender=mass1_node.id, receiver=mass2_node.id, sender_port="mass1_output_port", receiver_port="mass2_output_port")
    spring2_edge = Edge(id="spring2_edge", sender=mass2_node.id, receiver=mass3_node.id, sender_port="mass2_output_port", receiver_port="mass3_output_port")

    # Add edges to the graph
    multi_mass_graph.edges.extend([spring1_edge, spring2_edge])

    # Generate a graph image
    graph_image_file = "MultiMassSystem.png"
    multi_mass_model.to_graph_image(engine="dot", output_format="png", filename_root="MultiMassSystem", is_horizontal=True)

    # Display the generated graph image
    st.write("Displaying the generated graph image")
    #st.image(graph_image_file)
    pil_image = PILImage.open(graph_image_file)


     # Define time array
    t = np.linspace(0, 10, 100)

    # Define displacement functions (e.g., sine waves for simplicity)
    displacement1 = np.sin(t)
    displacement2 = np.cos(t)
    displacement3 = np.sin(t + np.pi/4)  # Adding phase difference for variety

    # Plotting the displacements over time
    st.write("Plotting the displacements over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, displacement1, label='Mass 1', color='blue')
    plt.plot(t, displacement2, label='Mass 2', color='orange')
    plt.plot(t, displacement3, label='Mass 3', color='green')
    plt.xlabel('Time')
    plt.ylabel('Displacement')
    plt.title('Displacement over Time for Multiple Masses')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Calculate kinetic energy (KE)
    def calculate_ke(m, v):
        return 0.5 * m * v ** 2

    # Calculate potential energy (PE)
    def calculate_pe(k, x):
        return 0.5 * k * x ** 2

    # Define velocity functions (e.g., cosine waves for simplicity)
    velocity1 = np.cos(t)
    velocity2 = np.sin(t)
    velocity3 = np.cos(t + np.pi/6)  # Adding phase difference for variety

    # Define spring extensions (e.g., sine waves for simplicity)
    extension1 = np.sin(t)
    extension2 = np.cos(t)
    extension3 = np.sin(t + np.pi/3)  # Adding phase difference for variety

    # Calculate kinetic energy for each mass
    ke1 = calculate_ke(m1, velocity1)
    ke2 = calculate_ke(m2, velocity2)
    ke3 = calculate_ke(m3, velocity3)

    # Calculate potential energy for each spring
    pe1 = calculate_pe(k1, extension1)
    pe2 = calculate_pe(k2, extension2)
    pe_total = pe1 + pe2  # Total potential energy of the system

    # Calculate total energy of the system
    te = ke1 + ke2 + ke3 + pe_total

    # Plotting the kinetic energy over time
    st.write("Plotting the kinetic energy over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, ke1, label='KE Mass 1', color='blue')
    plt.plot(t, ke2, label='KE Mass 2', color='orange')
    plt.plot(t, ke3, label='KE Mass 3', color='green')
    plt.xlabel('Time')
    plt.ylabel('Kinetic Energy')
    plt.title('Kinetic Energy over Time for Multiple Masses')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Plotting the potential energy over time
    st.write("Plotting the potential energy over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, pe1, label='PE Spring 1', color='blue')
    plt.plot(t, pe2, label='PE Spring 2', color='orange')
    plt.plot(t, pe_total, label='Total PE', color='green')
    plt.xlabel('Time')
    plt.ylabel('Potential Energy')
    plt.title('Potential Energy over Time for Multiple Springs')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Plotting the total energy over time
    st.write("Plotting the total energy over time")
    plt.figure(figsize=(10, 5))
    plt.plot(t, te, label='Total Energy', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Total Energy')
    plt.title('Total Energy over Time for the System')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)





if __name__ == "__main__":
    app()
