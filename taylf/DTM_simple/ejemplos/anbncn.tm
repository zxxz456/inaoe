# Maquina de Turing que acepta L = { a^n b^n c^n | n >= 1 }
#   (mismo numero de a's, b's y c's, en ese orden). NO es libre de contexto.
#
# Idea (extiende la de 0^n 1^n): en cada pasada marca la a mas a la izquierda
# como X, su b correspondiente como Y y su c como Z; luego regresa al inicio y
# repite. Cuando ya no quedan a's, verifica que el resto sea Y...Y Z...Z y nada
# mas. Si en cualquier paso falta una b o una c, no hay transicion -> RECHAZA

Q=q0,q1,q2,q3,q4,q5,q6
Sigma=a,b,c
Gamma=X,Y,Z,B
q_ini=q0
F=q6


q0 a -> q1 X R     
q0 Y -> q4 Y R    


q1 a -> q1 a R
q1 Y -> q1 Y R
q1 b -> q2 Y R


q2 b -> q2 b R
q2 Z -> q2 Z R
q2 c -> q3 Z L   


q3 a -> q3 a L
q3 b -> q3 b L
q3 Y -> q3 Y L
q3 Z -> q3 Z L
q3 X -> q0 X R    


q4 Y -> q4 Y R
q4 Z -> q5 Z R


q5 Z -> q5 Z R
q5 B -> q6 B R    
