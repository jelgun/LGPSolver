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
all_members([14, 32, 50, 68], [A0, A1, A2, A3]),
not(A1 = 14),
not(A0 = 14),
not(member([14, c0], All)),
not(C1 = c0),
not(C0 = c0),
or([and([member([32, c0], All),C3 = c3]),and([member([32, c3], All),C3 = c0])]),
member([C2_val, c2], All),
A1-C2_val=:=36.
