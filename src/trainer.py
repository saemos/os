import os
from src.transformer import MicroTransformer

def load_data(filepath):
    if not os.path.exists(filepath):
        # Fallback if file doesn't exist yet
        return "def python_code(): pass\nint c_code() { return 0; }"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def main():
    print("Initializing From-Scratch AI Engine...")
    
    # 1. Load data
    text = load_data("data/book_data.txt")
    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    
    print(f"Loaded dataset. Vocab Size: {vocab_size} unique characters.")

    # 2. Initialize Model
    model = MicroTransformer(vocab_size=vocab_size, n_embd=16, block_size=8)
    print(f"Model initialized with {model.get_parameter_count()} trainable parameters.")
    print("Architecture built successfully from scratch using pure Python!")

if __name__ == "__main__":
    main()
