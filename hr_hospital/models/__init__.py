# isort: skip_file
# Load order matters: hospital_medic_info is inherited by doctor and patient.
from . import hospital_doctor_category
from . import hospital_medic_info
from . import hospital_doctor
from . import hospital_patient
from . import hospital_disease
from . import hospital_visit
from . import hospital_doctor_history
