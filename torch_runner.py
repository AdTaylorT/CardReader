import torch
import torch.utils.data.dataset
import torchvision

x=torch.rand(5,3)
print(x)

print(torch.cuda.is_available())
print(torch.cuda.device_count())

images: list
torch.utils.data.DataLoader