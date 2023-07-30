# Deploy notebooks to shared workspace

![Repository databricks techniques](https://docs.databricks.com/_images/repos-cicd-techniques.png)
| Source: Databricks (https://docs.databricks.com/_images/repos-cicd-techniques.png)

For this template's case, the notebooks are deployed to all the workspaces defined in the pipeline steps to the **"Shared"** directory on the Databricks workspace. This pipeline opts out to use the repository integration, since of the time writing this, we found it hard to manage for large scale of teams. If there will be an official repository integration with Azure DevOps or Github, where personal access token are managed by an Active Directory, we would try to create a revised version.
