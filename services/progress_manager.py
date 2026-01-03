class ProgressManager:
    """Provides static utility methods for progress calculation and ASCII bar generation."""

    @staticmethod
    def calculate_percentage(current : int, total : int) -> float:
        if total <= 0: return 0
        return round((current / total) * 100, 2)

    @staticmethod
    def generate_bar(percentage : float, length : int = 20) -> tuple[str, str]:
        filled_length = round(length * percentage / 100)
        bar = '█' * filled_length + '░' * (length - filled_length)
        return f"|{bar}|", f"{percentage}%"