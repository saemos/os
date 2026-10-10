scratch-ai-engine/
│


├── .github/
│   └── workflows/
│       └── test_engine.yml     # Automated CI pipeline to test code on push



│
├── data/
│   └── book_data.txt           # Your C, C++, and Python textbook notes/snippets
│




├── src/
│   ├── __init__.py
│   ├── engine.py               # Custom Autograd Engine (Value class & math)
│   ├── transformer.py          # Micro-Transformer & Attention layers from scratch
│   └── trainer.py              # Training loop & optimization logic




│
├── .gitignore                  # Ignores compiled python files, checkpoints, etc.
├── README.md                   # Project documentation & architectural notes
└── requirements.txt            # (Optional/Minimal) Standard lib only, or basic tools
