"""
pdf_reader.py
-------------
PDF reading service – Phase 3+ placeholder.

This module will use pdfplumber to:
  1. Load the PDF from the path specified in config.py.
  2. Extract and clean text page-by-page.
  3. Expose helper functions for chunk-based retrieval that the chatbot
     service can call to find relevant context.

No implementation is included in Phase 1.
"""

import logging

logger = logging.getLogger(__name__)


# ============================================================ #
# Phase 3+ – implement when pdfplumber is ready                #
# ============================================================ #

def load_pdf(path: str) -> None:
    """
    Load and parse the PDF at *path* using pdfplumber.

    Args:
        path: Filesystem path to the PDF file.

    Raises:
        NotImplementedError: Until Phase 3 is implemented.
    """
    logger.warning(
        "pdf_reader.load_pdf called but not yet implemented (Phase 3+). "
        "path=%r",
        path,
    )
    raise NotImplementedError(
        "PDF reading logic is not implemented yet. "
        "This will be added in Phase 3 using pdfplumber."
    )


def extract_text(path: str) -> str:
    """
    Extract all text from the PDF at *path*.

    Args:
        path: Filesystem path to the PDF file.

    Returns:
        Full extracted text as a single string.

    Raises:
        NotImplementedError: Until Phase 3 is implemented.
    """
    raise NotImplementedError("Phase 3+: extract_text not yet implemented.")
