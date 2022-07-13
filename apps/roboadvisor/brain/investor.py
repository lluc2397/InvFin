from ..constants import *
from ..models import (
    InvestorProfile,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionRiskAversion,
    TemporaryInvestorProfile,
)


def get_investor_type(user, service_activity):

    experience = RoboAdvisorQuestionInvestorExperience.objects.get(
        user=user, service_activity=service_activity
        )
    risk_aversion = RoboAdvisorQuestionRiskAversion.objects.get(
        user=user, service_activity=service_activity
        )

    view_on_volatility = risk_aversion.volatilidad
    objectif = experience.objectif
    zero_five = risk_aversion.percentage_for_zerofive
    one_five = risk_aversion.percentage_for_onefive
    time_investing_exp = experience.time_investing_exp
    period_investing_exp = experience.period_investing_exp

    investor_type = 4
    horizon = 3
    if period_investing_exp == 5:
        horizon = 1
        if time_investing_exp < 10:
            horizon = 2
    

    if view_on_volatility == 1:
        investor_type = 3
        if objectif == 3:
            result = "Muy conservador"
            risk_profile = 4
            profile_explanation = PROFILE_VERY_CONSERVATIVE

        else:
            result = "Conservador"
            risk_profile = 3
            profile_explanation = PROFILE_CONSERVATIVE
       
    else:
        if zero_five > 0:
            
            result = "Muy agresivo"
            risk_profile = 1
            profile_explanation = PROFILE_VERY_AGRESIVE

        else:
            if one_five >= 50:
                investor_type = 1
                result = "Agresivo"
                risk_profile =2
                profile_explanation = PROFILE_AGRESIVE

            else:
                investor_type = 2
                result = "Moderado"
                risk_profile =5
                profile_explanation = PROFILE_REGULAR            


    type_profile_investor = {
        'horizon': horizon,
        'risk_profile': risk_profile,
        'investor_type': investor_type
    }

    if user.has_investor_profile:
        investor_profile = user.user_investor_profile
    else:
        type_profile_investor['user'] = user
        investor_profile = InvestorProfile.objects.create(**type_profile_investor)
        type_profile_investor.pop('user')
    
    type_profile_investor['profile_related'] = investor_profile
    TemporaryInvestorProfile.objects.create(**type_profile_investor)

    return {
        'explanation': profile_explanation,
        'result': result
    }
