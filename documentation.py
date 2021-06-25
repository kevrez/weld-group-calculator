# this line is a git test

strength_doc = """In this program, weld strength is calculated using formula XXX in AISC 360:
                  phiRn = 1.392 * t, where t is the weld throat in sixteenths of an inch.
                  the phi value included in phiRn is the only strength reduction factor considered in these equations."""

section_doc = """Section properties are calculated by treating welds as lines, and using formulas provided\
                by Omer W. Blodgett in DESIGN OF WELDMENTS (1976).

                Moment capacity is calculated by using an equivalent section modulus Sx or Sy from the weld geometry. It is then multiplied by the linear strength of the selected weld to obtain a moment capacity in kip-inches.

                Shear and axial capacities are calculated by multiplying the total linear length of weld by the weld strength. They are therefore considered equal to each other.

                Torsional strength is calculated by calculating the polar section modulus by dividing J, the XXX by c, the XXX. This modulus is multiplied by the linear weld strength to obtain a strength in kip-inches.

                In this program, the load angle effect described by AISC in section XXXX is not considered. Since AISC allows an increase of up to 50% for loading perpendicular to the line of the weld, the section properties calculated here are accurate to conservative by up to 33%."""

formula_doc ="""
            | Single Vertical Line
                length = d
                Sx = d ** 2 / 6
                Sy = 0
                J = 0
                PM = 0
                c = 0

            - Single Horizontal Line
                length = b
                Sx = b ** 2 / 6
                Sy = 0
                J = 0
                PM = 0
                c = 0

            || Double Vertical Line
                length = b + d
                Sx = d ** 2 / 3
                Sy = b * d
                J = d / 6 * (3 * b ** 2 + d ** 2)
                c = (b ** 2 + d ** 2) ** 0.5 / 2
                PM = J / c

            = Double Horizontal Line
                length = 2 * b
                Sx = b * d
                Sy = b ** 2 / 3
                J = b / 6 * (b ** 2 + 3 * d ** 2)
                c = (b ** 2 + d ** 2) ** 0.5 / 2
                PM = J / c

            ▯ Rectangle
                length = 2 * b + 2 * d
                Sx = d / 3 * (3 * b + d)
                Sy = b / 3 * (b + 3 * d)
                J = (b + d) ** 3 / 6
                c = (b ** 2 + d ** 2) ** 0.5 / 2
                PM = J / c

            # CHECK ALL THE FORMULAS BELOW THIS

            ⨅ Two Vertical Lines/One Horizontal Line
                length = b + 2 * d
                # check, there are multiple Sx values shown
                Sx = d / 3 * (2 * b + d)
                Sy = b / 6 * (b + 6 * d)
                J = d**2 / 3 * ((2 * b + d)/(b + 2 * d)) + \
                    b**2 / 12 * (b + 6 * d)  # check
                Nx = d**2 / (b + 2 * d)
                c = (Nx**2 + (b / 2)**2)**0.5  # check
                PM = J / c

            ╥ Two Vertical Lines with Top Flange
                length = b + 2 * d
                Sx = d / 3 * (2 * b + d)
                Sy = b**2 / 6
                J = d**3 / 3 * (2 * b + d)/(b + 2 * d) + b**3 / 12  # check
                Ct = d**2 / (b + 2 * d)  # check
                c = (Ct**2 + (b / 2)**2)**0.5  # check
                PM = J / c

            ╦ Wide Flange Section - Upper Perimeter
                length = 2 * (b + d)
                Sx = d / 3 * (4 * b + d)
                Sy = b / 3
                J = d**3 / 6 * ((4 * b + d)/(b + d)) + b**2 / 6  # check
                Ct = d**2 / (2 * (b + d))
                c = (Ct**2 + (b / 2)**2)**0.5  # check
                PM = J / c

            ⌶ Wide Flange Section - Full Perimeter
                length = 2 * (2 * b + d)
                Sx = d / 3 * (6 * b + d)
                Sy = 2 / 3 * b**2
                J = d**2 / 6 * (6 * b + d) + b**3 / 3
                c = (b**2 + d**2)**0.5 / 2
                PM = J / c
                """

