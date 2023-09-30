def cros_vec(vector1, vector2):
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Los vectores deben tener tres componentes.")

    a1, a2, a3 = vector1
    b1, b2, b3 = vector2

    cros_vec_x = a2 * b3 - a3 * b2
    cros_vec_y = a3 * b1 - a1 * b3
    cros_vec_z = a1 * b2 - a2 * b1

    return (cros_vec_x, cros_vec_y, cros_vec_z)


def sub_vec(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Los arrays deben tener la misma longitud.")

    result = []
    for i in range(len(array1)):
        result.append(array1[i] - array2[i])

    return tuple(result)

def add_vec(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Los arrays deben tener la misma longitud.")

    result = []
    for i in range(len(array1)):
        result.append(array1[i] + array2[i])

    return tuple(result)

def mul_vec(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Los arrays deben tener la misma longitud.")

    result = []
    for i in range(len(array1)):
        result.append(array1[i] * array2[i])

    return tuple(result)

def mul_veck(scalar, array):
    result = []
    for i in range(len(array)):
        result.append(scalar * array[i])

    return tuple(result)

def div_veck(array,scalar):
    result = []
    for i in range(len(array)):
        result.append(array[i]/scalar)

    return tuple(result)

def get_magnitude(vector):
    suma_cuadrados = sum(componente ** 2 for componente in vector)
    norma = suma_cuadrados ** 0.5
    return norma

def normalize_vec(vector):
    norma = get_magnitude(vector)
    if norma == 0:
        raise ValueError("No se puede normalizar un vector nulo.")

    vector_normalizado = [componente/norma for componente in vector]

    return tuple(vector_normalizado)


def dot_vec(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma longitud")

    product = sum(x * y for x, y in zip(vector1, vector2))
    return product

def negate_vec(vector):
    vector = list(vector)
    for i in range(len(vector)):
        vector[i] *= -1
        
    return vector