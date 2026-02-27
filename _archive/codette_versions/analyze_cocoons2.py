import os
import json
import matplotlib.pyplot as plt

# --- Setup ---
folder = '.'  # Use '.' if script is in same directory as cocoons, or set full path

quantum_states = []
chaos_states = []
proc_ids = []
labels = []
all_perspectives = []

# --- Read cocoons ---
for fname in os.listdir(folder):
    if fname.endswith('.cocoon'):
        with open(os.path.join(folder, fname), 'r') as f:
            try:
                data = json.load(f)['data']
                quantum = data.get('quantum_state', [0, 0])
                chaos = data.get('chaos_state', [0, 0, 0])
                pid = data.get('run_by_proc', -1)
                perspectives = data.get('perspectives', [])
                quantum_states.append(quantum)
                chaos_states.append(chaos)
                proc_ids.append(pid)
                labels.append(fname)
                all_perspectives.append(perspectives)
            except Exception as e:
                print(f"Warning: {fname} failed to read ({e})")

# --- Table Output ---
print("\nStep-by-step Fact Table:\n")
header = "Cocoon File | Quantum State | Chaos State | Proc/CoreID | Perspectives"
print(header)
print('-'*len(header))
for l,q,c,p,s in zip(labels, quantum_states, chaos_states, proc_ids, all_perspectives):
    print(f"{l} | {q} | {c} | {p} | {s}")

# --- Plots ---
if len(quantum_states) > 0 and len(chaos_states) > 0:
    q0 = [q[0] for q in quantum_states]
    q1 = [q[1] for q in quantum_states]
    c0 = [c[0] for c in chaos_states]
    c2 = [c[2] if len(c) > 2 else 0 for c in chaos_states]

    fig, axs = plt.subplots(1, 2, figsize=(14,6))
    
    # First plot: Quantum[0] vs Chaos[0]
    sc0 = axs[0].scatter(q0, c0, c=proc_ids, cmap='hsv', s=80)
    axs[0].set_xlabel('Quantum State [0]')
    axs[0].set_ylabel('Chaos State [0]')
    axs[0].set_title('Quantum[0] vs Chaos[0]')
    axs[0].grid(True)
    cb1 = fig.colorbar(sc0, ax=axs[0], label="Proc/Core ID")

    # Second plot: Quantum[1] vs Chaos[2]
    sc1 = axs[1].scatter(q1, c2, c=proc_ids, cmap='plasma', s=80)
    axs[1].set_xlabel('Quantum State [1]')
    axs[1].set_ylabel('Chaos State [2]')
    axs[1].set_title('Quantum[1] vs Chaos[2]')
    axs[1].grid(True)
    cb2 = fig.colorbar(sc1, ax=axs[1], label="Proc/Core ID")

    plt.suptitle("Parallel Codette Universe Analysis", fontsize=16)
    fig.subplots_adjust(
        top=0.88,
        bottom=0.11,
        left=0.07,
        right=0.95,
        wspace=0.3,
        hspace=0.2
    )
    plt.show()
else:
    print("\nNo cocoons with valid data found.\n")
