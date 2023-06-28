import math
from tabulate import tabulate

## Input Parameters ##

engine_config = {
    "type": "undersquare",
    "stroke_type": "fourStroke",
    "fuel_type": "gasoline",
    "cycle_type": "otto",
    "cylinder_count": 1,
    "rpm_estimation_range": [1000, 10000],
    "rpm_estimation_step": 1000,
    "mep_estimation_range": [50, 100],
    "mep_estimation_step": 10,
    "valve_type": "freevalve",
    "valve_count_per_cylinder": 2,
}

engine_dimensions = {
    "bore": 30.0,  # Diameter of the cylinder (mm)
    "stroke": 37.5,  # Distance the piston travels inside the cylinder (mm)
    "compression_ratio": 8.75,  # Compression ratio
}

### Unit Conversion ###

engine_dimensions_cm = {key: value / 10 for key, value in engine_dimensions.items() if key != "compression_ratio"}
engine_dimensions_in = {key: value * 0.393701 for key, value in engine_dimensions_cm.items()}

### Engine Geometry Calculations ###

piston_crown_surface_area = math.pi / 4 * engine_dimensions_cm["bore"] ** 2  # in square cm
displacement = piston_crown_surface_area * engine_dimensions_cm["stroke"]  # in cubic cm
clearance_volume = displacement / (engine_dimensions["compression_ratio"] - 1)  # in cubic cm
cylinder_volume = displacement + clearance_volume  # in cubic cm
clearance_height = clearance_volume / piston_crown_surface_area
clearance_height_mm = clearance_height * 10

bore_stroke_ratio = engine_dimensions["bore"] / engine_dimensions["stroke"]

engine_config["type"] = "undersquare" if engine_dimensions["stroke"] > engine_dimensions["bore"] else "oversquare"

### Performance Calculations ###

K = engine_config["cylinder_count"]  # Number of cylinders
A = math.pi / 4 * engine_dimensions_in["bore"] ** 2  # Piston area in square inches

# Create a table for horsepower for each RPM and each MEP
HP_table = []
for P in range(engine_config["mep_estimation_range"][0], engine_config["mep_estimation_range"][1] + engine_config["mep_estimation_step"], engine_config["mep_estimation_step"]):
    row = [P]
    for N in range(engine_config["rpm_estimation_range"][0], engine_config["rpm_estimation_range"][1] + engine_config["rpm_estimation_step"], engine_config["rpm_estimation_step"]):
        HP = (P * engine_dimensions_in["stroke"] * A * (N / 2) * K) / 33000
        row.append(HP)
    HP_table.append(row)

# Mean Piston Speed Calculations
mps_table = []
for N in range(engine_config["rpm_estimation_range"][0], engine_config["rpm_estimation_range"][1] + engine_config["rpm_estimation_step"], engine_config["rpm_estimation_step"]):
    mean_piston_speed = 2 * engine_dimensions["stroke"] / 1000 * N / 60  # in m/s
    mps_table.append(mean_piston_speed)

gamma = 1.4  # Heat capacity ratio
thermal_efficiency = 1 - 1 / (engine_dimensions["compression_ratio"] ** (gamma - 1))  # Thermal efficiency

### Results Display ###

geometry_info = [
    ('Engine Configuration', engine_config["type"], ""),
    ('Bore Diameter', f"{engine_dimensions['bore']:.3f}", "mm"),
    ('Stroke Distance', f"{engine_dimensions['stroke']:.3f}", "mm"),
    ('Compression Ratio', f"{engine_dimensions['compression_ratio']:.3f}", ""),
    ('Displacement', f"{displacement:.3f}", "cc"),
    ('Clearance Volume', f"{clearance_volume:.3f}", "cc"),
    ('Cylinder Volume', f"{cylinder_volume:.3f}", "cc"),
    ('Bore-to-Stroke Ratio', f"{bore_stroke_ratio:.3f}", ""),
    ('Piston Crown Surface Area', f"{piston_crown_surface_area:.3f}", "cm^2"),
    ('Clearance Height', f"{clearance_height_mm:.3f}", "mm"),
]

performance_info = [
    ('Thermal Efficiency', f"{thermal_efficiency*100:.3f}", "%"),
    ('Number of Cylinders', f"{K}", ""),
]

# Formatting Mean Piston Speed Table
formatted_mps_table = [[f"{value:.3f}" for value in mps_table]]

mps_headers = [f'{N} RPM' for N in range(engine_config["rpm_estimation_range"][0], engine_config["rpm_estimation_range"][1] + engine_config["rpm_estimation_step"], engine_config["rpm_estimation_step"])]
print("\nMean Piston Speed Table (m/s)")
print(tabulate(formatted_mps_table, headers=mps_headers, tablefmt='pretty'))

formatted_HP_table = [[f"{value:.3f}" if isinstance(value, float) else value for value in row] for row in HP_table]

print("\nGeometry Information")
print(tabulate(geometry_info, headers=['Parameter', 'Value', 'Unit'], tablefmt='pretty'))

print("\nPerformance Information")
print(tabulate(performance_info, headers=['Parameter', 'Value', 'Unit'], tablefmt='pretty'))

hp_headers = ['MEP (psi)'] + [f'{N} RPM' for N in range(engine_config["rpm_estimation_range"][0], engine_config["rpm_estimation_range"][1] + engine_config["rpm_estimation_step"], engine_config["rpm_estimation_step"])]
print("\nHorsepower Table")
print(tabulate(formatted_HP_table, headers=hp_headers, tablefmt='pretty'))
