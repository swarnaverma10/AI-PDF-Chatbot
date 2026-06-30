"""
chatbot.py
----------
Chatbot service layer – Phase 2+ placeholder.

This module will house the orchestration logic that:
  1. Receives a sanitised user question.
  2. Retrieves relevant context from the PDF knowledge base (pdf_reader.py).
  3. Calls the OpenRouter API with the context + question.
  4. Returns the model's answer together with source references.

No implementation is included in Phase 1 – the stub is intentionally
minimal so future developers can locate where to add logic without
restructuring the project.
"""

import logging

logger = logging.getLogger(__name__)


# ============================================================ #
# Phase 2+ – implement when OpenRouter & pdf_reader are ready  #
# ============================================================ #

async def get_answer(question: str, session_id: str | None = None) -> dict:
    """
    Generate an answer for *question* using the PDF knowledge base.

    Args:
        question:   Sanitised user question.
        session_id: Optional session identifier for multi-turn support.

    Returns:
        A dict compatible with ``ChatResponse`` (answer, sources, session_id).

    Raises:
        NotImplementedError: Until Phase 2 is implemented.
    """
    logger.warning(
        "chatbot.get_answer called but not yet implemented (Phase 2+). "
        "question=%r session_id=%r",
        question,
        session_id,
    )
    raise NotImplementedError(
        "Chatbot logic is not implemented yet. "
        "This will be added in Phase 2 once OpenRouter and pdf_reader are wired up."
    )
