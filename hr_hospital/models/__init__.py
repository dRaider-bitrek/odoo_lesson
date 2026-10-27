# isort: skip_file
# Load order matters: hospital_medic_info is inherited by doctor and patient.
from . import hospital_doctor_category as hospital_doctor_category
from . import hospital_medic_info as hospital_medic_info
from . import hospital_doctor as hospital_doctor
from . import hospital_patient as hospital_patient
from . import hospital_disease as hospital_disease
from . import hospital_visit as hospital_visit
from . import hospital_doctor_history as hospital_doctor_history
