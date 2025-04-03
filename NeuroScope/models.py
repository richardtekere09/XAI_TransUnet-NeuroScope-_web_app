from django.db import models
from django.contrib.auth.models import User

# -------------------------------------
# ✅ Profile Model (For Doctors/Researchers)
# -------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to Django User model
    bio = models.CharField(max_length=300, blank=True, null=True)  # Short description
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)  # Doctor/Researcher certificate
    is_verified = models.BooleanField(default=False)  # Admin verification
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/default-avatar.png'
    )  # Default avatar

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.is_verified else 'Unverified'}"


# -------------------------------------
# ✅ Doctors (Verified Researchers)
# -------------------------------------
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to Django User model
    specialty = models.CharField(max_length=100)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Admin verifies status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.username} - {'Verified' if self.is_verified else 'Unverified'}"


# -------------------------------------
#  MRI Scans Table
# -------------------------------------
class MRI_Scan(models.Model):
    patient_uid = models.CharField(max_length=50, unique=True)  # Unique identifier for each scan
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Doctor who uploaded the scan
    scan_file = models.FileField(upload_to='mri_scans/')  # Uploaded MRI scan file (DICOM/NIfTI)
    preprocessed_scan = models.FileField(upload_to='preprocessed_scans/', blank=True, null=True)  # Preprocessed version
    segmentation_result = models.FileField(upload_to='segmentation_results/', blank=True, null=True)  # AI segmentation
    shap_explanation = models.FileField(upload_to='xai_shap/', blank=True, null=True)  # SHAP explanations
    grad_cam_explanation = models.FileField(upload_to='xai_gradcam/', blank=True, null=True)  # Grad-CAM explanations
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    notes = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Scan {self.patient_uid} uploaded by {self.doctor.user.username}"


# -------------------------------------
#  Doctor Feedback (Reviews)
# -------------------------------------
class DoctorFeedback(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Doctor giving feedback
    scan = models.ForeignKey(MRI_Scan, on_delete=models.CASCADE)  # Related MRI scan
    feedback = models.TextField()  # Doctor's review on segmentation result
    rating = models.IntegerField(blank=True, null=True)  # Rating (Optional)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Feedback by {self.doctor.user.username} on Scan {self.scan.patient_uid}"
