import os

from anstosstools import project_logger


def test_logging(tmpdir):
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    log_file = os.path.join(tmpdir, 'test_log.txt')

    project_logger.setup_logger(log_file)
    project_logger.test_logging()
