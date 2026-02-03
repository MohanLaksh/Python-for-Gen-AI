from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_retry_decorator(max_attempts: int = 3):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError, TimeoutError)),
        before_sleep=lambda retry_state: logger.warning(f"Retrying... attempt {retry_state.attempt_number} ended with: {retry_state.outcome.exception()}")
    )
