import random
from torchvision import datasets
import face_recognition as r

# Load combined dataset (assuming both datasets are combined into one folder structure)
combined_dataset_path = '../arcface/combined_dataset'  # Path to the combined dataset
combined_dataset = datasets.ImageFolder(root=combined_dataset_path)

# Function to generate random face pairs
def generate_random_pairs(dataset, num_pairs, same_person_ratio=0.5):
    pairs = []
    labels = []

    # Determine how many pairs should be the same person
    num_same_person_pairs = int(num_pairs * same_person_ratio)
    num_different_person_pairs = num_pairs - num_same_person_pairs

    # Pick same person pairs
    for _ in range(num_same_person_pairs):
        class_idx = random.choice(range(len(dataset.classes)))  # Randomly choose a class
        class_indices = [i for i, (_, label) in enumerate(dataset.imgs) if label == class_idx]
        img1_idx, img2_idx = random.sample(class_indices, 2)  # Get two different images from the same class
        pairs.append((dataset.imgs[img1_idx][0], dataset.imgs[img2_idx][0]))  # Add image paths
        labels.append(1)  # Same person

    # Pick different person pairs
    for _ in range(num_different_person_pairs):
        img1_idx = random.randint(0, len(dataset.imgs) - 1)
        img2_idx = random.randint(0, len(dataset.imgs) - 1)
        while dataset.imgs[img1_idx][1] == dataset.imgs[img2_idx][1]:  # Ensure they are different
            img2_idx = random.randint(0, len(dataset.imgs) - 1)
        pairs.append((dataset.imgs[img1_idx][0], dataset.imgs[img2_idx][0]))  # Different persons
        labels.append(0)  # Different person

    return pairs, labels

# Generate pairs for evaluation
num_pairs = 10000
pairs, labels = generate_random_pairs(combined_dataset, num_pairs, same_person_ratio=0.5)
correct = 0
s_avg = 0.0
d_avg = 0.0

# Now you can insert your comparison function here to evaluate the pairs
# For example:
for (img1_path, img2_path), label in zip(pairs, labels):
    # print(f'Comparing: {img1_path} and {img2_path}')
    similarity = r.recognition(img1_path, img2_path)
    if label:
        c = 'same'
        s_avg += similarity
        if similarity >= 0.3:
            correct += 1
    else:
        c = 'diff'
        d_avg += similarity
        if similarity < 0.3:
            correct += 1
    print(f'{c} | sim = {similarity:5f}')
    
acc = correct / num_pairs
s_avg /= (num_pairs/2)
d_avg /= (num_pairs/2)

print(acc, s_avg, d_avg)