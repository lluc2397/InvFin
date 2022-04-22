from ..constants import INVESTOR_PROFILES


def INVESTOR_SCORE(investor_story,
    view_on_volatility,
    onefive,
    zerofive,
    investor):

    INVESTOR_TYPE = ((1, 'Activo'), (2, 'Intermedio'), (3, 'Pasivo'), (4, 'Especulador'))

    INVESTOR_RISK_PROFILE = ((1, 'PROFILE VERY AGRESIVE'), (2, 'PROFILE AGRESIVE'), (3, 'PROFILE CONSERVATIVE'), (4, 'PROFILE VERY CONSERVATIVE'), (5, 'PROFILE REGULAR'))

    if int(view_on_volatility) == 1:
        number = 2
        investor_is = 3
        if investor_story.objectif == 2 or investor_story.objectif == 3:
            result = "Muy conservador"
            risk_aversion = 4
            profile_explanation = PROFILE_VERY_CONSERVATIVE

        else:
            result = "Conservador"
            risk_aversion =3
            profile_explanation = PROFILE_CONSERVATIVE
       
    else:
        if int(zerofive) > 0:
            investor_is = 4
            number = 1
            result = "Muy agresivo"
            risk_aversion =1
            profile_explanation = PROFILE_VERY_AGRESIVE
        else:
            if int(onefive) >= 50:
                investor_is = 1
                number = 1
                result = "Agresivo"
                risk_aversion =2
                profile_explanation = PROFILE_AGRESIVE
            else:
                investor_is = 2
                number = 3
                result = "Moderado"
                risk_aversion =5
                profile_explanation = PROFILE_REGULAR            

    

    CURRENT_INVESTORS_TYPE.objects.create(
        investor_related = investor,
        investors_type = investor_is,
        risk_aversion = risk_aversion,
    )


    type_profile_investor = {
        'explanation': profile_explanation,
        'number' : number,
        'result': result
    }

    return type_profile_investor
