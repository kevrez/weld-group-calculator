strength_doc = """In this program, weld strength is calculated using formula XXX in AISC 360:
                  phiRn = 1.392 * t, where t is the weld throat in sixteenths of an inch.
                  the phi value included in phiRn is the only strength reduction factor considered in these equations."""

section_doc = \
                """Section properties are calculated by treating welds as lines, and using formulas provided by Omer W. Blodgett in DESIGN OF WELDMENTS (1976).

                Moment capacity is calculated by using an equivalent section modulus Sx or Sy from the weld geometry. It is then multiplied by the linear strength of the selected weld to obtain a moment capacity in kip-inches. It is then converted to kip-ft as necessary, separate from the calculation.

                Shear and axial capacities are calculated by multiplying the total linear length of weld by the weld strength. They are therefore considered equal to each other.

                Torsional strength is calculated by calculating the polar section modulus by dividing J, the torsional constant by c, the average distance to centroid. This modulus is multiplied by the linear weld strength to obtain a strength in kip-inches. It is then converted to kip-ft as necessary, separate from the calculation.

                In this program, the load angle effect described by AISC in section XXXX is not considered. Since AISC allows an increase of up to 50% for loading perpendicular to the line of the weld, the section properties calculated here are accurate to conservative by up to 33%."""