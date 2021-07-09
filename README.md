# Weld Group Calculator
This program is a calculator for fillet and flare bevel welds in various arrangements It was developed by Kevin Reznicek.

## Disclaimers
This program is in an untested state and is NOT for use in design or construction. 
The equations used in the program are still in need of review. 
Before using, it is your responsibility to read all of the documentation. 
The equations utilized in the program for each weld group are enumerated in this documentation.

None of the contributors will be liable for any element of design or construction related to the use of this software.


# Documentation: 
In this program, weld strength is calculated using AISC Section J, assuming E70XX electrodes and SMAW welding. 
The basic formula used to calculate the linear weld strength of a given size is:

&phi;R<sub>n</sub> = 1.392 • t

where t is the weld throat in sixteenths of an inch. 
The &phi; value included in &phi;R<sub>n</sub> is the only strength reduction factor considered in these equations.

Individual section properties are calculated by treating welds as lines, and using formulas provided by Omer W. Blodgett in DESIGN OF WELDMENTS (1976), and WELDED CONNECTIONS by Blodgett et al (1999). 

## Load Angle
In this program, the load angle effect described by AISC in section J is considered at the user's option. 
Section J allows for an increase of up to 50% in calculated weld strength for weld in groups with loading perpendicular to the line of the weld. 
This increase, however, must be accompanied by a reduction of 15% in the calculated strength of welds loaded parallel to the line of the weld. 
Expressed as equations, the user is allowed to take the maximum of the following formulas to calculate the strength of the weld group:

- R<sub>n</sub> = R<sub>nwl</sub> + R<sub>nwt</sub> (Equation J2/-6a)

- R<sub>n</sub> = 0.85 • R<sub>nwl</sub> + 1.5 • R<sub>nwt</sub> (Equation J2-6b)

## Moment:
Moment capacity is calculated from the section modulus (S<sub>x</sub> or S<sub>y</sub>) provided by Blodgett from the weld geometry from the appropriate formula. 
The section modulus is then multiplied by the linear strength of the selected weld to obtain a moment capacity in kip-inches. 
It is then converted to kip-ft as necessary, separate from the calculation.

Weld groups with asymmetrical shapes have multiple values for S<sub>x</sub>, related to top and bottom of the weld group. 
This program uses the minimum of the two values (S<sub>xt</sub> and S<sub>xb</sub>) as the group's section modulus in order to determine the strength of the section.

## Shear & Axial Forces
Shear and axial capacities are calculated by multiplying the total linear length of weld by the weld strength. 

When the effect of the loading angle is considered, shear and axial strengths are calculated by treating each weld individually with respect to the direction it is loaded.

## Torsion
Torsional strength is calculated by calculating the polar section modulus by dividing J, the torsional constant by c, the average distance to centroid. 
This modulus is multiplied by the linear weld strength to obtain a strength in kip-inches. 
It is then converted to kip-ft as necessary, separate from the calculation.

When the effect of the load angle is considered with respect to torsion, the weld strength is considered to always be multiplied by the 0.85 factor from equation J2-6b.

## Utilization & Interaction
Utilization values are calculated differently than the method that Blodgett suggests in WELDED CONNECTIONS. This approach is still based on the same root principles, but was chosen due to added ease of implementation:
- Determine the maximum loading on the weld group, considering moment in each direction, shear in each direction, axial force, and torsional force
- Calculate the section properties of the weld group for each individual case
- Arbitratily select a weld size and calculate its linear strength
- Multiply the value of each section property by the weld strength to obtain the section's strength for that property
- Calculate an individual utilization ratio for each force/section property pair
- Combine the individual utilization ratios, either by adding them directly, or by using the square-root-of-sum-of-squares (SRSS) method
- Determine whether the section has sufficient strength by comparing the total utilization to 1.0. If a value above 1.0 is obtained, the section is insufficient to resist the required loading, and the weld must be upsized or the section geometry updated

## Section Property Formulas

### Factors
When load angle is not considered:

- f<sub>T</sub> = 1.0

- f<sub>L</sub> = 1.0

When load angle is considered:

- f<sub>T</sub> = 1.5

- f<sub>L</sub> = 0.85

### Weld group: |
- L<sub>Vx</sub> = d • f<sub>T</sub>

- L<sub>Vy</sub> = d • f<sub>L</sub>

- L<sub>A</sub> = d

- S<sub>x</sub> = (d<sup>2</sup>) / 6

- S<sub>y</sub> = 0

- J = 0

- c = 0

- PM = 0

### Weld group: -
- L<sub>Vx</sub> = b • f<sub>L</sub>

- L<sub>Vy</sub> = b • f<sub>T</sub>

- L<sub>A</sub> = b

- S<sub>x</sub> = 0

- S<sub>y</sub> = (b<sup>2</sup>) / 6

- J = 0

- c = 0

- PM = 0

### Weld group: ||
- L<sub>Vx</sub> = 2 • d • f<sub>T</sub>

- L<sub>Vy</sub> = 2 • d • f<sub>L</sub>

- L<sub>A</sub> = 2 • d

- S<sub>x</sub> = (d<sup>2</sup>) / 3

- S<sub>y</sub> = b • d

- J = d/6 • (3b<sup>2</sup> + d<sup>2</sup>)

- c = (b<sup>2</sup> + d<sup>2</sup>)<sup>1/2</sup> / 2

- PM = J / c


### Weld group: =
- L<sub>Vx</sub> = 2 • b • f<sub>L</sub>

- L<sub>Vy</sub> = 2 • b • f<sub>T</sub>

- L<sub>A</sub> = 2 • b

- S<sub>x</sub> = b • d

- S<sub>y</sub> = (b<sup>2</sup>) / 3

- J = b/6 • (b<sup>2</sup> + 3•d<sup>2</sup>)

- c = (b<sup>2</sup> + d<sup>2</sup>) ^ 0.5 / 2

- PM = J / c

### Weld group: ▯
- L<sub>Vx</sub> = 2b • f<sub>L</sub> + 2•d • f<sub>T</sub>

- L<sub>Vy</sub> = 2b • f<sub>T</sub> + 2•d • f<sub>L</sub>

- L<sub>A</sub> = 2b + 2•d

- S<sub>x</sub> = d/3 • (3b + d)

- S<sub>y</sub> = b/3 • (3•d + b)

- J = (b+d)<sup>3</sup> / 6

- c = (b<sup>2</sup> + d<sup>2</sup>)<sup>1/2</sup> / 2

- PM = J / c

### Weld group: ⨅
- L<sub>Vx</sub> = b • f<sub>L</sub> + 2•d • f<sub>T</sub>

- L<sub>Vy</sub> = b • f<sub>T</sub> + 2•d • f<sub>L</sub>

- L<sub>A</sub> = b + 2•d

- S<sub>xt</sub> = d/3 • (2b + d)

- S<sub>xb</sub> = (d<sup>2</sup> • (2b + d)) / (3 • (b+d))

- S<sub>x</sub> = min(S<sub>xt</sub>, S<sub>xb</sub>)

- S<sub>y</sub> = b/6 • (b + 6•d)

- J = d<sup>3</sup> / 3 • ((2b + d)/(b + 2•d)) + b<sup>2</sup> / 12 • (b+6 • d)

- Nx = d<sup>2</sup> / (b + 2•d)

- c = (Nx<sup>2</sup> + (b/2)<sup>2</sup>)<sup>1/2</sup>

- PM = J / c

### Weld group: ╥
- L<sub>Vx</sub> = b • f<sub>L</sub> + 2•d • f<sub>T</sub>

- L<sub>Vy</sub> = b • f<sub>T</sub> + 2•d • f<sub>L</sub>

- L<sub>A</sub> = b + 2•d

- S<sub>xt</sub> = d/3 • (2b + d)

- S<sub>xb</sub> = (d<sup>2</sup> • (2b + d)) / (3 • (b+d))

- S<sub>x</sub> = min(S<sub>xt</sub>, S<sub>xb</sub>)

- S<sub>y</sub> = b<sup>2</sup> / 6

- J = d<sup>3</sup> / 3 • ((2b + d)/(b + 2•d)) + b<sup>3</sup> / 12

- Ct = d<sup>2</sup> / (b + 2•d)

- Cb = d • ((b+d) / (b + 2•d))

- Cu = max(Ct, Cb)

- c = (Cu<sup>2</sup> + (b/2)<sup>2</sup>)<sup>1/2</sup>

- PM = J / c

### Weld group: ╦
- L<sub>Vx</sub> = 2 • (b • f<sub>L</sub> + d • f<sub>T</sub>)

- L<sub>Vy</sub> = 2 • (b • f<sub>T</sub> + d • f<sub>L</sub>)

- L<sub>A</sub> = 2 • (b + d)

- S<sub>xt</sub> = d/3 • (4b + d)

- S<sub>xb</sub> = d<sup>2</sup> / 3 • ((4b + d) / (2b + d))

- S<sub>x</sub> = min(S<sub>xt</sub>, S<sub>xb</sub>)

- S<sub>y</sub> = b<sup>2</sup> / 3

- J = d<sup>3</sup> / 6 • ((4b + d)/(b+d)) + b<sup>3</sup> / 6

- Ct = d<sup>2</sup> / (2 • (b+d))

- Cb = d/2 • ((2b + d) / (b+d))

- Cu = max(Ct, Cb)

- c = (Cu<sup>2</sup> + (b/2)<sup>2</sup>)<sup>1/2</sup>

- PM = J / c

### Weld group: ⌶
- L<sub>Vx</sub> = 2 • (2b • f<sub>L</sub> + d • f<sub>T</sub>)

- L<sub>Vy</sub> = 2 • (2b • f<sub>T</sub> + d • f<sub>L</sub>)

- L<sub>A</sub> = 2 • (2b + d)

- S<sub>x</sub> = d/3 • (6b + d)

- S<sub>y</sub> = 2/3 • b<sup>2</sup>

- J = d<sup>2</sup> / 6 • (6b + d) + b<sup>3</sup> / 3

- c = (b<sup>2</sup> + d<sup>2</sup>)<sup>1/2</sup> / 2

- PM = J / c

### Section Properties
Note: f<sub>T</sub> and f<sub>L</sub> are applied for shear and axial properties when calculating the 'effective' length of weld within the weld group.

- &phi;M<sub>nx</sub> = &phi;R<sub>n</sub> • Sx • f<sub>T</sub>

- &phi;M<sub>ny</sub> = &phi;R<sub>n</sub> • Sy • f<sub>T</sub>

- &phi;V<sub>nx</sub> = &phi;R<sub>n</sub> • L<sub>Vx</sub>

- &phi;V<sub>ny</sub> = &phi;R<sub>n</sub> • L<sub>Vy</sub>

- &phi;A<sub>n</sub> = &phi;R<sub>n</sub> • L<sub>A</sub> • f<sub>T</sub>

- &phi;T<sub>n</sub> = &phi;R<sub>n</sub> • PM • f<sub>L</sub>