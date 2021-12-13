from prefect import task, Flow

from musedashboard.mongo_job_flow import MongoJobFlow


@task
def update_history_muse_dashboard():
    MongoJobFlow.save_history_in_mongo_db()


flow = Flow("muse_dashboard", tasks=[update_history_muse_dashboard])

flow.register(project_name="muse_dashboard")
