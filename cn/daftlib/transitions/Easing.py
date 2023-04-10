
# TERMS OF USE - EASING EQUATIONS
# ---------------------------------------------------------------------------------
# Open source under the BSD License.
#
# Copyright © 2001 Robert Penner All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer. Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and
# the following disclaimer in the documentation and/or other materials provided
# with the distribution. Neither the name of the author nor the names of
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ---------------------------------------------------------------------------------

import math

class Easing:

    PI = 3.141592653589793
    PI_M2 = PI * 2
    PI_D2 = PI / 2

    def linearEaseNone(t, b, c, d):
        return c * t / d + b

    def sineEaseIn(t, b, c, d):
        return -c * math.cos(t / d * Easing.PI_D2) + c + b

    def sineEaseOut(t, b, c, d):
        return c * math.sin(t / d * Easing.PI_D2) + b

    def sineEaseInOut(t, b, c, d):
        return -c / 2 * (math.cos(Easing.PI * t / d) - 1) + b

    def quintEaseIn(t, b, c, d):
        t /= d
        return c * t * t * t * t * t + b

    def quintEaseOut(t, b, c, d):
        t = t / d - 1
        return c * (t * t * t * t * t + 1) + b

    def quintEaseInOut(t, b, c, d):
        t /= d / 2
        if t < 1:
            return c / 2 * t * t * t * t * t + b
        t -= 2
        return c / 2 * (t * t * t * t + 2) + b

    def quartEaseIn(t, b, c, d):
        t /= d
        return c * t * t * t * t + b

    def quartEaseOut(t, b, c, d):
        t = t / d - 1
        return -c * (t * t * t * t - 1) + b

    def quartEaseInOut(t, b, c, d):
        t /= d / 2
        if t < 1:
            return c / 2 * t * t * t * t + b
        t -= 2
        return -c / 2 * (t * t * t * t - 2) + b

    def quadEaseIn(t, b, c, d):
        t /= d
        return c * t * t + b

    def quadEaseOut(t, b, c, d):
        t /= d
        return -c * t * (t - 2) + b

    def quadEaseInOut(t, b, c, d):
        t /= d / 2
        if t < 1:
            return c / 2 * t * t + b
        t -= 1
        return -c / 2 * (t * (t - 2) - 1) + b

    def expoEaseIn(t, b, c, d):
        if t == 0:
            return b
        return c * pow(2, 10 * (t / d - 1)) + b

    def expoEaseOut(t, b, c, d):
        if t == d:
            return b + c
        return c * (-pow(2, -10 * t / d) + 1) + b

    def expoEaseInOut(t, b, c, d):
        if t == 0:
            return b
        if t == d:
            return b + c
        t /= d / 2
        if t < 1:
            return c / 2 * pow(2, 10 * (t - 1)) + b
        t -= 1
        return c / 2 * (-pow(2, -10 * t) + 2) + b

    def elasticEaseIn(t, b, c, d, a=None, p=None):
        if t == 0:
            return b
        if (t / d) == 1:
            return b + c
        if not p:
            p = d * 0.3
        if not a or a < abs(c):
            a = c
            s = p / 4
        else:
            s = p / Easing.PI_M2 * math.asin(c / a)
        return -(a * math.pow(2, 10 * (t / d - 1)) * math.sin((t * d - s) * Easing.PI_M2 / p)) + b

    def elasticEaseOut(t, b, c, d, a=None, p=None):
        if t == 0:
            return b
        if (t / d) == 1:
            return b + c
        if not p:
            p = d * 0.3
        if not a or a < abs(c):
            a = c
            s = p / 4
        else:
            s = p / Easing.PI_M2 * math.asin(c / a)
        return (a * math.pow(2, -10 * t / d) * math.sin((t * d - s) * Easing.PI_M2 / p) + c + b)

    def elasticEaseInOut(t, b, c, d, a=None, p=None):
        if t == 0:
            return b
        if (t / (d / 2)) == 2:
            return b + c
        if not p:
            p = d * (0.3 * 1.5)
        if not a or a < abs(c):
            a = c
            s = p / 4
        else:
            s = p / Easing.PI_M2 * math.asin(c / a)
        if t < 1:
            return -0.5 * (a * math.pow(2, 10 * (t / d - 1)) * math.sin((t * d - s) * Easing.PI_M2 / p)) + b
        return a * math.pow(2, -10 * (t / d - 1)) * math.sin((t * d - s) * Easing.PI_M2 / p) * 0.5 + c + b

    def circularEaseIn(t, b, c, d):
        return -c * (math.sqrt(1 - (t / d) * (t / d)) - 1) + b

    def circularEaseOut(t, b, c, d):
        t = t / d - 1
        return c * math.sqrt(1 - t * t) + b

    def circularEaseInOut(t, b, c, d):
        if (t / (d / 2)) < 1:
            return -c / 2 * (math.sqrt(1 - (t / d) * (t / d)) - 1) + b
        t -= 2
        return c / 2 * (math.sqrt(1 - t * t) + 1) + b

    def backEaseIn(t, b, c, d, s=1.70158):
        t /= d
        return c * t * t * ((s + 1) * t - s) + b

    def backEaseOut(t, b, c, d, s=1.70158):
        t = t / d - 1
        return c * (t * t * ((s + 1) * t + s) + 1) + b

    def backEaseInOut(t, b, c, d, s=1.70158):
        s *= 1.525
        t /= d / 2
        if t < 1:
            return c / 2 * (t * t * ((s + 1) * t - s)) + b
        t -= 2
        return c / 2 * (t * t * ((s + 1) * t + s) + 2) + b

    def bounceEaseIn(t, b, c, d):
        return c - Easing.bounceEaseOut(d - t, 0, c, d) + b

    def bounceEaseOut(t, b, c, d):
        if t < d / 2.75:
            return c * (7.5625 * t * t) + b
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return c * (7.5625 * t * t + 0.75) + b
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return c * (7.5625 * t * t + 0.9375) + b
        else:
            t -= 2.625 / 2.75
            return c * (7.5625 * t * t + 0.984375) + b

    def bounceEaseInOut(t, b, c, d):
        if t < d / 2:
            return Easing.bounceEaseIn(t * 2, 0, c, d) * 0.5 + b
        return Easing.bounceEaseOut(t * 2 - d, 0, c, d) * 0.5 + c * 0.5 + b

    def cubicEaseIn(t, b, c, d):
        t /= d
        return c * t * t * t + b

    def cubicEaseOut(t, b, c, d):
        t = t / d - 1
        return c * (t * t * t + 1) + b

    def cubicEaseInOut(t, b, c, d):
        t /= d / 2
        if t < 1:
            return c / 2 * t * t * t + b
        t -= 2
        return c / 2 * (t * t * t + 2) + b