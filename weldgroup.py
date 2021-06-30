# NOTE: IN THIS CLASS, SECTION PROPERTIES ARE ALWAYS INPUTTED AND PROCESSED
# IN THE FOLLOWING ORDER: MOMENT-X, MOMENT-Y, SHEAR-X, SHEAR-Y, AXIAL, TORSION

# NOTE: IN THIS CLASS, LENGTH IS ALWAYS EXPRESSED IN INCHES.
# ANY ADJUSTMENTS TO FT ARE MADE OUTSIDE OF THE CLASS.

# flare_bevel_strengths = {1: 0.803,
#                          2: 1.605,
#                          3: 2.408,
#                          4: 3.211,
#                          5: 4.013,
#                          6: 4.816,
#                          7: 5.618,
#                          8: 6.421,
#                          9: 7.224,
#                          10: 8.026,
#                          }


class WeldGroup:
    # class constructor
    def __init__(self, t: int = 3, group: str = '=', b: float = 0, d: float = 0, isFlareBevel: bool = False, t_HSS: int = 4):
        self.t = t
        self.group = group
        self.b = b
        self.d = d
        self.isFlareBevel = isFlareBevel
        self.t_HSS = t_HSS

        # if flare bevel selected, calculate effective throat of flare bevel from t_HSS
        if isFlareBevel:
            # print("\n\n CALCULATING A FLARE BEVEL WELD\n\n")
            self.R = 0.93 * 2 * t_HSS
            self.t = 0.31 * self.R

        self.weld_strength = 1.392 * self.t

        self.phiMnx, self.phiMny, self.phiVnx, self.phiVny, self.phiAn, self.phiTn = self.calculate_properties(
            group, b, d, self.weld_strength)

    def calculate_properties(self, group: str = "=", b: float = 0, d: float = 0, weld_strength: float = 0) -> None:
        """
        Calculate the 'section' properties of the inputted weld group based
        on its dimensions and weld strength. Assign the section properties
        to the global variables.

        :param group: selected weld group
        :param b: width of group in x-direction (horizontal)
        :param d: height of group in y-direction (vertical)
        """

        # round small group dimensions to zero in case of typos
        if (b < 1.0) and (d < 1.0):  # checked
            length = 0
            Sx = 0
            Sy = 0
            J = 0
            PM = 0
            c = 0

        # calculate different properties based on weld group
        elif group == '|':                           # all checked
            length = d
            Sx = (d**2) / 6
            Sy = 0
            J = 0
            PM = 0
            c = 0

        elif group == '-':                           # all checked
            length = b
            Sx = (b**2) / 6
            Sy = 0
            J = 0
            PM = 0
            c = 0

        elif group == '||':                          # all checked
            length = 2 * d
            Sx = (d**2) / 3
            Sy = b * d
            J = d/6 * (3*b**2 + d**2)
            c = (b**2 + d**2)**0.5 / 2
            PM = J / c

        elif group == '=':                           # all checked
            length = 2 * b
            Sx = b * d
            Sy = (b**2) / 3
            J = b/6 * (b**2 + 3*d**2)
            c = (b**2 + d**2) ** 0.5 / 2
            PM = J / c

        elif group == '▯':                           # all checked
            length = 2*b + 2*d
            Sx = d/3 * (3*b + d)
            Sy = b/3 * (3*d + b)
            J = (b+d)**3 / 6
            c = (b**2 + d**2)**0.5 / 2
            PM = J / c

        elif group == '⨅':                           # all checked - question
            length = b + 2*d

            Sxt = d/3 * (2*b + d)
            Sxb = (d**2 * (2*b + d)) / (3 * (b+d))
            Sx = (Sxt + Sxb) / 2

            Sy = b/6 * (b + 6*d)
            J = d**3 / 3 * ((2*b + d)/(b + 2*d)) + b**2 / 12 * (b+6 * d)
            Nx = d**2 / (b + 2*d)
            c = (Nx**2 + (b/2)**2)**0.5
            PM = J / c

        elif group == '╥':                           # all checked - question
            length = b + 2*d

            Sxt = d/3 * (2*b + d)
            Sxb = (d**2 * (2*b + d)) / (3 * (b+d))
            Sx = (Sxt + Sxb) / 2

            Sy = b**2 / 6
            J = d**3 / 3 * ((2*b + d)/(b + 2*d)) + b**3 / 12
            Ct = d**2 / (b + 2*d)
            c = (Ct**2 + (b/2)**2)**0.5
            PM = J / c

        elif group == '╦':                           # all checked - question
            length = 2 * (b+d)

            Sxt = d/3 * (4*b + d)
            Sxb = (4*b * d**2 + d**3) / (6*b + 3*d)
            Sx = (Sxt + Sxb) / 2

            Sy = b / 3
            J = d**3 / 6 * ((4*b + d)/(b+d)) + b**3 / 6
            Ct = d**2 / (2 * (b+d))
            c = (Ct**2 + (b/2)**2)**0.5
            PM = J / c

        elif group == "⌶":                           # all checked
            length = 2 * (2*b + d)
            Sx = d/3 * (6*b + d)
            Sy = 2/3 * b**2
            J = d**2 / 6 * (6*b + d) + b**3 / 3
            c = (b**2 + d**2)**0.5 / 2
            PM = J / c

        else:
            length = 0
            Sx = 0
            Sy = 0
            J = 0
            PM = 0
            c = 0

        # assign properties
        phiMnx = weld_strength * Sx
        phiMny = weld_strength * Sy
        phiVnx = weld_strength * length
        phiVny = weld_strength * length
        phiAn = weld_strength * length
        phiTn = weld_strength * PM

        return phiMnx, phiMny, phiVnx, phiVny, phiAn, phiTn,

    def properties(self):
        # updates section properties and returns them. Useful in case of changes to attributes
        self.phiMnx, self.phiMny, self.phiVnx, self.phiVny, self.phiAn, self.phiTn = self.calculate_properties(
            self.group, self.b, self.d, self.weld_strength)
        return self.phiMnx, self.phiMny, self.phiVnx, self.phiVny, self.phiAn, self.phiTn

    def check(self, Mux: float = 0, Muy: float = 0, Vux: float = 0, Vuy: float = 0, Au: float = 0, Tu: float = 0):
        phiMnx, phiMny, phiVnx, phiVny, phiAn, phiTn = self.properties()
        works = True

        # Mnx
        if (phiMnx == 0) and (Mux != 0):  # force inputted but zero for the section property
            works = False
        else:
            try:
                util_phiMnx = Mux / phiMnx * 100  # individual utilization
            except ZeroDivisionError:  # in case we get a 0/0
                util_phiMnx = 0
                # delete for deployment
                print("phiMnx is 0 and force provided is 0")

        # Mny
        if (phiMny == 0) and (Muy != 0):  # force inputted but zero for the section property
            works = False
        else:
            try:
                util_phiMny = Muy / phiMny * 100  # individual utilization
            except ZeroDivisionError:  # in case we get a 0/0
                util_phiMny = 0
                # delete for deployment
                print("phiMny is 0 and force provided is 0")

        # Vnx
        if (phiVnx == 0) and (Vux != 0):  # force inputted but zero for the section property
            works = False
        else:
            try:
                util_phiVnx = Vux / phiVnx * 100  # individual utilization
            except ZeroDivisionError:  # in case we get a 0/0
                util_phiVnx = 0
                # delete for deployment
                print("phiVnx is 0 and force provided is 0")

        # Vny
        if (phiVny == 0) and (Vuy != 0):  # force inputted but zero for the section property
            works = False
        else:
            try:
                util_phiVny = Vuy / phiVny * 100  # individual utilization
            except ZeroDivisionError:  # in case we get a 0/0
                util_phiVny = 0
                # delete for deployment
                print("phiVny is 0 and force provided is 0")

        # An
        if (phiAn == 0) and (Au != 0):  # force inputted but zero for the section property
            works = False
        else:
            try:
                util_phiAn = Au / phiAn * 100  # individual utilization
            except ZeroDivisionError:  # in case we get a 0/0
                util_phiAn = 0
                # delete for deployment
                print("An is 0 and force provided is 0")

        # Tn
        if (phiTn == 0) and (Tu != 0):  # force inputted but zero for the section property
            works = False
        else:
            try:
                util_phiTn = (Tu / phiTn * 100)  # individual utilization
            except ZeroDivisionError:  # in case we get a 0/0
                util_phiTn = 0
                # delete for deployment
                print("Tn is 0 and force provided is 0")

        if not works:
            return None

        if works:
            # calculate total utilization as sum of individual utilizations
            total_ratio = util_phiMnx + util_phiMny + \
                util_phiVnx + util_phiVny + util_phiAn + util_phiTn
            return util_phiMnx, util_phiMny, util_phiVnx, util_phiVny, util_phiAn, util_phiTn, total_ratio


if __name__ == '__main__':
    b = 8
    d = 15
    w = WeldGroup(t=3, group='⨅', b=b, d=d)

    phiMnx, phiMny, phiVnx, phiVny, phiAn, phiTn = w.properties()
    print()
    print(f'phiMnx = {phiMnx:.2f}')
    print(f'phiMny = {phiMny:.2f}')
    print(f'phiVnx = {phiVnx:.2f}')
    print(f'phiVny = {phiVny:.2f}')
    print(f'phiAn = {phiAn:.2f}')
    print(f'phiTn = {phiTn:.2f}')
    print()
