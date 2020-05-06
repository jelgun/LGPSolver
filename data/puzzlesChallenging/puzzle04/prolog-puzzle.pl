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
all_members([1974, 1975, 1976, 1977], [A0, A1, A2, A3]),
or([and([member([1974, c2], All),A3 = 1976]),and([member([1976, c2], All),A3 = 1974])]),
member([C1_val, c1], All),
member([C0_val, c0], All),
C1_val-C0_val=:=1,
and([or([member([1974, c3], All),C0 = c3]), not(and([member([1974, c3], All),C0 = c3]))]),
member([C0_val, c0], All),
C0_val-A1=:=1.
