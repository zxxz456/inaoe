# Maquina de Turing que acepta los PALINDROMOS sobre {a, b}
#     L = { w en {a,b}* | w == w^R }
# Incluye la cadena vacia y las de un solo simbolo (tambien son palindromos)
#
# Idea: borra el simbolo mas a la izquierda recordandolo en el estado, va al
# extremo derecho y comprueba que coincida; lo borra y regresa al inicio
# Repite hasta que no quede nada (o quede un solo simbolo). Si los extremos no
# coinciden, no hay transicion -> RECHAZA

Q=q0,q1,q2,q3,q4,q5,q6
Sigma=a,b
Gamma=B
q_ini=q0
F=q6


q0 a -> q1 B R   
q0 b -> q3 B R    
q0 B -> q6 B R   


q1 a -> q1 a R
q1 b -> q1 b R
q1 B -> q2 B L     


q2 a -> q5 B L    
q2 B -> q6 B R    



q3 a -> q3 a R
q3 b -> q3 b R
q3 B -> q4 B L


q4 b -> q5 B L     
q4 B -> q6 B R     



q5 a -> q5 a L
q5 b -> q5 b L
q5 B -> q0 B R  
