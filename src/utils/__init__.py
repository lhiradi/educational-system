def days_overlap(days1, days2):
    set1 = set(day.strip().upper() for day in days1.split(","))
    set2 = set(day.strip().upper() for day in days2.split(","))
    return not set1.isdisjoint(set2)

def get_total_enrolled_units(student):
    """Returns the sum of units for all courses the student is enrolled in."""
    return sum(link.course.course_unit for link in student.course_links)