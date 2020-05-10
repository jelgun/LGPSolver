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
all_members([8500, 9000, 9500, 10000], [A0, A1, A2, A3]),
or([and([member([9000, c1], All),C2 = c0]),and([C2 = c1,member([9000, c0], All)])]),
member([C2_val, c2], All),
C2_val-A0=:=1000,
not(member([9000, c0], All)),
not(C1 = c0),
not(member([8500, c0], All)),
not(A1 = 9000),
not(A1 = 8500),
and([or([member([9500, c0], All),member([8500, c0], All)]), not(and([member([9500, c0], All),member([8500, c0], All)]))]).