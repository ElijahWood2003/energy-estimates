from bs4 import BeautifulSoup
import requests
import pandas as pd

# USA zip information
zipdf = pd.read_csv('db/uszips.csv')

# USA energy provider information 
# From: https://catalog.data.gov/dataset/u-s-electric-utility-companies-and-rates-look-up-by-zipcode-2022
energydf = pd.read_csv('db/iou_zipcodes_2022.csv')

# Takes a zip code and outputs the town
def zip_to_town(zip: int) -> str:
    df = zipdf[zipdf['zip'] == zip]
    
    # if zip was not found throw error
    if(df.empty):
        raise ValueError("This zipcode does not exist.")
    
    city = df['city']
    return city.to_string()[5:].strip()

# Takes a zipcode and outputs the energy provider
# Returns a str list of energy providers
# Automatically removes any duplicates from the list before returning
def zip_to_energy(zip: int) -> list:
    df = energydf[energydf['zip'] == zip]
    
    # if zip was not found throw error
    if(df.empty):
        raise ValueError("This zipcode does not exist.")
    
    utility_series = df['utility_name']
    utility_list: list = []

    # Adding the information into the list iff it is not a duplicate
    for index, value in utility_series.items():
        add: bool = True
        
        # Setting add to false if any duplicates are found of the current item
        for value2 in utility_list:
            if(value2 == value):
                add = False
                break
        
        # If there are no duplicates then add to the list
        if(add):
            utility_list.append(value)
        
    return utility_list

# Takes an energy provider and outputs the residential rates as a list
def energy_to_rates(energy: str) -> list:
    df = energydf[energydf['utility_name'] == energy]
    
    # if zip was not found throw error
    if(df.empty):
        raise ValueError("This energy provider does not exist.")
    
    rates_series = df['res_rate']
    
    rates_list: list = []

    # Adding the information into the list iff it is not a duplicate
    for index, value in rates_series.items():
        add: bool = True
        
        # Setting add to false if any duplicates are found of the current item
        for value2 in rates_list:
            if(value2 == value):
                add = False
                break
        
        # If there are no duplicates then add to the list
        if(add):
            rates_list.append(value)
        
    return rates_list

# Num_panels inputs the annual kwh and pannel wattage and outputs 
# the number of solar panels
def num_panels(ann_kwh: int, pan_watt: int) -> int:
    PEAK_HOURS: float = 4.71
    return int(round((PEAK_HOURS * ann_kwh) / pan_watt))
    
# system_size inputs the annual kwh and sunlight hours
# and outputs the system size
def system_size(ann_kwh: int, sun_hours: float) -> float:
    return float(ann_kwh / sun_hours)

# system_cost = ppw * system size
# BOTH = true iff we should add the 7500 extra
def system_cost(ppw: float, system_size: float, BOTH: bool) -> float:
    both: float = 7500 * BOTH
    return ppw * system_size * 1000 + both

# cost: float = system_cost(1.85, 10, False)
# print(f"System Cost: {cost}")
    
def system_cost_discount(system_cost: float) -> float:
    TAX_CREDIT: float = .3
    return system_cost * TAX_CREDIT

# final_cost calculates all factors and outputs the final (estimated)
# cost of the product
def final_cost(discount: float, system_cost: float) -> float:
    return system_cost - discount
    
# inputs system size and sun hours
# outputs energy in kwh per day
def daily_solar_energy(system_size: float, sun_hours: float) -> float:
    return system_size * sun_hours
    
# yearly_production inputs panel wattage, sunlights hours, and number of panels
# outputs the total ?
def yearly_production(pan_watt: int, sun_hours: float, num_panels: int) -> float:
    return pan_watt * sun_hours * num_panels
    
    
# Example of zipcode input
zipcode: str = input("\nInput a zipcode: ")
zipcode = int(zipcode)

# Example of zip_to_town
print(f"Town: {zip_to_town(zipcode)}")

# Example of zip to energy
energy_list = zip_to_energy(zipcode)
str_space = "                    "
print("Energy Provider(s): " + f",\n{str_space}".join(energy_list[0:]))

# Ask user which energy provider if there are several
index: int = 0
if(len(energy_list) != 1):
    index = int(input("\nWhich energy provider do you have? Type 0-X. "))

# Example of energy to rates
rates_list = energy_to_rates(energy_list[index])
inflation_estimate: float = 0.01
rate = rates_list[0] + inflation_estimate
print("Residential Rates: " + f"{rate}")

# Get monthly energy bill
energy_bill = float(input("\nHow much is your monthly energy bill? $"))

# Output energy estimate
monthly_usage = energy_bill / rate
print("Average Usage of kWh: " + f"{monthly_usage}")

print("\n")