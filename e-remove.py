import sys

def read(fileName):
  # Open the file in read mode ('r')
  with open(fileName, 'r') as file:
    global n_states, alphabet_size, alphabet, accepting, transitions
    
    lines = file.readlines()
    
    # getting the numbers at the end of the line for the variables
    n_states = int(lines[0].split(': ')[1])
    alphabet_size = int(lines[1].split(': ')[1])
    
    # creates a list of alphabet depending on alphabet size starting from 'a', 'b', etc.
    alphabet = [chr(ord('a') + i) for i in range(alphabet_size)]
    
    # getting accepting states
    accepting = set(map(int, lines[2].split(': ')[1].split()))
    
    # init transitions with 'e' and all other states pointing to empty set
    transitions = {state: {'e': set()} for state in range(n_states)}
    for symbol in alphabet:
      for state in range(n_states):
        transitions[state][symbol] = set()
        

    # getting transitions
    for state, line in enumerate(lines[3:]):
      transition_states = line.strip().split()
      #print(f"{transition_states}/n")
      for i, symbol in enumerate(transition_states):
        #print(symbol)
        if symbol != '{}':
          # for e-transitions ('e') if i is 0, else use alphabet symbols
          transitions[state]['e' if i == 0 else alphabet[i-1]] = set(map(int, symbol[1:-1].split(',')))
          
    
          
  #print(transitions)
    
def stage_one():
    global accepting
    
    accepting_set = set(accepting)  # Create a mutable copy of the global accepting states
    
    changes_made = True

    while changes_made:
      changes_made = False  # Assume no changes, to begin with
      for state_q in range(n_states):  # Iterate through all states
        if state_q in accepting_set:  # Skip if state_q is already an accepting state
          continue
        
        e_move = transitions[state_q]['e']  # Get e-transitions for state_q
       
        # Check if any state reachable via e-transitions from state_q is an accepting state
        if any(state_r in accepting_set for state_r in e_move): 
          accepting_set.add(state_q)  # Add state_q to accepting states
          changes_made = True  # Mark that a change has been made for the next iteration

    accepting = accepting_set  # Update the global accepting states
    return sorted(accepting)  # Return a sorted list of the updated accepting states
  
def stage_two():
  add_transition = transitions
  
  changes_made = True
  

  while changes_made:
    changes_made = False
    # Iterate over each state q in the automaton
    for q in range(n_states):
      print("step 1")
      for r in range(n_states):
        print("step 2")
        # Now check transitions from each r via each symbol a in the alphabet
        for a in alphabet:
          print("step 3")
          reachable_from_r = add_transition.get((r), set())
          print(reachable_from_r)
          for s in reachable_from_r:
            print("step 4")
            # If s is not already in delta(q, a), add it
            if s not in add_transition.get((q, a), set()):
              print("step 5")
              # Update delta(q, a) with s
              if (q, a) in add_transition:
                print("step 5.1")
                add_transition[(q, a)].add(s)
              else:
                print("step 5.2")
                add_transition[(q, a)] = {s}
              changes_made = True  # Mark that a change was made
        

    
  
  #print(add_transition)
  
  return transitions
  
def stage_three():
  transitions = stage_two();
  for states in range(n_states):
    transitions[states]['e'] = "{}"
    
  return transitions
    
def print_NFA(transitions):
  # iterate through each state and its transitions
  for state, transition_dict in transitions.items():
    row = []
    # add e-transitions to the row
    e_trans = transition_dict['e']
    row.append(e_trans)
    # add transitions for each symbol in the alphabet
    for symbol in alphabet:
      rest = ",".join(map(str, sorted(transition_dict.get(symbol, set()))))  # Handle missing symbols
      row.append("{" + rest + "}")

    # Print the row
    print(" ".join(row))
        
def print_ANS():
  accepted = stage_one()  # update accepting states
  print(f"Number of states: {n_states}")
  print(f"Alphabet size: {alphabet_size}")
  print(f"Accepting states: {' '.join(map(str, accepted))}")
  transitions = stage_three() # update transitions
  print_NFA(transitions)
    


def main():
  fileName = None
    
  if len(sys.argv) > 1:
    fileName = sys.argv[1]
    read(fileName)
    print_ANS()

if __name__ == "__main__":
  main()