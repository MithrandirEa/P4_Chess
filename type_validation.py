from datetime import datetime


def validate_cast(prompt: str, expected_type, default=None):
    """
    Demande une saisie à l'utilisateur et la convertit vers le type attendu.
    - prompt : texte affiché à l'utilisateur
    - expected_type : type attendu (int, float, str, datetime)
    - default : valeur par défaut si l'utilisateur appuie sur Entrée sans rien saisir
    """

    while True:
        raw = input(prompt).strip()

        # Si l'utilisateur n'écrit rien → on prend la valeur par défaut
        if raw == "" and default is not None:
            return default

        try:
            # Cas particulier : date
            if expected_type == datetime:
                return datetime.strptime(raw, "%Y-%m-%d")

            # Cas général (int, float, str, etc.)
            return expected_type(raw)

        except ValueError:
            # Message d'erreur clair selon le type attendu
            if expected_type is int:
                print("Valeur invalide. On attend un nombre entier (ex: 4).")
            elif expected_type is float:
                print("Valeur invalide. On attend un nombre décimal (ex: 0.5).")
            elif expected_type is datetime:
                print("Date invalide. Format attendu : YYYY-MM-DD (ex: 2025-08-01).")
            else:
                print(f"Valeur invalide. On attend un type {expected_type.__name__}.")
