import view_utils as utils


def measure_global(measure):
    query = 'SELECT mg.month AS date, mg.numerator,  '
    query += 'mg.denominator, mg.measure_id, '
    query += 'mg.calc_value, mg.percentiles, mg.cost_savings, '
    query += 'ms.name, ms.title, ms.description, '
    query += 'ms.why_it_matters, '
    query += ' ms.denominator_short, ms.numerator_short, '
    query += 'ms.url, ms.is_cost_based, ms.is_percentage, '
    query += 'ms.low_is_good '
    query += "FROM frontend_measureglobal mg "
    query += "JOIN frontend_measure ms ON mg.measure_id=ms.id "
    if measure:
        query += "WHERE mg.measure_id=%s "
    query += "ORDER BY mg.measure_id, mg.month"

    data = utils.execute_query(query, [[measure]])
    rolled = {}
    for d in data:
        id = d['measure_id']
        d_copy = {
            'date': d['date'],
            'numerator': d['numerator'],
            'denominator': d['denominator'],
            'calc_value': d['calc_value'],
            'percentiles': d['percentiles'],
            'cost_savings': d['cost_savings']
        }
        if id in rolled:
            rolled[id]['data'].append(d_copy)
        else:
            rolled[id] = {
                'id': id,
                'name': d['name'],
                'title': d['title'],
                'description': d['description'],
                'why_it_matters': d['why_it_matters'],
                'numerator_short': d['numerator_short'],
                'denominator_short': d['denominator_short'],
                'url': d['url'],
                'is_cost_based': d['is_cost_based'],
                'is_percentage': d['is_percentage'],
                'low_is_good': d['low_is_good'],
                'data': [d_copy]
            }
    d = {
        'measures': [rolled[k] for k in rolled]
    }
    return d


def measure_by_ccg(orgs, measure):
    query = 'SELECT mv.month AS date, mv.numerator, mv.denominator, '
    query += 'mv.calc_value, mv.percentile, mv.cost_savings, '
    query += 'mv.pct_id, pc.name as pct_name, measure_id, '
    query += 'ms.name, ms.title, ms.description, '
    query += 'ms.why_it_matters, ms.denominator_short, '
    query += 'ms.numerator_short, '
    query += 'ms.url, ms.is_cost_based, ms.is_percentage, '
    query += 'ms.low_is_good '
    query += "FROM frontend_measurevalue mv "
    query += "JOIN frontend_pct pc ON "
    query += "(mv.pct_id=pc.code AND pc.org_type = 'CCG') "
    query += "JOIN frontend_measure ms ON mv.measure_id=ms.id "
    query += "WHERE "
    if orgs:
        query += "("
    for i, org in enumerate(orgs):
        query += "mv.pct_id=%s "
        if (i != len(orgs) - 1):
            query += ' OR '
    if orgs:
        query += ") AND "
    query += 'mv.practice_id IS NULL '
    if measure:
        query += "AND mv.measure_id=%s "
    query += "ORDER BY mv.pct_id, measure_id, date"

    if measure:
        data = utils.execute_query(query, [orgs, [measure]])
    else:
        data = utils.execute_query(query, [orgs])

    rolled = {}
    for d in data:
        id = d['measure_id']
        d_copy = {
            'date': d['date'],
            'numerator': d['numerator'],
            'denominator': d['denominator'],
            'calc_value': d['calc_value'],
            'percentile': d['percentile'],
            'cost_savings': d['cost_savings'],
            'pct_id': d['pct_id'],
            'pct_name': d['pct_name']
        }
        if id in rolled:
            rolled[id]['data'].append(d_copy)
        else:
            rolled[id] = {
                'id': id,
                'name': d['name'],
                'title': d['title'],
                'description': d['description'],
                'why_it_matters': d['why_it_matters'],
                'numerator_short': d['numerator_short'],
                'denominator_short': d['denominator_short'],
                'url': d['url'],
                'is_cost_based': d['is_cost_based'],
                'is_percentage': d['is_percentage'],
                'low_is_good': d['low_is_good'],
                'data': [d_copy]
            }

    d = {
        'measures': [rolled[k] for k in rolled]
    }
    return d


def measure_by_practice(orgs, measure):
    query = 'SELECT mv.month AS date, mv.numerator, mv.denominator, '
    query += 'mv.calc_value, mv.percentile, mv.cost_savings, '
    query += 'mv.practice_id, pc.name as practice_name, measure_id, '
    query += 'ms.name, ms.title, ms.description, ms.why_it_matters, '
    query += 'ms.denominator_short, ms.numerator_short, '
    query += 'ms.url, ms.is_cost_based, ms.is_percentage, '
    query += 'ms.low_is_good '
    query += "FROM frontend_measurevalue mv "
    query += "JOIN frontend_practice pc ON mv.practice_id=pc.code "
    query += "JOIN frontend_measure ms ON mv.measure_id=ms.id "
    query += "WHERE "
    for i, org in enumerate(orgs):
        if len(org) == 3:
            query += "mv.pct_id=%s "
        else:
            query += "mv.practice_id=%s "
        if (i != len(orgs) - 1):
            query += ' OR '
    if measure:
        query += "AND mv.measure_id=%s "
    query += "ORDER BY mv.practice_id, measure_id, date"

    if measure:
        data = utils.execute_query(query, [orgs, [measure]])
    else:
        data = utils.execute_query(query, [orgs])

    rolled = {}
    for d in data:
        id = d['measure_id']
        d_copy = {
            'date': d['date'],
            'numerator': d['numerator'],
            'denominator': d['denominator'],
            'calc_value': d['calc_value'],
            'percentile': d['percentile'],
            'cost_savings': d['cost_savings'],
            'practice_id': d['practice_id'],
            'practice_name': d['practice_name']
        }
        if id in rolled:
            rolled[id]['data'].append(d_copy)
        else:
            rolled[id] = {
                'id': id,
                'name': d['name'],
                'title': d['title'],
                'description': d['description'],
                'why_it_matters': d['why_it_matters'],
                'numerator_short': d['numerator_short'],
                'denominator_short': d['denominator_short'],
                'url': d['url'],
                'is_cost_based': d['is_cost_based'],
                'is_percentage': d['is_percentage'],
                'low_is_good': d['low_is_good'],
                'data': [d_copy]
            }

    d = {
        'measures': [rolled[k] for k in rolled]
    }
    return d
