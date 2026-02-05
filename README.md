# Chess Engine in Python 

## Summary
- Chess engine developed entirely in Python, using a hybrid architecture (Layered + Hexagonal).
- Bitboard-based representation for fast move generation and board evaluation.
- AI player implemented using alpha-beta pruning and transposition tables.
- Core classes designed following object-oriented programming principles and Single Responsibility Principle (SRP).

## Technologies
- Python 3.12
- Git

## Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/G-rm4n/Chess.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Chess
    ```
3. Run the project:
    ```bash
    python main.py
    ```


## Project Structure
```
    ├── Adapters
    │   ├── Bitboard.py
    │   ├── Translator.py
    │   └── __init__.py
    ├── Bot_Engine
    │   ├── MoveGenerator
    │   │   ├── MoveGenerator.py
    │   │   ├── __init__.py
    │   │   └── rayGenerator.py
    │   ├── Bot.py
    │   ├── Evaluate.py
    │   ├── MoveExecutor.py
    │   ├── TranspositionTable.py
    │   ├── ZoobristHash.py
    │   ├── __init__.py
    │   ├── constants.py
    │   └── legalCheck.py
    ├── Core
    │   ├── Board.py
    │   ├── GameMaster.py
    │   ├── Movement.py
    │   ├── Piece.py
    │   ├── Promotion.py
    │   └── __init__.py
    ├── Handlers
    │   ├── InputHandler.py
    │   └── __init__.py
    ├── Tests
    │   ├── TestBitboardGenerator.py
    │   ├── TestTranslator.py
    │   ├── __init__.py
    │   └── test_jaque.py
    ├── UI
    │   ├── Display.py
    │   └── __init__.py
    ├── Utils
    │   ├── GenerateIndividualBitboard.py
    │   └── __init__.py
    ├── .gitignore
    ├── README.md
    ├── States.py
    └── main.py
```

## Project Status
- In progress