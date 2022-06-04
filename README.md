# N-Puzzle-Solver
This is a SMT solver for N-Puzzle. It can also find minimal solution for it.  

The solver uses [Z3-solver](https://github.com/Z3Prover/z3).

## Checker

Script [checker.py](https://github.com/DerekBum/N-Puzzle-Solver/blob/main/checker.py) will answer if the current field state SAT or not if we have only **k** moves. If it is, then it will give a correct sequence of moves.  

To run this script you need to create a ```.txt``` file with  
1) Field size.
2) Field state.
3) Number of moves.  

Then simply run ```./checker.py input.txt```. Answer will be in ```output.txt```.  

## How to find minimum number of moves?

Script [findMin.py](https://github.com/DerekBum/N-Puzzle-Solver/blob/main/findMin.py) will find minimum number of moves (and these steps too) to solve the puzzle (if puzzle is solvable).

To run this script you need to create a ```.txt``` file with  
1) Field size.
2) Field state.

You can find examples in [input examples](https://github.com/DerekBum/N-Puzzle-Solver/tree/main/inputExamples).  

Then simply run ```./findMin.py input.txt```. Answer will be in ```output.txt```.  

## Presentation

I am using [ComposeSlidesPresenter](https://plugins.jetbrains.com/plugin/19233-composeslidespresenter) to show presentation. Please see [project GitHub page](https://github.com/DerekBum/composeSlidesPresenter) for more information.  
