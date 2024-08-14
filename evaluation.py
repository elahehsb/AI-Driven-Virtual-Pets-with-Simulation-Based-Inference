import matplotlib.pyplot as plt

# Simulate user interactions and analyze pet behavior
def simulate_interactions():
    actions = ['feed', 'play', 'rest']
    state_history = []
    
    for _ in range(100):
        action = np.random.choice(actions)
        response = requests.post('http://localhost:5000/interact', json={'action': action})
        state = response.json()
        state_history.append(state)
    
    return state_history

def plot_state_history(state_history):
    happiness = [state['happiness'] for state in state_history]
    health = [state['health'] for state in state_history]
    hunger = [state['hunger'] for state in state_history]
    
    plt.figure(figsize=(12, 6))
    plt.plot(happiness, label='Happiness')
    plt.plot(health, label='Health')
    plt.plot(hunger, label='Hunger')
    plt.xlabel('Interaction')
    plt.ylabel('State')
    plt.legend()
    plt.show()

state_history = simulate_interactions()
plot_state_history(state_history)
