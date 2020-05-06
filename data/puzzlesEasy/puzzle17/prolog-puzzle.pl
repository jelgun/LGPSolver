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
all_members([1, 2, 3, 4], [A0, A1, A2, A3]),
and([or([C2 = c0,C2 = c3]), not(and([C2 = c0,C2 = c3]))]),
and([or([A1 = 2,member([2, c0], All)]), not(and([A1 = 2,member([2, c0], All)]))]),
not(A2 = 1),
not(member([1, c3], All)),
not(A3 = 1),
not(C2 = c3),
not(C3 = c3),
member([3, c3], All),
C0 = c1.
