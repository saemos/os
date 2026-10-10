import math
import random

class Value:
    """Stores a scalar value and its gradient for backpropagation."""
    def __init__(self, data, children=(), local_grads=()):
        self.data = data
        self.grad = 0.0
        self._children = children
        self._local_grads = local_grads

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), (1.0, 1.0))
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), (other.data, self.data))
        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data ** other, (self,), (other * (self.data ** (other - 1)),))
        return out

    def exp(self):
        out_val = math.exp(self.data)
        out = Value(out_val, (self,), (out_val,))
        return out

    def log(self):
        out = Value(math.log(self.data), (self,), (1.0 / self.data,))
        return out

    def relu(self):
        out = Value(self.data if self.data > 0 else 0.0, (self,), (1.0 if self.data > 0 else 0.0,))
        return out

    def backward(self):
        # Topological sort of all nodes in the computational graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child, _ in zip(v._children, v._local_grads):
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1.0
        for v in reversed(topo):
            for child, local_grad in zip(v._children, v._local_grads):
                child.grad += v.grad * local_grad

    def __radd__(self, other): return self + other
    def __sub__(self, other): return self + (other * -1)
    def __rsub__(self, other): return (self * -1) + other
    def __rmul__(self, other): return self * other
    def __truediv__(self, other): return self * (other ** -1)
    def __rtruediv__(self, other): return other * (self ** -1)
    def __neg__(self): return self * -1
    
    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"
