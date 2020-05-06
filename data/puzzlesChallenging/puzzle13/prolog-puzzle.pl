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
all_members([5, 8, 11, 14], [A0, A1, A2, A3]),
or([and([A3 = 5,C2 = c1]),and([C3 = c1,A2 = 5])]),
and([or([member([8, c3], All),A1 = 8]), not(and([member([8, c3], All),A1 = 8]))]),
member([14, c0], All),
and([or([C1 = c2,A1 = 11]), not(and([C1 = c2,A1 = 11]))]),
member([C1_val, c1], All),
C1_val>A3.
