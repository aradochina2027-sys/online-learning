from learning.repositories.course_repository import CourseRepository


class CourseService:
    @staticmethod
    def get_courses():
        return CourseRepository.get_all()

    @staticmethod
    def get_course(course_id):
        return CourseRepository.get_by_id(course_id)

    @staticmethod
    def create_course(title, description, teacher):
        if not title.strip():
            raise ValueError("Назва курсу не може бути порожньою")

        return CourseRepository.create(
            title=title,
            description=description,
            teacher=teacher,
        )
