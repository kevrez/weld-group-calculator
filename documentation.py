strength_doc = """In this program, weld strength is calculated using formula XXX in AISC 360:
                  phiRn = 1.392 * t, where t is the weld throat in sixteenths of an inch.
                  the phi value included in phiRn is the only strength reduction factor considered in these equations."""

section_doc = \
    """Individual section properties are calculated by treating welds as lines, and using formulas provided by Omer W. Blodgett in DESIGN OF WELDMENTS (1976), and WELDED CONNECTIONS by Blodgett et al (1999).

                Moment capacity is calculated by using an equivalent section modulus Sx or Sy from the weld geometry from the appropriate formula. It is then multiplied by the linear strength of the selected weld to obtain a moment capacity in kip-inches. It is then converted to kip-ft as necessary, separate from the calculation.

                Weld groups with asymmetrical shapes have multiple values for Sx provided by Blodgett related to top and bottom. This program uses the mean of the two values as an effective section modulus to determine the strength of the section.

                Shear and axial capacities are calculated by multiplying the total linear length of weld by the weld strength. They will therefore always result in an equal value to each other.

                Torsional strength is calculated by calculating the polar section modulus by dividing J, the torsional constant by c, the average distance to centroid. This modulus is multiplied by the linear weld strength to obtain a strength in kip-inches. It is then converted to kip-ft as necessary, separate from the calculation.

                In this program, the load angle effect described by AISC in section XXXX is not considered. Since AISC allows an increase of up to 50% for loading perpendicular to the line of the weld, the section properties calculated here are accurate to conservative by up to 33%."""

utilization_doc = \
    """Utilization values are calculated differently than the method that Blodgett suggests in WELDED CONNECTIONS. His paper describes the following process:
                    - Find the position on the welded connection where the combination of forces will be maximum
                    - Find the value of each of the forces on the welded connection at this point. Divide the force by the section modulus to determine a minimum required weld strength
                    - Combine (vectorially) all forces on the weld at this point
                    - Determine the required weld strength by dividing this value by the allowable force for the weld

                This program still relies on mechanical principles to determine the strength of the weld group, but it leans on the methods described in AISC 360-15:
                    - Determine the maximum loading on the weld group, considering moment in each direction, shear in each direction, axial force, and torsional force
                    - Calculate the section properties of the weld group from the equations provided by Blodgett and the methods mentioned in the previous section
                    - Multiply each section property by a linear weld strength previously selected by the engineer to obtain the section's strength for that property
                    - Calculate an individual utilization ratio for each force/section property pair by dividing the value of the force by the strength of the related property
                    - Combine the individual utilization ratios by adding them directly (NON-VECTORIAL COMBINATION)
                    - Determine whether the section has sufficient strength by comparing the total utilization to 1.0. If a value above 1.0 is obtained, the section is insufficient to resist the required loading, and the weld must be upsized

                The non-vectorial combination of each individual utilization ratio results in a higher total utilization ratio than if the values were added vectorially using the square root of the sum of the squares. This is a conservative assumption by Uzun+Case and is intended to account for the potential unconservativeness of not studying the most critical point at each weld group. The resulting total ratio is accurate to conservative as a result, similarly to not considering the load angle effect as mentioned in the previous section.

                A second reason for the decision to calculate the strength and utilization of the weld group this way is ease of implementation. This method provides the advantage that the strength of the section and the resulting total utilization ratio can be calculated the same way each time, as opposed to determining the individual weld with the highest demand, which Blodgett's method requires."""
