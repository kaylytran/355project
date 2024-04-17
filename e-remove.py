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
  #print(accepting_set)
  changes_made = True

  while changes_made:
    changes_made = False  # Assume no changes, to begin with
    
    for state_q in range(n_states):  # Iterate through all states
      if state_q not in accepting_set:  
        for state_r in range(n_states):
          if state_r in accepting_set:
            if state_r in transitions[state_q]['e']:
              accepting_set.add(state_q)  # add state_q to accepting states
              changes_made = True # Mark that a change has been made for the next iteration
              break
              
  accepting = accepting_set  # Update the global accepting states
  return sorted(accepting)  # Return a sorted list of the updated accepting states
  
def stage_two():
  add_transition = transitions
  
  changes_made = True

  while changes_made:
    changes_made = False # assume no changes, to begin with
    
    for a in alphabet:
      for state_q in range(n_states):
        for state_r in range(n_states):
          if state_r in add_transition[state_q]['e']:
            for state_s in range(n_states):
              if state_s in add_transition[state_r][a]:
                if state_s not in add_transition[state_q][a]:
                  new_s = add_transition[state_r][a]
                  add_transition[state_q][a].update(frozenset(new_s))
                  changes_made = True
  
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