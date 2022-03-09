

def discounted_cashflow(
    last_revenue,
    revenue_growth, 
    net_income_margin, 
    fcf_margin,
    buyback,
    average_shares_out,
    required_return= 0.075, 
    perpetual_growth=0.025
    ):
    
    today_value = 0

    for i in range(1, 6):
        if i <= 1:
            revenue_expected = last_revenue
            shares_outs = average_shares_out

        revenue_expected = revenue_expected * (1+(revenue_growth/100))

        income_expected = revenue_expected * (net_income_margin/100)
        
        fcf_expected = income_expected * (fcf_margin/100)

        discount_factor = (1+required_return)**(i)

        shares_outs = shares_outs * (1-(buyback/100))

        pv_future_cf = fcf_expected / discount_factor
    
        today_value += pv_future_cf
    
    terminal_value = ((fcf_expected * (1+perpetual_growth))/(required_return-perpetual_growth))
    pv_future_cf_tv = terminal_value / discount_factor        
    today_value += pv_future_cf_tv
    fair_value = today_value / shares_outs if shares_outs != 0 else 0

    return fair_value





