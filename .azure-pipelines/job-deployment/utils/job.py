import json

from databricks_cli.sdk import JobsService


def get_existing_jobs(jobs_service: JobsService):
    # Default limit is 20 for this request. We set it to 100 to make sure we never miss a job
    existing_jobs_request = jobs_service.list_jobs(limit=100)
    return existing_jobs_request.get("jobs", [])


def find_job_id(existing_jobs, job_name):
    for job in existing_jobs:
        if job["settings"]["name"] == job_name:
            return job["job_id"]
    return None


def find_jobs_to_update(existing_jobs, job_configs):
    jobs_to_update = []
    new_jobs = []

    existing_job_names = {job["settings"]["name"] for job in existing_jobs}

    for job_config in job_configs:
        job_name = job_config["name"]

        if job_name in existing_job_names:
            updated_job = {
                "job_id": find_job_id(existing_jobs, job_name),
                "new_settings": job_config,
            }
            jobs_to_update.append(updated_job)
        else:
            new_jobs.append(job_config)

    return jobs_to_update, new_jobs


def load_job_configs(file_paths):
    job_configs = []

    for file_path in file_paths:
        try:
            with open(file_path) as file:
                job_config = json.load(file)
                job_configs.append(job_config)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")

    return job_configs


def update_jobs(jobs_to_update, jobs_service: JobsService):
    for job in jobs_to_update:
        try:
            job_id = job.get("job_id")
            new_settings = job.get("new_settings")
            jobs_service.update_job(job_id, new_settings)
            print(f"Updated job '{job_id}' '{new_settings.get('name')}' successfully")
        except Exception as e:
            print(f"Failed to update job {job_id}: {str(e)}")


def create_jobs(new_jobs, jobs_service: JobsService):
    for job in new_jobs:
        try:
            created_job = jobs_service.create_job(**job)
            print(f"Created job '{created_job['job_id']}' '{created_job['name']}'")
        except Exception as e:
            print(f"Failed to update job {job.get('name')}: {str(e)}")
