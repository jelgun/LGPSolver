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
A1-A3=:=1,
or([and([C2 = c3,member([1, c1], All)]),and([C2 = c1,member([1, c3], All)])]),
member([C2_val, c2], All),
member([C3_val, c3], All),
C2_val-C3_val=:=2,
and([or([A3 = 2,member([2, c0], All)]), not(and([A3 = 2,member([2, c0], All)]))]).
