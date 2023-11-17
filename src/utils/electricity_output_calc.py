
class SolarPanelSystem:
    """Class for modeling a specific solar panel system"""
    def __init__(self, 
                 system_cost, 
                 system_effect_kWp,
                 insolation, 
                 tilt_and_direction=1.0,
                 power_loss=0.9,
                 effect_reduction=0.9):
        
        self.insolation = insolation
        self.system_cost = system_cost
        self.system_effect_kWp = system_effect_kWp
        self.tilt_and_direction = tilt_and_direction
        self.power_loss = power_loss
        self.effect_reduction = effect_reduction


    def calc_yearly_electricity_output(self):
        """Calculates the output in kWh of a solar panel system for one year"""
        
        kWh = self.system_effect_kWp * self.tilt_and_direction * self.insolation * self.power_loss * self.effect_reduction
        return kWh


    def electricity_cost_saved_per_year(self, electricity_price_per_kWh):
        """Calculates the saved cost per year (from not having to pay the electricity bill)"""
        return self.calc_yearly_electricity_output() * electricity_price_per_kWh
        

    def profitability_over_time(self, list_of_electricity_prices, years=30):
        """Takes a list of yearly electricity prices per kWh and outputs a list of total profitability
        per year, adding the negative purchase price as the initial value. Ex. After 0 years the profitability is <purchase price * -1>,
        after 1 year the profitability is <purchase price * -1 + accumulated savings>"""
        try: 
            correct_input = len(list_of_electricity_prices) == years

            if not correct_input:
                raise ValueError("The list of electricity prices doesn't match the number of years")

        except ValueError as e:
            print(f"An error occurred: {e}")

        else:
            balance_per_year = [self.system_cost * -1]
            total_accumulated_savings = 0
            for electricity_price in list_of_electricity_prices:
                total_accumulated_savings += self.electricity_cost_saved_per_year(electricity_price)
                balance_per_year.append(round((self.system_cost * -1) + total_accumulated_savings, 2))
            
            return balance_per_year


    def years_until_breakeven(self, list_of_electricity_prices, years=30):
        # we could here create a method of this class that outputs the number of years until breakeven
        # This would only be a bonus feature
        pass


if __name__=='__main__':
    
    my_system = SolarPanelSystem(131000, 10, 1000)
    
    list_of_electricity_prices = [1.02, 0.52, 0.49, 1.03, 0.89, 
                                  0.98, 0.59, 0.42, 0.38, 0.36, 
                                  0.48, 0.66, 0.94, 0.82, 0.39, 
                                  0.31, 0.84, 0.57, 0.84, 0.46, 
                                  0.45, 0.34, 0.66, 0.64, 0.97, 
                                  0.39, 0.88, 0.35, 0.8, 0.33]
    
    # print(my_system.calc_yearly_electricity_output())

    # print(my_system.electricity_cost_saved_per_year(0.98))
    print(my_system.profitability_over_time(list_of_electricity_prices))

    # for i in range(30):
    #     list_of_electricity_prices.append(round(random() * 0.75 + 0.3, 2))

