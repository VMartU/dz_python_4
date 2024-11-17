from kaggle_environments import make
import random

# Определение агентов
def rock(observation, configuration):
    return 0

def paper(observation, configuration):
    return 1

def scissors(observation, configuration):
    return 2

def copy_opponent(observation, configuration):
    if observation.step > 0:
        return observation.lastOpponentAction
    return random.randint(0, configuration.signs - 1)

def reactionary(observation, configuration):
    if observation.step > 0:
        return (observation.lastOpponentAction + 1) % configuration.signs
    return random.randint(0, configuration.signs - 1)

action_histogram = {}
def statistical(observation, configuration):
    global action_histogram
    if observation.step == 0:
        action_histogram = {}
    if observation.step > 0:
        action = observation.lastOpponentAction
        action_histogram[action] = action_histogram.get(action, 0) + 1
    if action_histogram:
        most_frequent_action = max(action_histogram, key=action_histogram.get)
        return (most_frequent_action + 1) % configuration.signs
    return random.randint(0, configuration.signs - 1)

def random_agent(observation, configuration):
    return random.randint(0, configuration.signs - 1)

last_action = None
def cyclical_agent(observation, configuration):
    global last_action
    if last_action is None:
        last_action = random.randint(0, configuration.signs - 1)
    else:
        last_action = (last_action + 1) % configuration.signs
    return last_action

def losing_agent(observation, configuration):
    if observation.step > 0:
        return (observation.lastOpponentAction + 2) % configuration.signs
    return random.randint(0, configuration.signs - 1)

def step_based_agent(observation, configuration):
    return observation.step % configuration.signs

def spock_agent(observation, configuration):
    if configuration.signs > 3:
        return 3  # Спок
    return random.randint(0, configuration.signs - 1)

def lizard_agent(observation, configuration):
    if configuration.signs > 4:
        return 4  # Ящерица
    return random.randint(0, configuration.signs - 1)

def avoid_last_opponent(observation, configuration):
    if observation.step > 0:
        return (observation.lastOpponentAction + random.randint(1, configuration.signs - 1)) % configuration.signs
    return random.randint(0, configuration.signs - 1)

last_own_action = None
def repeat_self_agent(observation, configuration):
    global last_own_action
    if last_own_action is None:
        last_own_action = random.randint(0, configuration.signs - 1)
    return last_own_action

def predictive_agent(observation, configuration):
    return random.randint(0, configuration.signs - 1)

def counter_predictive_agent(observation, configuration):
    predicted_action = random.randint(0, configuration.signs - 1)
    return (predicted_action + 1) % configuration.signs

# Создание окружения
env = make("rps", configuration={"episodeSteps": 200})

# Список агентов
agents = [
    rock, paper, scissors, copy_opponent, reactionary, statistical, random_agent,
    cyclical_agent, losing_agent, step_based_agent, spock_agent, lizard_agent,
    avoid_last_opponent, repeat_self_agent, predictive_agent, counter_predictive_agent
]

# Результаты матчей
results = {}

for i in range(len(agents)):
    for j in range(i + 1, len(agents)):
        agent_1 = agents[i]
        agent_2 = agents[j]
        env.reset()
        env.run([agent_1, agent_2])
        
        # Подсчет побед, поражений и ничьих
        agent_1_wins = 0
        agent_2_wins = 0
        ties = 0
        
        for step in env.steps:
            reward_1 = step[0]["reward"]
            reward_2 = step[1]["reward"]
            if reward_1 > reward_2:
                agent_1_wins += 1
            elif reward_1 < reward_2:
                agent_2_wins += 1
            else:
                ties += 1
        
        # Сохранение результатов
        results[f"{agent_1.__name__} vs {agent_2.__name__}"] = {
            agent_1.__name__: {"wins": agent_1_wins, "losses": agent_2_wins, "ties": ties},
            agent_2.__name__: {"wins": agent_2_wins, "losses": agent_1_wins, "ties": ties},
        }

# Вывод результатов
print("Результат:")
for match, result in results.items():
    agent_1, agent_2 = result.keys()
    print(f"{agent_1}: Победы: {result[agent_1]['wins']}, Поражения: {result[agent_1]['losses']}, Ничьи: {result[agent_1]['ties']}")
    print(f"{agent_2}: Победы: {result[agent_2]['wins']}, Поражения: {result[agent_2]['losses']}, Ничьи: {result[agent_2]['ties']}")
    print("-----")
