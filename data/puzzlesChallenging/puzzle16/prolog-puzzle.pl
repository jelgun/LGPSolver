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
all_members([1962, 1969, 1976, 1983], [A0, A1, A2, A3]),
or([and([C3 = c2,A1 = 1962]),and([C1 = c2,A3 = 1962])]),
A2-A3=:=14,
member([C1_val, c1], All),
member([C3_val, c3], All),
C1_val-C3_val=:=7,
and([or([member([1969, c3], All),A0 = 1969]), not(and([member([1969, c3], All),A0 = 1969]))]).
