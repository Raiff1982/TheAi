import os
import json
import matplotlib.pyplot as plt

folder = './astro_cocoons/'
quantum_states = []
chaos_states = []
proc_ids = []
labels = []

for fname in os.listdir(folder):
    if fname.endswith('.cocoon'):
        with open(os.path.join(folder, fname), 'r') as f:
            data = json.load(f)['data']
            quantum_states.append(data['quantum_state'])
            chaos_states.append(data['chaos_state'])
            proc_ids.append(data.get('run_by_proc', -1))
            labels.append(fname)

print("\nStep-by-step Fact Table:\n")
print("Cocoon File | Quantum State | Chaos State | Proc/CoreID")
print("--------------------------------------------")
for l,q,c,p in zip(labels, quantum_states, chaos_states, proc_ids):
    print(f"{l} | {q} | {c} | {p}")

# Simple scatter plot of quantum state 0 vs. chaos state 0
x = [q[0] for q in quantum_states]
y = [c[0] for c in chaos_states]

plt.figure(figsize=(8,6))
plt.scatter(x, y, c=proc_ids, cmap='hsv', s=80)
plt.xlabel('Quantum State Value [0]')
plt.ylabel('Chaos State Value [0]')
plt.title('Quantum vs. Chaos Distribution Across Cores')
plt.colorbar(label="Core/Proc ID")
plt.grid(True)
plt.show()
