import math 

# Engine configuration
engine_config = {
    "type": "undersquare",
    "stroke_type": "fourStroke",
    "fuel_type": "gasoline",
    "cycle_type": "otto",
    "cylinder_count": 1,
    "rpm_estimation_range": [1000, 10000],
    "rpm_estimation_step": 1000,
}

# Engine dimensions (in millimeters)
engine_dimensions = {
    "bore": 30.0,  # Diameter of the cylinder (mm)
    "stroke": 37.5,  # Distance the piston travels inside the cylinder (mm)
    "compression_ratio": 8.75,  # Compression ratio
}

# Convert bore and stroke from millimeters to centimeters
engine_dimensions_cm = {key: value / 10 for key, value in engine_dimensions.items() if key != "compression_ratio"}

piston_crown_surface_area = math.pi / 4 * engine_dimensions_cm["bore"] ** 2  # in square cm
displacement = piston_crown_surface_area * engine_dimensions_cm["stroke"]  # in cubic cm

# Calculate clearance volume from compression ratio and displacement
clearance_volume = displacement / (engine_dimensions["compression_ratio"] - 1)  # in cubic cm

# Calculate total cylinder volume
cylinder_volume = displacement + clearance_volume  # in cubic cm

# Estimate clearance height in cm
clearance_height = clearance_volume / piston_crown_surface_area

# Convert clearance height from cm to mm for printing
clearance_height_mm = clearance_height * 10

# Check if the engine is undersquare
engine_config["type"] = "undersquare" if engine_dimensions["stroke"] > engine_dimensions["bore"] else "oversquare"

# Assume some values for mean effective pressure (P), engine rpm (N), and number of cylinders (K)
P = 75  # in psi
K = engine_config["cylinder_count"]

# Convert bore and stroke from cm to inches for horsepower calculation
engine_dimensions_in = {key: value * 0.393701 for key, value in engine_dimensions_cm.items()}

# Calculate piston area in square inches
A = math.pi / 4 * engine_dimensions_in["bore"] ** 2

HP_values = []
# Calculate horsepower for each RPM in the range
for N in range(engine_config["rpm_estimation_range"][0], engine_config["rpm_estimation_range"][1] + engine_config["rpm_estimation_step"], engine_config["rpm_estimation_step"]):
    # Calculate horsepower
    HP = (P * engine_dimensions_in["stroke"] * A * (N / 2) * K) / 33000
    HP_values.append(HP)

# Find max and min horsepower
HP_max = max(HP_values)
HP_min = min(HP_values)

# Calculate torque
T = (HP * 5252) / N

gamma = 1.4

# Calculate thermal efficiency
thermal_efficiency = 1 - 1 / (engine_dimensions["compression_ratio"] ** (gamma - 1))

# Print results in columns
print("{:<45} {:>11.3f} {:<10}".format('Thermal Efficiency:', thermal_efficiency*100, "%"))
print("{:<45} {:>11.3f} {:<10}".format('Displacement:', displacement, "cc"))
print("{:<45} {:>11.3f} {:<10}".format('Compression Ratio:', engine_dimensions["compression_ratio"], ""))
print("{:<45} {:>11.3f} {:<10}".format('Clearance Volume:', clearance_volume, "cc"))
print("{:<45} {:>11.3f} {:<10}".format('Cylinder Volume:', cylinder_volume, "cc"))
print("{:<45} {:>11.3f} {:<10}".format('Piston Crown Surface Area:', piston_crown_surface_area, "cm^2"))
print("{:<45} {:>11} {:<10}".format('Engine Configuration:', engine_config["type"], ""))
print("{:<45} {:>11.3f} {:<10}".format('Mean Effective Pressure Placeholder:', P, "psi"))
print("{:<45} {:>11.3f} {:<10}".format('Engine RPM Placeholder:', N, "rpm"))
print("{:<45} {:>11} {:<10}".format('Number of Cylinders:', K, ""))
print("{:<45} {:>11.3f} {:<10}".format('Horsepower Range:', HP_min, "to"))
print("{:<45} {:>11.3f} {:<10}".format(' ', HP_max, "HP"))
print("{:<45} {:>11.3f} {:<10}".format('Torque:', T, "ft-lb"))
print("{:<45} {:>11.3f} {:<10}".format('Bore Diameter:', engine_dimensions["bore"], "mm"))
print("{:<45} {:>11.3f} {:<10}".format('Stroke Distance:', engine_dimensions["stroke"], "mm"))
print("{:<45} {:>11.3f} {:<10}".format('Clearance Height:', clearance_height_mm, "mm"))
