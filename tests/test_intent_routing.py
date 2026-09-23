from app.data_analyst.intent_classifier import classify_intent
from app.data_analyst.analyst_tool import answer_data_question


def test_classifies_numeric_query_as_data():
    intent = classify_intent("What is the average revenue in the dataset?")
    assert intent == "data"


def test_classifies_open_ended_query_as_research():
    intent = classify_intent("What are the main causes of inflation?")
    assert intent == "research"


def test_data_analyst_returns_numeric_answer():
    result = answer_data_question("What is the average revenue?")
    assert "answer" in result
    assert isinstance(result["answer"], str)


def test_data_analyst_handles_unsupported_question_gracefully():
    result = answer_data_question("What color is the sky?")
    assert result["value"] is None
    assert "couldn't map" in result["answer"].lower()