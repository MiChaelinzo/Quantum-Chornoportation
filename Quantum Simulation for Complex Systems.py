import cirq
import matplotlib.pyplot as plt

# Define qubits
qubits = cirq.LineQubit.range(4)

# Example Hamiltonian: H = X⊗X + Z⊗I
hamiltonian = cirq.PauliString(cirq.X(qubits[0]) * cirq.X(qubits[1])) + cirq.PauliString(cirq.Z(qubits[0]))

# Define simulation time steps and parameters
time_steps = 100
time_step_size = 0.01

# Construct the simulation circuit
circuit = cirq.Circuit()
for step in range(time_steps):
    # Implement the Hamiltonian evolution for each time step
    circuit.append(cirq.PauliStringPhasor(hamiltonian, exponent=time_step_size))

# Simulate the circuit
simulator = cirq.Simulator()
results = simulator.simulate(circuit, qubit_order=qubits)

# Analyze the simulation results
# Example observables: X on qubit 0, Z on qubit 1, and X⊗X on qubits 0 and 1
observables = [cirq.X(qubits[0]), cirq.Z(qubits[1]), cirq.X(qubits[0]) * cirq.X(qubits[1])]

# Calculate expectation values for each observable at each time step
expectation_values = []
for step, state_vector in enumerate(results.final_state_vector):
    step_expectations = []
    for observable in observables:
        expectation = cirq.PauliString(observable).expectation_from_state_vector(state_vector, qubits)
        step_expectations.append(expectation.real)
    expectation_values.append(step_expectations)

# Plotting
time_array = [step * time_step_size for step in range(time_steps)]  # Time values for x-axis

plt.figure()
labels = ["X0", "Z1", "X0X1"]  # Labels for each observable
for i, observable_expectations in enumerate(zip(*expectation_values)):
    plt.plot(time_array, observable_expectations, label=labels[i])

plt.xlabel("Time")
plt.ylabel("Expectation Value")
plt.title("Evolution of Observables")
plt.legend()
plt.show()
