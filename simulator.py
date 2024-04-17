import sys

def read_nfa(filename):
    with open(filename, 'r') as file:
        n_states = int(file.readline().strip())
        initial_state = int(file.readline().strip())
        accepting_states = set(map(int, file.readline().strip().split()))
        transitions = {i: {} for i in range(n_states)}

        for line in file:
            parts = line.strip().split()
            start_state = int(parts[0])
            transition_symbol = parts[1]
            end_state = int(parts[2])

            if transition_symbol not in transitions[start_state]:
                transitions[start_state][transition_symbol] = set()
            transitions[start_state][transition_symbol].add(end_state)
    return n_states, initial_state, accepting_states, transitions

def simulate_nfa(n_states, initial_state, accepting_states, transitions, input_string):
    current_states = {initial_state}
    
    for symbol in input_string:
        next_states = set()
        for state in current_states:
            if symbol in transitions[state]:
                next_states.update(transitions[state][symbol])
        current_states = next_states

    if current_states & accepting_states:
        return "accept"
    else:
        return "reject"

def main():
    filename = sys.argv[1]
    n_states, initial_state, accepting_states, transitions = read_nfa(filename)
    
    for line in sys.stdin:
        input_string = line.strip()
        result = simulate_nfa(n_states, initial_state, accepting_states, transitions, input_string)
        print(result)

if __name__ == "__main__":
    main()
