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
all_members([540, 600, 660, 1440], [A0, A1, A2, A3]),
member([C0_val, c0], All),
C0_val>A1,
or([and([A1 = 600,C2 = c1]),and([A2 = 600,C1 = c1])]),
and([or([member([660, c3], All),A0 = 660]), not(and([member([660, c3], All),A0 = 660]))]),
member([C3_val, c3], All),
A1-C3_val=:=60.
