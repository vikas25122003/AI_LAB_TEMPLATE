% ==========================================
% PROLOG KNOWLEDGE BASE TEMPLATE
% ==========================================

% 1. DYNAMIC PREDICATES
% ------------------------------------------
% Allows adding/removing facts at runtime (e.g., from Python)
:- dynamic friend/2.
:- dynamic task/2.

% 2. FACTS
% ------------------------------------------
% Basic assertions about the world
human(socrates).
human(plato).
human(aristotle).

parent(john, mary).
parent(john, tom).
parent(mary, ann).
parent(mary, bob).

male(john).
male(tom).
male(bob).
female(mary).
female(ann).

married(john).
married(mary).

% Initial dynamic facts
friend(alex, sam).
friend(sam, jordan).

% 3. RULES & QUANTIFIERS
% ------------------------------------------

% Universal Quantifier Example: "All humans are mortal"
% For all X, if X is human, then X is mortal.
mortal(X) :- human(X).

% Existential Quantifier Example: "X is a parent"
% X is a parent if there EXISTS some Y such that parent(X, Y).
is_parent(X) :- parent(X, _).

% 4. NEGATION (\+)
% ------------------------------------------
% "X is a bachelor if X is male AND X is NOT married"
bachelor(X) :- male(X), \+ married(X).

% 5. RECURSION
% ------------------------------------------
% Base case: X is ancestor of Y if X is parent of Y
ancestor(X, Y) :- parent(X, Y).
% Recursive step: X is ancestor of Y if X is parent of Z AND Z is ancestor of Y
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% 6. ARITHMETIC
% ------------------------------------------
% Calculate area of a circle: Area is Pi * R^2
circle_area(Radius, Area) :-
    Area is 3.14159 * Radius * Radius.

% Calculate factorial
factorial(0, 1).
factorial(N, Result) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, SubResult),
    Result is N * SubResult.

% 7. LIST OPERATIONS
% ------------------------------------------
% Check if element is in list (built-in member/2, but here's custom implementation)
contains(X, [X|_]).
contains(X, [_|Tail]) :- contains(X, Tail).

% Sum of a list
sum_list([], 0).
sum_list([Head|Tail], Sum) :-
    sum_list(Tail, TailSum),
    Sum is Head + TailSum.

% 8. CUT OPERATOR (!)
% ------------------------------------------
% The cut prevents backtracking. 
% Example: Max of two numbers. Once we find X >= Y, we stop looking for other rules.
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).

% 9. BACKTRACKING DEMO
% ------------------------------------------
% Finds all children of a person and prints them.
% Uses 'fail' to force backtracking to find all solutions.
print_children(Parent) :-
    parent(Parent, Child),
    write(Child), nl,
    fail.
print_children(_). % Always succeed at the end

% 10. DYNAMIC MANIPULATION
% ------------------------------------------
add_friend(X, Y) :-
    assertz(friend(X, Y)).

remove_friend(X, Y) :-
    retract(friend(X, Y)).
