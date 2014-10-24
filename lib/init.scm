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

(defmacro (defrec (name . args) . body)
   '(define* ,name
       ((lambda (F) (F F))
        (lambda (F)
           (lambda ,args
              ((lambda (,name) . ,body) (F F)))))))

(define (first l) (car l))
(define (second l) (car (cdr l)))
(define (third l) (car (car (cdr l))))

(defrec (map f l)
   (if (isnil l) nil
                 (cons (f (car l)) (map f (cdr l)))))

(defmacro (let bindings . body)
   '((lambda ,(map first bindings) . body) . ,(map second bindings)))
   
