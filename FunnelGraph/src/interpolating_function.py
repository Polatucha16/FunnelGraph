
# def inter_poly(x, parmaters=[0,0,1,1]):
#     ''' In wolfram mathematica use:
#         InterpolatingPolynomial[{{{x0}, y0, 0}, {{x1}, y1, 0}}, x] 
#     Returns value of polynomial in x with properties:
#         inter_poly(x0) = y0, inter_poly(x1) = y1 
#     and
#         inter_poly'(x0) = 0, inter_poly'(x1) = 0
#     '''
#     x0, y0, x1, y1 = parmaters
#     return y0+((x-x0)**2)*(-((2*(x-x1)*(-y0+y1))/(-x0+x1)**3)
#                          +(-y0+y1)/(-x0+x1)**2)

def inter_poly(x, parmaters=[0,0,1,1]):
    """ For i=0,1 and parmaters = [x0,y0,x1,y1] output has: 
            f(xi)=yi, f'(x0)=0 and f''(x0)=0.
    """
    x0, y0, x1, y1 = parmaters
    return y0 + ((x-x0)**3)*( (-y0+y1)/(-x0+x1)**3 +
        (x-x1)*(	
            (6*(x-x1)*(-y0+y1))/(-x0+x1)**5-
            (3*(-y0+y1))/(-x0+x1)**4
        	)
        )