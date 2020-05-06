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
all_members([1964, 1968, 1972, 1976], [A0, A1, A2, A3]),
or([and([A1 = 1976,member([1964, c1], All)]),and([A1 = 1964,member([1976, c1], All)])]),
and([or([member([1964, c0], All),A1 = 1964]), not(and([member([1964, c0], All),A1 = 1964]))]),
A2-A0=:=8,
member([C2_val, c2], All),
member([C3_val, c3], All),
C2_val<C3_val,
and([or([A3 = 1968,C3 = c0]), not(and([A3 = 1968,C3 = c0]))]).
