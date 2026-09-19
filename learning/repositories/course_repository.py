from learning.models import Course


class CourseRepository:
    @staticmethod
    def get_all():
        return Course.objects.all()

    @staticmethod
    def get_by_id(course_id):
        return Course.objects.filter(id=course_id).first()

    @staticmethod
    def create(title, description, teacher):
        return Course.objects.create(
            title=title,
            description=description,
            teacher=teacher,
        )
