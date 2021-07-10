# Weld Group Calculator
This program is a calculator for fillet and flare bevel welds in various arrangements, developed by Kevin Reznicek for the use of Uzun+Case Engineers in Atlanta, GA.

## Disclaimers
This program is in an untested state and is NOT currently for use in design or construction. 
The equations and calculation assumptions used in the program are currently in need of vetting by Uzun+Case's team of engineers. 
Before using this application, it is your responsibility to read all of the documentation. 
The equations utilized in the program for each weld group are enumerated in this documentation.

**None of the contributors will be liable for any element of design or construction related to the use of this software. It is the engineer's responsibility to determine adequacy of design. This tool is merely intended to aid in simplifying the design process.**


# Documentation: 
In this program, weld strength is calculated using the provisions in AISC Section J, assuming E70XX electrodes and SMAW welding. 
The basic formula used to calculate the linear weld strength of a given size is:

- &phi;R<sub>n</sub> = 1.392 • t

where t is the weld throat in sixteenths of an inch. 
The &phi; value included in &phi;R<sub>n</sub> is the only strength reduction factor considered in these equations.

Individual section properties are calculated by treating welds as lines, and using formulas provided by Omer W. Blodgett in DESIGN OF WELDMENTS (1976), and WELDED CONNECTIONS by Blodgett et al (1999) to determine weld group section properties. 

## Load Angle
In this program, the load angle effect described by AISC in section J is considered at the user's option. 
Section J allows for an increase of up to 50% in the calculated weld strength for weld in groups with loading perpendicular to the line of the weld. 
This increase, however, must be accompanied by a reduction of 15% in the calculated strength of welds loaded parallel to the line of the weld. 
Expressed as equations, the user is allowed to take the maximum of the following formulas to calculate the strength of the weld group:

- R<sub>n</sub> = R<sub>nwl</sub> + R<sub>nwt</sub> (Equation J2-6a)

- R<sub>n</sub> = 0.85 • R<sub>nwl</sub> + 1.5 • R<sub>nwt</sub> (Equation J2-6b)

## Moment:
Moment capacity is calculated from the section modulus (S<sub>x</sub> or S<sub>y</sub>) formulas provided by Blodgett. 
The section modulus given the weld group geometry is multiplied by the linear strength of the selected weld to obtain a moment capacity.

- &phi;M<sub>n</sub> = &phi;R<sub>n</sub> • S

where S is the section modulus about a given axis.

Weld groups with asymmetrical shapes have multiple values for S<sub>x</sub>, related to the top and bottom of the weld group. 
This program uses the minimum of the two values (S<sub>xt</sub> and S<sub>xb</sub>) as the group's section modulus in order to determine the strength of the section.

## Shear & Axial Forces
Shear and axial capacities are calculated by multiplying the total linear length of weld by the weld strength. 

- &phi;V<sub>n</sub> = &phi;R<sub>n</sub> • L
- &phi;A<sub>n</sub> = &phi;R<sub>n</sub> • L

where L is the length of the given weld, and &phi;R<sub>n</sub> considers the load angle effect, if desired.

When the effect of the loading angle is considered, shear and axial strengths are calculated by adding the strength of each individual weld with respect to the direction it is loaded.

## Torsion
Torsional strength is calculated by calculating the polar section modulus (PM) by dividing J, the torsional constant by c, the average distance to centroid. 
This modulus is multiplied by the linear weld strength to obtain a strength in kip-inches. 

- PM = J / c
- &phi;T<sub>n</sub> = &phi;R<sub>n</sub> • PM

When the effect of the load angle is considered with respect to torsion, the weld strength is considered to always be multiplied by the 0.85 factor from equation J2-6b.

## Utilization & Interaction
Utilization values are calculated differently than the method that Blodgett suggests in WELDED CONNECTIONS. The approach used is based on the same root principles, but was selected due to added ease of implementation:
- Determine the maximum loading on the weld group, considering moment in each direction, shear in each direction, axial force, and torsional force
- Calculate the section properties of the weld group
- Arbitrarily select a weld size and calculate its linear strength
- Multiply the value of each section property by the weld strength to obtain the section's strength for each property
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
- L<sub>V<sub>x</sub></sub> = d • f<sub>T</sub>

- L<sub>V<sub>y</sub></sub> = d • f<sub>L</sub>

- L<sub>A</sub> = d

- S<sub>x</sub> = d<sup>2</sup> / 6

- S<sub>y</sub> = 0

- J = 0

- c = 0

- PM = 0

### Weld group: -
- L<sub>V<sub>x</sub></sub> = b • f<sub>L</sub>

- L<sub>V<sub>y</sub></sub> = b • f<sub>T</sub>

- L<sub>A</sub> = b

- S<sub>x</sub> = 0

- S<sub>y</sub> = b<sup>2</sup> / 6

- J = 0

- c = 0

- PM = 0

### Weld group: ||
- L<sub>V<sub>x</sub></sub> = 2 • d • f<sub>T</sub>

- L<sub>V<sub>y</sub></sub> = 2 • d • f<sub>L</sub>

- L<sub>A</sub> = 2 • d

- S<sub>x</sub> = d<sup>2</sup> / 3

- S<sub>y</sub> = b • d

- J = d/6 • (3b<sup>2</sup> + d<sup>2</sup>)

- c = (b<sup>2</sup> + d<sup>2</sup>)<sup>1/2</sup> / 2

- PM = J / c


### Weld group: =
- L<sub>V<sub>x</sub></sub> = 2 • b • f<sub>L</sub>

- L<sub>V<sub>y</sub></sub> = 2 • b • f<sub>T</sub>

- L<sub>A</sub> = 2 • b

- S<sub>x</sub> = b • d

- S<sub>y</sub> = b<sup>2</sup> / 3

- J = b/6 • (b<sup>2</sup> + 3•d<sup>2</sup>)

- c = (b<sup>2</sup> + d<sup>2</sup>)<sup>1/2</sup> / 2

- PM = J / c

### Weld group: ▯
- L<sub>V<sub>x</sub></sub> = 2b • f<sub>L</sub> + 2d • f<sub>T</sub>

- L<sub>V<sub>y</sub></sub> = 2b • f<sub>T</sub> + 2d • f<sub>L</sub>

- L<sub>A</sub> = 2b + 2d

- S<sub>x</sub> = d/3 • (3b + d)

- S<sub>y</sub> = b/3 • (3•d + b)

- J = (b+d)<sup>3</sup> / 6

- c = (b<sup>2</sup> + d<sup>2</sup>)<sup>1/2</sup> / 2

- PM = J / c

### Weld group: ⨅
- L<sub>V<sub>x</sub></sub> = b • f<sub>L</sub> + 2d • f<sub>T</sub>

- L<sub>V<sub>y</sub></sub> = b • f<sub>T</sub> + 2d • f<sub>L</sub>

- L<sub>A</sub> = b + 2d

- S<sub>xt</sub> = d/3 • (2b + d)

- S<sub>xb</sub> = (d<sup>2</sup>(2b + d)) / (3(b+d))

- S<sub>x</sub> = min(S<sub>xt</sub>, S<sub>xb</sub>)

- S<sub>y</sub> = b/6 • (b + 6d)

- J = d<sup>3</sup> / 3 • ((2b + d)/(b + 2d)) + b<sup>2</sup> / 12 • (b + 6d)

- Nx = d<sup>2</sup> / (b + 2d)

- c = (Nx<sup>2</sup> + (b/2)<sup>2</sup>)<sup>1/2</sup>

- PM = J / c

### Weld group: ╥
- L<sub>V<sub>x</sub></sub> = b • f<sub>L</sub> + 2d • f<sub>T</sub>

- L<sub>V<sub>y</sub></sub> = b • f<sub>T</sub> + 2d • f<sub>L</sub>

- L<sub>A</sub> = b + 2d

- S<sub>xt</sub> = d/3 • (2b + d)

- S<sub>xb</sub> = (d<sup>2</sup> • (2b + d)) / (3 • (b+d))

- S<sub>x</sub> = min(S<sub>xt</sub>, S<sub>xb</sub>)

- S<sub>y</sub> = b<sup>2</sup> / 6

- J = d<sup>3</sup> / 3 • ((2b + d)/(b + 2d)) + b<sup>3</sup> / 12

- Ct = d<sup>2</sup> / (b + 2d)

- Cb = d • ((b+d) / (b + 2d))

- Cu = max(Ct, Cb)

- c = (Cu<sup>2</sup> + (b/2)<sup>2</sup>)<sup>1/2</sup>

- PM = J / c

### Weld group: ╦
- L<sub>V<sub>x</sub></sub> = 2 • (b • f<sub>L</sub> + d • f<sub>T</sub>)

- L<sub>V<sub>y</sub></sub> = 2 • (b • f<sub>T</sub> + d • f<sub>L</sub>)

- L<sub>A</sub> = 2 • (b + d)

- S<sub>xt</sub> = d/3 • (4b + d)

- S<sub>xb</sub> = d<sup>2</sup> / 3 • ((4b + d) / (2b + d))

- S<sub>x</sub> = min(S<sub>xt</sub>, S<sub>xb</sub>)

- S<sub>y</sub> = b<sup>2</sup> / 3

- J = d<sup>3</sup> / 6 • ((4b + d)/(b+d)) + b<sup>3</sup> / 6

- Ct = d<sup>2</sup> / (2(b + d))

- Cb = d/2 • ((2b + d) / (b+d))

- Cu = max(Ct, Cb)

- c = (Cu<sup>2</sup> + (b/2)<sup>2</sup>)<sup>1/2</sup>

- PM = J / c

### Weld group: ⌶
- L<sub>V<sub>x</sub></sub> = 2 • (2b • f<sub>L</sub> + d • f<sub>T</sub>)

- L<sub>V<sub>y</sub></sub> = 2 • (2b • f<sub>T</sub> + d • f<sub>L</sub>)

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

- &phi;V<sub>nx</sub> = &phi;R<sub>n</sub> • L<sub>V<sub>x</sub></sub>

- &phi;V<sub>ny</sub> = &phi;R<sub>n</sub> • L<sub>V<sub>y</sub></sub>

- &phi;A<sub>n</sub> = &phi;R<sub>n</sub> • L<sub>A</sub> • f<sub>T</sub>

- &phi;T<sub>n</sub> = &phi;R<sub>n</sub> • PM • f<sub>L</sub>