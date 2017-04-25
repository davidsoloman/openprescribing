from frontend.models import MeasureGlobal, MeasureValue


def measure_global(measure):
    qs = MeasureGlobal.objects.select_related('measure').order_by('measure_id', 'month')

    if measure:
        qs = qs.filter(measure=measure)

    rolled = {}

    for mg in qs:
        measure_global_data = {
            'date': mg.month,
            'numerator': mg.numerator,
            'denominator': mg.denominator,
            'calc_value': mg.calc_value,
            'percentiles': mg.percentiles,
            'cost_savings': mg.cost_savings
        }

        if mg.measure_id in rolled:
            rolled[mg.measure_id]['data'].append(measure_global_data)
        else:
            rolled[mg.measure_id] = {
                'id': mg.measure_id,
                'name': mg.measure.name,
                'title': mg.measure.title,
                'description': mg.measure.description,
                'why_it_matters': mg.measure.why_it_matters,
                'numerator_short': mg.measure.numerator_short,
                'denominator_short': mg.measure.denominator_short,
                'url': mg.measure.url,
                'is_cost_based': mg.measure.is_cost_based,
                'is_percentage': mg.measure.is_percentage,
                'low_is_good': mg.measure.low_is_good,
                'data': [measure_global_data]
            }

    return {'measures': rolled.values()}


def measure_by_ccg(orgs, measure):
    qs = MeasureValue.objects.select_related('pct', 'measure').filter(pct__org_type='CCG', practice_id=None).order_by('pct_id', 'measure_id', 'month')

    if orgs:
        qs = qs.filter(pct__in=orgs)

    if measure:
        qs = qs.filter(measure=measure)

    rolled = {}

    for mv in qs:
        measure_value_data = {
            'date': mv.month,
            'numerator': mv.numerator,
            'denominator': mv.denominator,
            'calc_value': mv.calc_value,
            'percentile': mv.percentile,
            'cost_savings': mv.cost_savings,
            'pct_id': mv.pct.code,
            'pct_name': mv.pct.name
        }
        if mv.measure_id in rolled:
            rolled[mv.measure_id]['data'].append(measure_value_data)
        else:
            rolled[mv.measure_id] = {
                'id': mv.measure_id,
                'name': mv.measure.name,
                'title': mv.measure.title,
                'description': mv.measure.description,
                'why_it_matters': mv.measure.why_it_matters,
                'numerator_short': mv.measure.numerator_short,
                'denominator_short': mv.measure.denominator_short,
                'url': mv.measure.url,
                'is_cost_based': mv.measure.is_cost_based,
                'is_percentage': mv.measure.is_percentage,
                'low_is_good': mv.measure.low_is_good,
                'data': [measure_value_data]
            }

    return {'measures': rolled.values()}


def measure_by_practice(orgs, measure):
    qs = MeasureValue.objects.select_related('practice', 'measure').order_by('practice_id', 'measure_id', 'month')

    pct_ids = [org for org in orgs if len(org) == 3]
    if pct_ids:
        qs = qs.filter(pct_id__in=pct_ids)

    practice_ids = [org for org in orgs if len(org) != 3]
    if practice_ids:
        qs = qs.filter(practice_id__in=practice_ids)

    if measure:
        qs = qs.filter(measure=measure)

    rolled = {}

    for mv in qs:
        measure_value_data = {
            'date': mv.month,
            'numerator': mv.numerator,
            'denominator': mv.denominator,
            'calc_value': mv.calc_value,
            'percentile': mv.percentile,
            'cost_savings': mv.cost_savings,
            'practice_id': mv.practice_id,
            'practice_name': mv.practice.name
        }
        if mv.measure_id in rolled:
            rolled[mv.measure_id]['data'].append(measure_value_data)
        else:
            rolled[mv.measure_id] = {
                'id': mv.measure_id,
                'name': mv.measure.name,
                'title': mv.measure.title,
                'description': mv.measure.description,
                'why_it_matters': mv.measure.why_it_matters,
                'numerator_short': mv.measure.numerator_short,
                'denominator_short': mv.measure.denominator_short,
                'url': mv.measure.url,
                'is_cost_based': mv.measure.is_cost_based,
                'is_percentage': mv.measure.is_percentage,
                'low_is_good': mv.measure.low_is_good,
                'data': [measure_value_data]
            }

    return {'measures': rolled.values()}
