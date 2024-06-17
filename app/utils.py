def calculate_plan(height: float, weight: float, age: float, sex: str, factor: float) -> float:
    if sex == 'male':
        result = ((10 * weight) + (6.25 * height) - (5 * age) + 5) * factor
        return round(result, 1)

    if sex == 'female':
        result = ((10 * weight) + (6.25 * height) - (5 * age) - 161) * factor
        return round(result, 1)

    raise ValueError('Unknown sex')