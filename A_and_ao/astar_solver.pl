% A* Search Solver in Prolog
% Expects facts: edge(From, To, Cost), h(Node, H_Val).

solve_astar(Start, Goal) :-
    h(Start, H),
    % Queue format: [F_Score-G_Score-CurrentNode-PathSoFar]
    astar_step([H-0-Start-[]], Goal, Path, Cost),
    % Output format for Python to parse: RESULT:['a','b']:10
    format('RESULT:~w:~w', [Path, Cost]).

% Base Case: Reached Goal
astar_step([_-G-Goal-PathRev|_], Goal, Path, G) :-
    reverse([Goal|PathRev], Path).

% Recursive Step
astar_step([_-G-Current-PathRev|RestQueue], Goal, FinalPath, FinalCost) :-
    findall(
        NewF-NewG-Next-[Current|PathRev],
        (
            edge(Current, Next, StepCost),
            \+ member(Next, PathRev), % Simple cycle prevention
            NewG is G + StepCost,
            h(Next, H),
            NewF is NewG + H
        ),
        Children
    ),
    append(RestQueue, Children, NewQueue),
    keysort(NewQueue, SortedQueue), % Sort by F-Score (Key)
    astar_step(SortedQueue, Goal, FinalPath, FinalCost).
