UNIDADES_CONVERSION = {
    "resistencia": {
        "µΩ": 1e-6,
        "mΩ": 1e-3,
        "Ω": 1,
        "kΩ": 1e3,
        "MΩ": 1e6,
        "GΩ": 1e9
    },
    "voltaje": {
        "µV": 1e-6,
        "mV": 1e-3,
        "V": 1,
        "kV": 1e3
    },
    "corriente": {
        "µA": 1e-6,
        "mA": 1e-3,
        "A": 1,
        "kA": 1e3
    },
    "torque": {
        "Nmm": 1e-3,
        "Nm": 1,
        "kNm": 1e3
    },
    "tiempo": {
        "ms": 1e-3,
        "s": 1,
        "min": 60,
        "h": 3600
    }
}


def convertir(valor: float, de: str, a: str, categoria: str) -> float:
    """
    Convierte un valor entre unidades dentro de la misma categoría.
    Ejemplo: convertir(1000, "mV", "V", "voltaje") => 1.0
    """
    if categoria not in UNIDADES_CONVERSION:
        raise ValueError(f"Categoría desconocida: {categoria}")

    unidades = UNIDADES_CONVERSION[categoria]
    if de not in unidades or a not in unidades:
        raise ValueError(f"Unidad desconocida en {categoria}: {de} o {a}")

    valor_base = valor * unidades[de]
    return valor_base / unidades[a]


if __name__ == "__main__":
    print(convertir(1000, "mV", "V", "voltaje"))  # 1.0
    print(convertir(1, "h", "s", "tiempo"))       # 3600.0
    print(convertir(100, "mΩ", "Ω", "resistencia"))  # 0.1
