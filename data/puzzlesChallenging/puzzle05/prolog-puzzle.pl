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
all_members([625, 775, 825, 1075], [A0, A1, A2, A3]),
or([and([C0 = c1,A1 = 1075]),and([A0 = 1075,C1 = c1])]),
not(member([775, c0], All)),
not(C1 = c0),
not(A1 = 775),
member([C2_val, c2], All),
A3-C2_val=:=150,
and([or([C2 = c3,member([775, c3], All)]), not(and([C2 = c3,member([775, c3], All)]))]).
