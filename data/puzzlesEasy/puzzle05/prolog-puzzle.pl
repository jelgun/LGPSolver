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
all_members([4000000, 5000000, 6000000, 7000000], [A0, A1, A2, A3]),
not(member([5000000, c0], All)),
not(A1 = 5000000),
not(A2 = 5000000),
not(C1 = c0),
not(C2 = c0),
and([or([A2 = 4000000,C2 = c2]), not(and([A2 = 4000000,C2 = c2]))]),
member([7000000, c2], All),
C0 = c3,
member([C0_val, c0], All),
A0-C0_val=:=1000000.
