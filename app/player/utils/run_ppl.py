from ...utils.maafw import Tasker, JobWithResult
from ...utils.datetime import datetime, timedelta, sleep

def maafw_run_ppl(tasker: Tasker, entry: str, pipeline_override: dict = {}, timeout: int = 10) -> tuple[bool, JobWithResult | None]:
    # Deprecated 2025/04/18
    """Run a pipeline task with a timeout.

    Args:
        tasker (Tasker): The Tasker instance to use.
        entry (str): The pipeline entry to run.
        pipeline_override (dict, optional): The pipeline override. Defaults to {}.
        timeout (int, optional): The timeout in seconds. Defaults to 10.

    Returns:
        tuple[bool, object]: A tuple of a boolean indicating whether the task was completed successfully,
            and the job result if the task was completed.
    """
    time_start = datetime.now()
    job = tasker.post_task(entry, pipeline_override)
    while (datetime.now() - time_start) < timedelta(seconds=timeout):
        if job.done:
            return True, job.get()
        # TODO consider shorten sleep time to enhance performance
        sleep(0.01)
    tasker.post_stop()
    return False, job.get()

def dummy_run_ppl (*args, **kwargs) -> tuple[bool, JobWithResult | None]:
    return (False, None)