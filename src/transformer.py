import random
from src.engine import Value

class MicroTransformer:
    def __init__(self, vocab_size, n_embd=16, block_size=8):
        self.vocab_size = vocab_size
        self.n_embd = n_embd
        self.block_size = block_size

        # Initialize weights randomly with small Gaussian distribution
        def init_matrix(rows, cols):
            return [[Value(random.gauss(0, 0.08)) for _ in range(cols)] for _ in range(rows)]

        self.wte = init_matrix(vocab_size, n_embd)  # Token Embeddings
        self.wpe = init_matrix(block_size, n_embd)  # Position Embeddings

    def get_parameter_count(self):
        total = (self.vocab_size * self.n_embd) + (self.block_size * self.n_embd)
        return total
