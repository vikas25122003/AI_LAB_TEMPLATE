% ============================================================
% GENERIC RECURSIVE PATHFINDER (DFS + BACKTRACKING)
% ============================================================

% Entry Point
find_all_paths(Start, End) :-
    format('~n--- SEARCHING PATHS: ~w -> ~w ---~n', [Start, End]),
    path(Start, End, [Start], Path, 0, Cost),
    format('FOUND: ~w | Cost: ~w~n', [Path, Cost]),
    fail. % Force backtracking
find_all_paths(_, _) :-
    format('--- DONE ---~n').

% Base Case
path(Goal, Goal, Visited, Path, Cost, Cost) :-
    reverse(Visited, Path).

% Recursive Step
path(Current, Goal, Visited, Path, CurrentCost, TotalCost) :-
    edge(Current, Next, StepCost),
    \+ member(Next, Visited),
    
    % --- THE CUSTOMIZABLE HOOK ---
    % If the user defined a rule 'is_valid_step(Node)', we check it.
    % If not defined, we assume it's valid (true).
    (current_predicate(is_valid_step/1) -> is_valid_step(Next) ; true),
    
    NewCost is CurrentCost + StepCost,
    path(Next, Goal, [Next|Visited], Path, NewCost, TotalCost).
