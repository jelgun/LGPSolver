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
all_members([2008, 2009, 2010, 2011], [A0, A1, A2, A3]),
member([C0_val, c0], All),
member([C2_val, c2], All),
C2_val-C0_val=:=1,
and([or([member([2008, c0], All),C2 = c0]), not(and([member([2008, c0], All),C2 = c0]))]),
or([and([C0 = c1,member([2010, c2], All)]),and([C0 = c2,member([2010, c1], All)])]),
or([and([member([2009, c2], All),A1 = 2010]),and([A1 = 2009,member([2010, c2], All)])]).
