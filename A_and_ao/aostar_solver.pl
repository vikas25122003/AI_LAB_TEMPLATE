% AO* Search Solver in Prolog
% Expects facts: branch(Node, [Child-Cost, ...]). 
% Each 'branch' fact represents an OR option. The list inside represents AND children.
% Expects facts: h(Node, H_Val).

solve_aostar(Start) :-
    ao_search(Start, Cost, SolutionTree),
    % Output format: RESULT:Cost:TreeString
    format('RESULT:~w:~w', [Cost, SolutionTree]).

% Base Case: Leaf Node (No branches)
ao_search(Node, Cost, Node) :-
    \+ branch(Node, _),
    h(Node, Cost).

% Recursive Step: Find Best Branch
ao_search(Node, BestCost, [Node | BestSubTrees]) :-
    findall(
        BranchCost-SubTrees,
        (
            branch(Node, Children),
            solve_branch(Children, BranchCost, SubTrees)
        ),
        Branches
    ),
    keysort(Branches, [BestCost-BestSubTrees | _]). % Pick min cost branch

% Solve AND Children (Sum of costs)
solve_branch([], 0, []).
solve_branch([Node-EdgeCost | Rest], TotalCost, [SubTree | RestTrees]) :-
    ao_search(Node, NodeCost, SubTree),
    solve_branch(Rest, RestCost, RestTrees),
    TotalCost is EdgeCost + NodeCost + RestCost.
