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
all_members([2, 5, 8, 11], [A0, A1, A2, A3]),
or([and([A2 = 5,C1 = c3]),and([C2 = c3,A1 = 5])]),
member([C1_val, c1], All),
C1_val-A1=:=3,
and([or([member([11, c2], All),A2 = 11]), not(and([member([11, c2], All),A2 = 11]))]),
or([and([A0 = 8,C1 = c2]),and([A1 = 8,C0 = c2])]).