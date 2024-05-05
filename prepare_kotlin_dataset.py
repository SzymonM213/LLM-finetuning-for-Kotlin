import os
import shutil
import numpy as np

KOTLIN_EXTENSIONS = [".kt", ".kts"]
SUBSTRINGS = ['fun', 'open class', 'inner class']
PROJECT_DIR = "kotlin"
DATASET_DIR = "data/kotlin_dataset"
KOTLIN_DIR = "data/kotlin"

PROMPTS_FILE = "prompts.txt"
ANSWERS_FILE = "answers.txt"

TEST_SIZE = 100
SEED = 42
TRAINING_SIZE = 1024

def move_files_to_data_directory(project_dir=PROJECT_DIR, data_dir=KOTLIN_DIR, proper_extensions=KOTLIN_EXTENSIONS):
    for root, _, files in os.walk(project_dir):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in proper_extensions:
                os.makedirs(data_dir, exist_ok=True)
                
                src_path = os.path.join(root, file)
                dest_path = os.path.join(data_dir, file)
                shutil.copy(src_path, dest_path)

def is_proper_prompt(prompt, answer):
    return any(substring in prompt for substring in SUBSTRINGS) \
           and "*" not in prompt \
           and "//" not in prompt \
           and "}" not in prompt \
           and answer != "" \
           and answer != "\n" \
           and "//" not in answer \
           and "/*" not in answer \
           and "*/" not in answer

def extract_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        prompts_path = os.path.join(DATASET_DIR, PROMPTS_FILE)
        answers_path = os.path.join(DATASET_DIR, ANSWERS_FILE)
        with open(prompts_path, 'a') as prompts_file, open(answers_path, 'a') as answers_file:
            lines = file.readlines()
            for i in range(len(lines) - 1):
                if is_proper_prompt(lines[i], lines[i + 1]):
                    if not lines[i].endswith("\n"):
                        lines[i] += "\n"
                    if not lines[i + 1].endswith("\n"):
                        lines[i + 1] += "\n"
                    prompts_file.write(lines[i])
                    answers_file.write(lines[i + 1])

def walk_through_files(directory=KOTLIN_DIR):
    for root, _, files in os.walk(directory):    
        for file in files:
            file_path = os.path.join(root, file)
            extract_lines_from_file(file_path)

def split_dataset():
    with open(os.path.join(DATASET_DIR, PROMPTS_FILE), 'r') as prompts_file, open(os.path.join(DATASET_DIR, ANSWERS_FILE), 'r') as answers_file:
        prompts = prompts_file.readlines()
        answers = answers_file.readlines()
        prompts_len = len(prompts)
        answers_len = len(answers)
        assert prompts_len == answers_len

        indices = np.random.permutation(prompts_len)
        split_index = TEST_SIZE
        test_indices = indices[:split_index]
        with open(os.path.join(DATASET_DIR, "prompts_test.txt"), 'w') as prompts_test_file, open(os.path.join(DATASET_DIR, "answers_test.txt"), 'w') as answers_test_file:
            for i in test_indices:
                prompts_test_file.write(prompts[i])
                answers_test_file.write(answers[i])

def merge_files(directory=KOTLIN_DIR, output_file=os.path.join(DATASET_DIR, "kotlin_dataset.txt")):
    with open(output_file, 'w') as out:
        for file in os.listdir(directory):
            with open(os.path.join(directory, file), 'r') as f:
                out.write(f.read())
                out.write('\n')

    with open(output_file, 'r') as f:
        lines = f.readlines()[:TRAINING_SIZE]
        with open(os.path.join(DATASET_DIR, f"kotlin_{TRAINING_SIZE}.txt"), 'w') as out:
            out.writelines(lines)

if __name__ == "__main__":
    os.makedirs(DATASET_DIR, exist_ok=True)
    move_files_to_data_directory()
    np.random.seed(SEED)
    walk_through_files()
    split_dataset()
    merge_files()