#!/usr/bin/env python3

import os
import sys

import databricks_cli.sdk as databricks_sdk
from databricks_cli.configure.config import _get_api_client
from databricks_cli.configure.provider import EnvironmentVariableConfigProvider
from utils.file import get_file_paths
from utils.job import (
    create_jobs,
    find_jobs_to_update,
    get_existing_jobs,
    load_job_configs,
    update_jobs,
)


def main():
    try:
        config = EnvironmentVariableConfigProvider().get_config()
        api_client = _get_api_client(config, command_name="cicd")
        jobs_service = databricks_sdk.JobsService(api_client)

        directory_path = os.environ.get("DIR_PATH")

        file_paths = get_file_paths(directory_path)
        job_configs = load_job_configs(file_paths)
        existing_jobs = get_existing_jobs(jobs_service)
        jobs_to_update, new_jobs = find_jobs_to_update(existing_jobs, job_configs)

        if jobs_to_update:
            update_jobs(jobs_to_update, jobs_service)

        if new_jobs:
            create_jobs(new_jobs, jobs_service)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
