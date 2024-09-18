area_of_study_choice = (
    (6, 'Medicine'),
)

level_of_english_choices = (
    (0, 'Beginner'),
    (1, 'Elementary'),
    (2, 'Pre-intermediate'),
    (3, 'Low Intermediate'),
    (4, 'Intermediate'),
    (5, 'Upper Intermediate'),
    (6, 'Pre-advanced'),
    (7, 'Advanced'),
    (8, 'Very Advanced'),
)

intake_month_choices = (
    (0, 'January'),
    (1, 'February'),
    (2, 'March'),
    (3, 'April'),
    (4, 'May'),
    (5, 'June'),
    (6, 'July'),
    (7, 'August'),
    (8, 'September'),
    (9, 'October'),
    (10, 'November'),
    (11, 'December'),
)

profile_status_choices = (
    (0, 'approved'),
    (1, 'rejected'),
    (2, 'hold'),
)

questions_choice = (
    (0, 'NO'),
    (1, 'YES'),
)

programme_level_choices_student = (
    (0, 'Foundation'),
    (1, 'Undergraduate'),
    (2, 'Postgraduate'),
    (3, 'Research'),
)
programme_level_choices_mentor = (
    (0, 'SSC'),
    (1, 'HSC'),
    (2, 'A Level'),
    (3, 'GCSE'),
    (4, 'Bachelors'),
    (5, 'Masters'),
    (6, 'PhD'),
    (7, 'Diploma'),
    (8, 'International Year'),
    (9, 'Associate Degree'),
    (10, 'Professional Certificate'),
)

i_am_a_choose = (
    (1, 'Student'),
    (2, 'Parent'),
    (3, 'Mentor'),
    (4, 'University'),
    (5, 'College'),
)
Gender = (('', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say'))

user_type_data = (
    ('', 'select-user'),
    (0, 'Super admin'),
    (1, 'Admin'),
    (2, 'Institute'),
    (3, 'Student'),
    (4, 'Mentor'),
    (5, 'Parent'),
    (6, 'Institute admin'),
    (7, 'App admin'),
    (8, 'Recruiter'),
    (9, 'System Mentor'),
    (10, 'System Recruiter'),
)

WORK_TYPE = (
    ('', '-- Select Work Type --'),
    (1, 'Company'),
    (2, 'Individual'),
    (3, 'School'),
)

AGE = (
    ('', 'Select'),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("19", "19"),
    ("20", "20"),
    ("21", "21"),
    ("22", "22"),
    ("23+", "23+"),
    ("I'm a Parent/Guardian", "I'm a Parent/Guardian"),
)

SUBJECT = (
    ('', 'Select'),
    (1, 'Business Studies'),
    (2, 'Social Studies'),
    (3, 'Arts & Design'),
    (4, 'Law'),
    (5, 'Biomedical Sciences'),
    (6, 'Medicine'),
    (7, 'Dentistry'),
    (8, 'pharmacy'),
    (9, 'Computer Science'),
    (10, 'Finance'),
    (11, 'Architecture'),
    (12, 'Finance & Accounting'),
    (13, 'Nursing'),
    (14, 'Politics'),
    (15, 'Chemical Engineering'),
    (16, 'Electrical Engineering'),
    (17, 'International Relations'),
    (18, 'Mechanical Engineering'),
    (19, 'Economics'),
)

COURSE = (
    (5, 'Medical Foundation Programme'),
    (1, 'University Foundation Programme in Business Management'),
    (2, 'University Foundation Programme in Engineering'),
    (3, 'University Foundation Programme in Social Sciences'),
    (4, 'University Foundation Programme in Computer Science'),
)

COMMENT_STATUS = (
    (True, 'published'),
    (False, 'draft'),
)

REASONE_FOR_AN_APPOINTMENT = (
    ('', 'Select'),
    ("Choosing a University", "Choosing a University"),
    ("University Application", "University Application"),
    ("Study Experience", "Study Experience"),
    ("Tutoring", "Tutoring"),
    ("Exam Preparation", "Exam Preparation"),
    ("Employment Prospects", "Employment Prospects"),
    ("Other", "Other"),
)

A_AM = (
    ('', 'Select'),
    ("the Applicant", "the Applicant"),
    ("a Parent", "a Parent"),
    ("a School", "a School"),
    ("an Agent", "an Agent"),
)

ROLE = (
    ('Institution Staff', 'Institution Staff'),
    ('Ambassador', 'Ambassador'),
    ('Mentor', 'Mentor')
)

ARE_YOU_CHOICES = (
    ('', 'Select'),
    (1, 'Institute'),
    (2, 'University')
)

platform_choice = (
    (0, 'Privately'),
    (1, 'Online Platform'),
)
how_did_you_hear_about_us_choices = (
    ('', 'Select option'),
    ('Facebook', 'Facebook'),
    ('Instagram', 'Instagram'),
    ('LinkedIn', 'LinkedIn'),
    ('Twitter', 'Twitter'),
    ('TikTok', 'TikTok'),
    ('My University', 'My University'),
    ('Google Search', 'Google Search'),
    ('Other', 'Other'),
)

platform_choice = (
    (0, 'Privately'),
    (1, 'Online Platform'),
)

how_did_you_hear_about_us_choices = (
    ('', 'Select option'),
    ('Facebook', 'Facebook'),
    ('Instagram', 'Instagram'),
    ('LinkedIn', 'LinkedIn'),
    ('Twitter', 'Twitter'),
    ('TikTok', 'TikTok'),
    ('My University', 'My University'),
    ('Friends or Family', 'Friends or Family'),
    ('Other', 'Other'),
)

platform_choice = (
    (0, 'Privately'),
    (1, 'Online Platform'),
)

how_did_you_hear_about_us_choices = (
    ('', 'Select option'),
    ('Facebook', 'Facebook'),
    ('Instagram', 'Instagram'),
    ('LinkedIn', 'LinkedIn'),
    ('Twitter', 'Twitter'),
    ('TikTok', 'TikTok'),
    ('My University', 'My University'),
    ('Friends or Family', 'Friends or Family'),
    ('Other', 'Other'),
)

TUTORING_SUBJECT_CHOICES = (
        ("Maths", "Maths"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("English", "English"),
        ("Economics", "Economics"),
        ("ICT", "ICT"),
        ("History", "History"),
        ("Geography", "Geography"),
        ("Personal Statement", "Personal Statement"),
        ("Interviews", "Interviews"),
    )

TUTORING_WITH = (
        ("UCAT", "UCAT"),
        ("BMAT", "BMAT"),
        ("GAMSAT", "GAMSAT"),
        ("HPAT", "HPAT"),
        ("IMAT", "IMAT"),
        ("Personal Statement", "Personal Statement"),
        ("MMI / Interviews", "MMI / Interviews"),

    )

TUTORING_LEVEL = (
        ('Highschool', 'Highschool'),
        ('College / University', 'College / University'),
        ('English Language', 'English Language'),
    )