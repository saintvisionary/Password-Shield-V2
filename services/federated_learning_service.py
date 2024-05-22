import torch
from torch import nn, optim
from torch.utils.data import DataLoader
import numpy as np
from .models import User

class FederatedModel(nn.Module):
    def __init__(self):
        super(FederatedModel, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_federated_model(data, model, epochs=5, lr=0.001):
    """Train a federated model with the provided data."""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr)
    for epoch in range(epochs):
        for inputs, labels in data:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    return model

def aggregate_models(global_model, client_models):
    """Aggregate client models into a global model."""
    global_dict = global_model.state_dict()
    for k in global_dict.keys():
        global_dict[k] = torch.stack([client_models[i].state_dict()[k].float() for i in range(len(client_models))], 0).mean(0)
    global_model.load_state_dict(global_dict)
    return global_model

def distribute_global_model(global_model, users):
    """Distribute the global model to all users."""
    global_dict = global_model.state_dict()
    for user in users:
        user.model.load_state_dict(global_dict)
    return users
