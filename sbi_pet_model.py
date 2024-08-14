import torch
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
from pyro.optim import Adam

# Define the probabilistic model for the virtual pet
def pet_model(data):
    happiness_mean = pyro.sample("happiness_mean", dist.Normal(50, 10))
    health_mean = pyro.sample("health_mean", dist.Normal(50, 10))
    hunger_mean = pyro.sample("hunger_mean", dist.Normal(50, 10))
    
    with pyro.plate("data", len(data)):
        observed_happiness = pyro.sample("obs_happiness", dist.Normal(happiness_mean, 5), obs=data['happiness'])
        observed_health = pyro.sample("obs_health", dist.Normal(health_mean, 5), obs=data['health'])
        observed_hunger = pyro.sample("obs_hunger", dist.Normal(hunger_mean, 5), obs=data['hunger'])

# Define the guide (variational distribution)
def pet_guide(data):
    happiness_mean_loc = pyro.param("happiness_mean_loc", torch.tensor(50.0))
    happiness_mean_scale = pyro.param("happiness_mean_scale", torch.tensor(10.0))
    health_mean_loc = pyro.param("health_mean_loc", torch.tensor(50.0))
    health_mean_scale = pyro.param("health_mean_scale", torch.tensor(10.0))
    hunger_mean_loc = pyro.param("hunger_mean_loc", torch.tensor(50.0))
    hunger_mean_scale = pyro.param("hunger_mean_scale", torch.tensor(10.0))
    
    pyro.sample("happiness_mean", dist.Normal(happiness_mean_loc, happiness_mean_scale))
    pyro.sample("health_mean", dist.Normal(health_mean_loc, health_mean_scale))
    pyro.sample("hunger_mean", dist.Normal(hunger_mean_loc, hunger_mean_scale))

# Generate synthetic data
def generate_data():
    return {
        'happiness': np.random.normal(50, 10, 100),
        'health': np.random.normal(50, 10, 100),
        'hunger': np.random.normal(50, 10, 100)
    }

data = generate_data()
data_tensor = {key: torch.tensor(val, dtype=torch.float32) for key, val in data.items()}

# Run inference
optimizer = Adam({"lr": 0.01})
svi = SVI(pet_model, pet_guide, optimizer, loss=Trace_ELBO())

n_steps = 1000
for step in range(n_steps):
    loss = svi.step(data_tensor)
    if step % 100 == 0:
        print(f"Step {step} : Loss = {loss}")

# Extract inferred parameters
inferred_params = {
    "happiness_mean": pyro.param("happiness_mean_loc").item(),
    "health_mean": pyro.param("health_mean_loc").item(),
    "hunger_mean": pyro.param("hunger_mean_loc").item(),
}

print(f"Inferred parameters: {inferred_params}")
