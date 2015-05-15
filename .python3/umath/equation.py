# coding: utf-8

from . import isreal, nth_root

def _approx(z):
    return round(z.real, 12) + round(z.imag, 12) * 1j


class Equation(object):
    def __init__(self, *consts):
        cs = len(consts)

        if cs == 0:
            raise TypeError('This takes one argument at least (0 given)')

        if cs > 0: self.a = complex(consts[0])
        if cs > 1: self.b = complex(consts[1])
        if cs > 2: self.c = complex(consts[2])
        if cs > 3: self.d = complex(consts[3])
        if cs > 4: self.e = complex(consts[4])

        if cs > 5:
            raise ValueError('This can solve until 4th-degree equation.')

        if self.a == 0.0:
            raise ValueError('The first argument must be non-zero.')

        if cs == 2: self._solve_1st()
        elif cs == 3: self._solve_2nd()
        elif cs == 4: self._solve_3rd()
        elif cs == 5: self._solve_4th()

        self.dimension = cs

    def _solve_1st(self):
        """
            The linear function
                y(x) = a*x + b

            a       : The coefficient a (!=0)
            b       : The coefficient b
            x       : returns a tuple of the real solution of y(x) = 0.
            cx      : returns a tuple of the complex solution of y(x) = 0.
            y(x)    : returns a*x + b
        """
        self.y = lambda x: self.a * x + self.b
        self.dy = lambda x: self.a
        self.dy2 = lambda x: 0+0j

        x0 = - (self.b / self.a)
        self.cx = (x0, )
        self.x = tuple(z.real for z in self.cx if isreal(z))

    def _solve_2nd(self):
        """
            The quadratic function:
                y(x) = a*(x**2) + b*(x) + c

            a       : The coefficient a (!=0)
            b       : The coefficient b
            c       : The coefficient c
            x       : returns a tuple of the real solutions of y(x) = 0.
            cx      : returns a tuple of the complex solutions of y(x) = 0
            D       : returns the discriminant D = b*b - 4*a*c
            sqrtD   : returns math.sqrt(D), or cmath.sqrt(D)
            axis    : returns -b / 2*a
            extremum: returns c - (b**2 / 4*a)
            vertex  : returns the vertex tuple of (axis, extremum)
            y(x)    : returns a*(x**2) + b*(x) + c
        """
        a, b, c = self.a, self.b, self.c
        self.y = lambda x: a*(x**2) + b*x + c
        self.dy = lambda x: 2*a*x + b
        self.dy2 = lambda x: 2*a

        self.D = b**2 - 4*a*c
        self.axis = -b / (2*a)                 # 軸
        self.extremum = c - (b*b)/(4*a)        # 極小
        self.vertex = (self.axis, self.extremum)      # 頂点座標

        cx = [(-b+t)/(2*a) for t in nth_root(self.D, 2)]

        self.cx = tuple(_approx(i) for i in cx)
        self.x = tuple(z.real for z in self.cx if isreal(z))


    def _solve_3rd(self):
        """
            The cubic function:
                y(x) = a*(x**3) + b*(x**2) + c*(x) + d

            a       : The coefficient a (!=0)
            b       : The coefficient b
            c       : The coefficient c
            d       : The coefficient d
            x       : returns a tuple of the real solutions of y(x) = 0.
            cx      : returns a tuple of the complex solutions of y(x) = 0
            y(x)    : returns a*(x**3) + b*(x**2) + c*(x) + d
        """
        a, b, c, d = self.a, self.b, self.c, self.d
        self.y = lambda x: a*(x**3) + b*(x**2) + c*x + d
        self.dy = lambda x: 3*a*(x**2) + 2*b*x + c
        self.dy2 = lambda x: 6*a*x + 2*b

        # Cardano's formula
        # http://ja.wikipedia.org/wiki/三次方程式
        A, B, C = b/a, c/a, d/a

        p = (B - A*A/3) / 3.
        q = (C - A*B/3 + 2*(A/3)**3) / 2.

        ss = [(-q+t) for t in nth_root(q**2 + p**3, 2)]

        us = nth_root(ss[0], 3)
        vs = nth_root(ss[1], 3)

        def permt(n):
            for i in range(n):
                for j in range(n):
                    yield (i,j)

        ijk = [(i, j, abs(us[i]*vs[j]+p)) for i,j in permt(3)]
        ijk.sort(key=lambda x: x[2])
        cx = tuple([us[i] + vs[j] - A/3 for i,j,k in ijk[:3]])

        self.cx = tuple(_approx(i) for i in cx)
        self.x = tuple(z.real for z in self.cx if isreal(z))


    def _solve_4th(self):
        """
                y(x) = a*(x**4) + b*(x**3) + c*(x**2) + d*(x) + e

            a       : The coefficient a (!=0)
            b       : The coefficient b
            c       : The coefficient c
            d       : The coefficient d
            e       : The coefficient e
            x       : returns a tuple of the real solutions of y(x) = 0.
            cx      : returns a tuple of the complex solutions of y(x) = 0
            y(x)    : returns a*(x**4) + b*(x**3) + c*(x**2) + d*(x) + e
        """
        a, b, c, d, e = self.a, self.b, self.c, self.d, self.e
        self.y = lambda x: a*(x**4) + b*(x**3) + c*(x**2) + d*x + e
        self.dy = lambda x: 4*a*(x**3) + 3*b*(x**2) + c*x + d
        self.dy2 = lambda x: 12*a*(x**2) + 6*b*x + c

        # フェラーリ法
        # y^4 + py^2 +qy + r = 0
        A,B,C,D = b/a, c/a, d/a, e/a
        S = A/4
        p = B - 6*S**2
        q = C - 2*B*S + (2*S)**3
        r = D - C*S + B*S**2 - 3*S**4

        if q:
            # u^3 + 2pu^2 + (p^2 - 4r)u - q^2 = 0
            rcf = self.__class__(1, 2*p, (p**2 - 4*r), -q**2)
            u = rcf.x[0]

            us0,us1 = nth_root(u, 2)

            rqf0 = self.__class__(1, us0, (p+u)/2 - (q/u/2)*us0)
            rqf1 = self.__class__(1, us1, (p+u)/2 - (q/u/2)*us1)

            ys = []
            ys.extend(rqf0.cx)
            ys.extend(rqf1.cx)

            self.cx = [y-S for y in ys]
        else:
            # y^4 + py^2 + r = 0
            # Y^2 + pY + r = 0    * Y = y^2
            bqf = self.__class__(1, p, r)
            cx = []
            for x in bqf.cx:
                cx.extend(nth_root(x, 2))
            
            self.cx = cx

        self.x = tuple(z.real for z in self.cx if isreal(z))


def runge_kutta4(yp, tmin, tmax, y0, t0, dt):
    yi = [y0]
    ti = [t0]
    nmax = int((tmax - tmin)/dt + 1)

    for n in range(nmax):
        tn = ti[n]
        yn = yi[n]

        dy1 = dt * yp(tn,          yn)
        dy2 = dt * yp(tn+(dt/2.0), yn+(dy1/2.0))
        dy3 = dt * yp(tn+(dt/2.0), yn+(dy2/2.0))
        dy4 = dt * yp(tn+dt,       yn+dy3)

        yi.append(yn + (dy1 + 2.*dy2 + 2.*dy3 + dy4) / 6.0)
        ti.append(tn+dt)
    return [ti, yi]


if __name__ == "__main__":
    #import doctest
    #doctest.testmod()

    def y(t, y):
        return 3 * t**2 + -2*t**5

    tmin, tmax = 0., 10.
    dt = 0.1
    y0, t0 = 0., 0.

    t,y = runge_kutta4(y, tmin, tmax, y0, t0, dt)
    for i in range(0, len(t), 10):
        print ('y(%2.1f)\t= %4.6f\t error: %4.6g' % (t[i], y[i], abs(y[i]-((t[i]**2 + 4.)**2)/16.)) )

# vim: ft=python fenc=utf-8 ff=unix
