all_members([H], L) :- member(H, L).
all_members([H|T], L) :- member(H, L), all_members(T, L).

all_not_members([H], L) :- not(member(H, L)).
all_not_members([H|T], L) :- not(member(H, L)), all_not_members(T, L).

and([H]) :- H.
and([H|T]) :- H, and(T).

or([H]) :- H, !.
or([H|_]) :- H, !.
or([_|T]) :- or(T).

solve(B0,B1,B2,B3) :-
B0 = [A0, C0],
B1 = [A1, C1],
B2 = [A2, C2],
B3 = [A3, C3],

All = [B0,B1,B2,B3],

all_members([c0, c1, c2, c3], [C0, C1, C2, C3]),
all_members([2, 3, 4, 5], [A0, A1, A2, A3]),
A1 = 3,
and([or([A3 = 4,C3 = c3]), not(and([A3 = 4,C3 = c3]))]),
member([C2_val, c2], All),
A1-C2_val=:=1,
C2 = c3,
and([or([A1 = 4,C1 = c0]), not(and([A1 = 4,C1 = c0]))]).
