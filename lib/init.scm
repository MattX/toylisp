; more primitives

(define* list
   (lambda x x))

(define* defmacro
  (macro
    (lambda ((name . args) . body)
	'(define* ,name (macro (lambda ,args . ,body))))))

(defmacro (define name-args . body)
	(if (atom name-args) '(define* ,name-args . ,body)
	                     '(define* ,(car name-args) (lambda ,(cdr name-args) . ,body))))


(define (first l) (car l))
(define (second l) (car (cdr l)))
(define (third l) (car (car (cdr l))))
(defrec (nth n l)
   (if (= n 0) (car l) (nth (- n 1) (cdr l))))

(define (map f l)
   (if (isnil l) nil
                 (cons (f (car l)) (map f (cdr l)))))

(defmacro (let bindings . body)
   '((lambda ,(map first bindings) . body) . ,(map second bindings)))
   
