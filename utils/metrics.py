import re

try:
    import textstat
except ImportError:
    textstat = None

def count_words(text: str) -> int:
    return len(text.split())

def count_sentences(text: str) -> int:
    return len(re.findall(r"[\.!\?]+", text))

def average_sentence_length(text: str) -> float:
    s = count_sentences(text)
    w = count_words(text)
    return w / s if s > 0 else 0.0

def estimated_reading_time(text: str, wpm: int = 200) -> float:
    return count_words(text) / wpm

def flesch_reading_ease(text: str) -> float | None:
    if textstat:
        try:
            return textstat.flesch_reading_ease(text)
        except:
            return None
    return None

def grammar_error_count(text: str) -> int | None:
    try:
        import language_tool_python
        tool = language_tool_python.LanguageTool("pt-BR")
        return len(tool.check(text))
    except ImportError:
        return None

def collect_metrics(text: str) -> dict:
    return {
        "words": count_words(text),
        "sentences": count_sentences(text),
        "avg_sentence_length": average_sentence_length(text),
        "reading_time_min": estimated_reading_time(text),
        "flesch_reading_ease": flesch_reading_ease(text),
        "grammar_errors": grammar_error_count(text),
    }
