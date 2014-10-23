; more primitives

(set! >= (lambda (x y) (or (> x y) (= x y))))

(set! < (lambda (x y) (not (>= x y))))

(set! <= (lambda (x y) (not (> x y))))

