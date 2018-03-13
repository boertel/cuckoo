from .controller import Controller
from . import resources

app = Controller('api', __name__)

app.add_resource('/', resources.IndexResource)
app.add_resource('/jobs', resources.JobIndexResource)
app.add_resource('/jobs/<job_id>', resources.JobDetailsResource)

app.add_resource('/applications', resources.ApplicationIndexResource)

app.add_resource('/user/<user_id>', resources.UserDetailResource)
