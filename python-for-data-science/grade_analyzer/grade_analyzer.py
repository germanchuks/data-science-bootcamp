# GradeAnalyzer.py

class GradeAnalyzer:
    def __init__(self, filename):
        """
        Initialize the GradeAnalyzer with the given filename.
        Args:
            filename (str): Path to the student grades data file.
        """
        self._filename = filename
        self._students = []
        self._subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'English']
        self._loaded = False

    @property
    def students(self):
        """
        Getter for the list of students.
        Returns:
            list: List of student dictionaries.
        """
        return self._students.copy()

    def check_data_loaded(self):
        """
        Checks if the student data has been loaded.
        Returns:
            bool: True if data is loaded, False otherwise.
        """
        if not self._loaded:
            print("Data not loaded. Please load the data first.")
            return False
        return True

    def validate_student_id(self, student_id):
        """
        Validates the student ID and returns the student data if found.
        Args:
            student_id (str): The student ID to validate.
        Returns:
            dict or None: Student dictionary if found, None otherwise.
        """
        try:
            if not isinstance(student_id, str):
                print("Student ID must be a string.")
                return None
            student = next(
                (s for s in self._students if s['id'] == student_id), None)
            if not student:
                print(f"Student with ID {student_id} not found.")
                return None
            return student
        except Exception as e:
            print(f"Error validating student ID: {e}")
            return None

    def validate_course_name(self, course_name):
        """
        Validates the course name.
        Args:
            course_name (str): The course name to validate.
        Returns:
            str or None: Course name if valid, None otherwise.
        """
        try:
            if not isinstance(course_name, str):
                print("Course name must be a string.")
                return None
            if course_name not in self._subjects:
                print(f"Course {course_name} is not valid.")
                return None
            return course_name
        except Exception as e:
            print(f"Error validating course name: {e}")
            return None

    def load_data(self):
        """
        Loads the data from the file and populates the students list.
        Returns:
            None
        """
        try:
            with open(self._filename, 'r') as file:
                self._students = []
                self._loaded = False
                next(file)
                for line in file:
                    student = self.parse_student_line(line)
                    if student:
                        self._students.append(student)
                self._loaded = True
                print(f"Data loaded successfully from {self._filename}.")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"Error loading data: {e}")
            self._loaded = False

    def parse_student_line(self, line):
        """
        Parses a line from the file and returns a dictionary with student data.
        Args:
            line (str): Line from the data file.
        Returns:
            dict or None: Student dictionary if valid, None otherwise.
        """
        try:
            parts = line.strip().split(',')
            if len(parts) != 7:
                print(
                    f"Skipping invalid line (expected 7 fields): {line.strip()}")
                return None
            student = {
                'id': parts[0],
                'name': parts[1],
                'grades': {
                    'Math': int(parts[2]),
                    'Physics': int(parts[3]),
                    'Chemistry': int(parts[4]),
                    'Biology': int(parts[5]),
                    'English': int(parts[6]),
                }
            }
            return student
        except Exception as e:
            print(f"Error parsing student line: {e}")
            return None

    def validate_data(self):
        """
        Checks loaded data for integrity.
        Returns:
            bool: True if data is valid, False otherwise.
        """
        try:
            if self.check_data_loaded() is False:
                return False
            print('Validating loaded data...')
            for student in self._students:
                if not isinstance(student, dict):
                    print(f"Invalid data format for student: {student}")
                    return False
                if 'name' not in student or 'id' not in student or 'grades' not in student:
                    print(
                        f"Missing required fields in student data: {student}")
                    return False
                if not isinstance(student['name'], str) or not isinstance(student['id'], str):
                    print(f"Invalid name or ID for student: {student}")
                    return False
                if not isinstance(student['grades'], dict) or len(student['grades']) != len(self._subjects):
                    print(
                        f"Invalid grades for student {student.get('name', 'Unknown')} ({student.get('id', 'Unknown')}).")
                    return False
            print('Data validation successful.')
            return True
        except Exception as e:
            print(f"Error validating data integrity: {e}")
            return False

    def get_student_count(self):
        """
        Returns the number of students loaded.
        Returns:
            int: Number of students.
        """
        try:
            if self.check_data_loaded() is False:
                return 0
            return len(self._students)
        except Exception as e:
            print(f"Error getting student count: {e}")
            return 0

    def calculate_student_average(self, student_id):
        """
        Calculates the overall average grade for a student.
        Args:
            student_id (str): The student ID.
        Returns:
            float or None: Average grade if student found, None otherwise.
        """
        try:
            if self.check_data_loaded() is False:
                return None
            student = self.validate_student_id(student_id)
            if not student:
                return None
            return sum(student['grades'].values()) / len(student['grades'])
        except Exception as e:
            print(f"Error calculating student average: {e}")
            return None

    def get_student_highest_score(self, student_id):
        """
        Gets the highest score for a student.
        Args:
            student_id (str): The student ID.
        Returns:
            tuple or None: (subject, score) if student found, None otherwise.
        """
        try:
            if self.check_data_loaded() is False:
                return None
            student = self.validate_student_id(student_id)
            if not student:
                return None
            return max(student['grades'].items(), key=lambda item: item[1])
        except Exception as e:
            print(f"Error getting highest score for student: {e}")
            return None

    def get_student_lowest_score(self, student_id):
        """
        Gets the lowest score for a student.
        Args:
            student_id (str): The student ID.
        Returns:
            tuple or None: (subject, score) if student found, None otherwise.
        """
        try:
            if self.check_data_loaded() is False:
                return None
            student = self.validate_student_id(student_id)
            if not student:
                return None
            return min(student['grades'].items(), key=lambda item: item[1])
        except Exception as e:
            print(f"Error getting lowest score for student: {e}")
            return None

    def is_student_passing(self, student_id, threshold=60):
        """
        Determines if a student has passed or failed based on average.
        Args:
            student_id (str): The student ID.
            threshold (int, optional): Passing threshold. Defaults to 60.
        Returns:
            bool or None: True if passing, False if not, None if error.
        """
        try:
            if self.check_data_loaded() is False:
                return False
            student = self.validate_student_id(student_id)
            if not student:
                return None
            if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 100:
                print(
                    f"Invalid threshold value: {threshold}. Must be between 0 and 100.")
                return None
            average = self.calculate_student_average(student_id)
            return average is not None and average >= threshold
        except Exception as e:
            print(f"Error determining if student is passing: {e}")
            return None

    def get_student_info(self, student_id):
        """
        Gets formatted student info.
        Args:
            student_id (str): The student ID.
        Returns:
            str or None: Formatted student info, None if not found.
        """
        try:
            if self.check_data_loaded() is False:
                return None
            student = self.validate_student_id(student_id)
            if not student:
                return None
            info = f"Student ID: {student['id']}\nName: {student['name']}\nGrades:\n"
            for subject, grade in student['grades'].items():
                info += f"  {subject}: {grade}\n"
            return info
        except Exception as e:
            print(f"Error getting student info: {e}")
            return None

    def convert_to_letter_grade(self, score):
        """
        Converts a numerical score to a letter grade.
        Args:
            score (int or float): The numerical score.
        Returns:
            str or None: Letter grade, None if invalid score.
        """
        try:
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                print(
                    f"Invalid score value: {score}. Must be a number between 0 and 100.")
                return None
            grades = [(90, 'A'), (80, 'B'), (70, 'C'), (60, 'D'), (50, 'E')]
            for threshold, letter in grades:
                if score >= threshold:
                    return letter
            return 'F'
        except Exception as e:
            print(f"Error converting score to letter grade: {e}")
            return None

    def get_course_scores(self, course_name):
        """
        Lists all scores for one subject.
        Args:
            course_name (str): The course name.
        Returns:
            list: List of scores for the subject.
        """
        try:
            if self.check_data_loaded() is False:
                return []
            course = self.validate_course_name(course_name)
            if not course:
                return []
            return [student['grades'].get(course_name, 0) for student in self._students]
        except Exception as e:
            print(f"Error getting course scores: {e}")
            return []

    def calculate_course_average(self, course_name):
        """
        Finds the average score for a subject.
        Args:
            course_name (str): The course name.
        Returns:
            float: Average score for the subject.
        """
        try:
            if self.check_data_loaded() is False:
                return 0
            if not self.validate_course_name(course_name):
                return 0
            scores = self.get_course_scores(course_name)
            return sum(scores) / len(scores) if scores else 0
        except Exception as e:
            print(f"Error calculating course average: {e}")
            return 0

    def find_course_median(self, course_name):
        """
        Finds the median score for a subject.
        Args:
            course_name (str): The course name.
        Returns:
            float or None: Median score, None if no scores.
        """
        try:
            scores = sorted(self.get_course_scores(course_name))
            n = len(scores)
            if n == 0:
                return None
            mid = n // 2
            return scores[mid] if n % 2 else (scores[mid - 1] + scores[mid]) / 2
        except Exception as e:
            print(f"Error finding course median: {e}")
            return None

    def get_course_grade_distribution(self, course_name):
        """
        Gets the count distribution of letter grades for a subject.
        Args:
            course_name (str): The course name.
        Returns:
            dict: Distribution of letter grades.
        """
        try:
            if self.check_data_loaded() is False:
                return {}
            if not self.validate_course_name(course_name):
                return {}
            distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
            for score in self.get_course_scores(course_name):
                letter_grade = self.convert_to_letter_grade(score)
                distribution[letter_grade] += 1
            return distribution
        except Exception as e:
            print(f"Error getting course grade distribution: {e}")
            return {}

    def rank_courses_by_difficulty(self):
        """
        Ranks courses by difficulty (hardest first, lowest average).
        Returns:
            list: List of (subject, average) tuples sorted by average ascending.
        """
        try:
            if self.check_data_loaded() is False:
                return []
            averages = {}
            for subject in self._subjects:
                averages[subject] = self.calculate_course_average(subject)
            return sorted(averages.items(), key=lambda item: item[1])
        except Exception as e:
            print(f"Error ranking courses by difficulty: {e}")
            return []

    def get_course_statistics(self, course_name):
        """
        Gets comprehensive statistics for a course.
        Args:
            course_name (str): The course name.
        Returns:
            dict or None: Dictionary of statistics, None if error.
        """
        try:
            if self.check_data_loaded() is False:
                return None
            if not self.validate_course_name(course_name):
                return None
            average = self.calculate_course_average(course_name)
            median = self.find_course_median(course_name)
            highest = max(self.get_course_scores(course_name), default=0)
            lowest = min(self.get_course_scores(course_name), default=0)
            distribution = self.get_course_grade_distribution(course_name)

            return {
                'average': average,
                'median': median,
                'highest': highest,
                'lowest': lowest,
                'distribution': distribution
            }
        except Exception as e:
            print(f"Error getting course statistics: {e}")
            return None

    def rank_students_by_average(self):
        """
        Ranks students by average score.
        Returns:
            list: List of (student_id, average) tuples sorted descending.
        """
        try:
            if self.check_data_loaded() is False:
                return []
            averages = [(student['id'], self.calculate_student_average(
                student['id'])) for student in self._students]
            return sorted(averages, key=lambda item: item[1], reverse=True)
        except Exception as e:
            print(f"Error ranking students by average: {e}")
            return []

    def get_top_performers(self, n=5):
        """
        Gets the top N students by average score.
        Args:
            n (int): Number of top students to return.
        Returns:
            list: List of (student_id, average) tuples.
        """
        try:
            if self.check_data_loaded() is False:
                return []
            if not isinstance(n, int) or n <= 0:
                print(f"Invalid value for n: {n}. Must be a positive integer.")
                return []
            return self.rank_students_by_average()[:n]
        except Exception as e:
            print(f"Error getting top performers: {e}")
            return []

    def get_struggling_students(self, threshold=60):
        """
        Gets students below a certain average score.
        Args:
            threshold (int or float): The threshold for struggling students.
        Returns:
            list: List of student dictionaries below the threshold.
        """
        try:
            if self.check_data_loaded() is False:
                return []
            if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 100:
                print(
                    f"Invalid threshold value: {threshold}. Must be between 0 and 100.")
                return []
            return [student for student in self._students if self.calculate_student_average(student['id']) < threshold]
        except Exception as e:
            print(f"Error getting struggling students: {e}")
            return []

    def calculate_class_statistics(self):
        """
        Calculates overall class performance statistics.
        Returns:
            dict or None: Dictionary of class statistics, None if error.
        """
        try:
            if not self.check_data_loaded():
                return None
            subject_stats = {
                subject: self.get_course_statistics(subject)
                for subject in self._subjects
            }
            metrics = {
                'top_performers': self.get_top_performers(n=5),
                'struggling_students (<60)': self.get_struggling_students(threshold=60),
                'subject_statistics': subject_stats,
                'student_count': len(self._students)
            }
            return metrics
        except Exception as e:
            print(f"Error calculating class statistics: {e}")
            return None

    def find_subject_correlations(self):
        """
        Finds and presents subject correlations as plain floats, sorted by strength.
        Returns:
            list: List of tuples (subject1, subject2, correlation) sorted by absolute correlation descending.
        """
        try:
            import numpy as np
            if not self.check_data_loaded():
                return []
            scores = {subject: [student['grades'][subject]
                                for student in self._students] for subject in self._subjects}
            correlations = []
            for i, s1 in enumerate(self._subjects):
                for s2 in self._subjects[i+1:]:
                    corr = float(np.corrcoef(scores[s1], scores[s2])[0, 1])
                    correlations.append((s1, s2, corr))
            # Sort by absolute correlation descending
            correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            # for s1, s2, corr in correlations:
            #     print(f"{s1} & {s2}: {corr:.2f}")
            return correlations
        except Exception as e:
            print(f"Error finding subject correlations: {e}")
            return {}

    def get_grade_distribution_summary(self):
        """
        Gets grade distribution across all subjects.
        Returns:
            dict: Dictionary of subject to grade distribution.
        """
        try:
            if self.check_data_loaded() is False:
                return {}
            distribution = {subject: self.get_course_grade_distribution(
                subject) for subject in self._subjects}
            return distribution
        except Exception as e:
            print(f"Error getting grade distribution summary: {e}")
            return {}

    def generate_student_report(self, student_id):
        """
        Generates a detailed report for a student.
        Args:
            student_id (str): The student ID.
        Returns:
            str or None: Report string, None if error.
        """
        try:
            if not self.check_data_loaded():
                return None
            student_data = self.validate_student_id(student_id)
            if student_data is None:
                return None
            info = self.get_student_info(student_id)
            avg = self.calculate_student_average(student_id)
            high = self.get_student_highest_score(student_id)
            low = self.get_student_lowest_score(student_id)
            status = "Passing" if self.is_student_passing(
                student_id) else "Failing"
            report = (
                f"{info}"
                f"Average Score: {avg:.2f}\n"
                f"Highest Score: {high[0]} ({high[1]})\n"
                f"Lowest Score: {low[0]} ({low[1]})\n"
                f"Passing Status: {status}\n"
                "Letter Grades:\n"
            )
            report += "".join(
                f"  {subject}: {self.convert_to_letter_grade(score)}\n"
                for subject, score in student_data['grades'].items()
            )
            report += "\n"
            return report
        except Exception as e:
            print(f"Error generating student report: {e}")
            return None

    def generate_course_report(self, course_name):
        """
        Generates a report for a course.
        Args:
            course_name (str): The course name.
        Returns:
            str or None: Report string, None if error.
        """
        try:
            if not self.check_data_loaded():
                return None

            if self.validate_course_name(course_name) is None:
                return None

            stats = self.get_course_statistics(course_name)
            if stats is None:
                return None

            report = (
                f"Course: {course_name}\n"
                f"Average Score: {stats['average']:.2f}\n"
                f"Highest Score: {stats['highest']:.2f}\n"
                f"Lowest Score: {stats['lowest']:.2f}\n"
                f"Distribution: {stats['distribution']}\n"
                f"Total Students: {len(self._students)}\n"
            )
            return report
        except Exception as e:
            print(f"Error generating course report: {e}")
            return None

    def generate_class_overview(self):
        """
        Generates a class-wide report.
        Returns:
            str or None: Report string, None if error.
        """
        try:
            if not self.check_data_loaded():
                return None
            overall_stats = self.calculate_class_statistics()
            if overall_stats is None:
                return None
            report = (
                f"Class Overview\n"
                f"Total Students: {overall_stats['student_count']}\n"
                f"Top Performers: {overall_stats['top_performers']}\n"
                f"Struggling Students (<60): {overall_stats['struggling_students (<60)']}\n"
            )
            for subject, stats in overall_stats['subject_statistics'].items():
                report += (
                    f"Subject: {subject}\n"
                    f"  Average: {stats['average']:.2f}\n"
                    f"  Highest: {stats['highest']:.2f}\n"
                    f"  Lowest: {stats['lowest']:.2f}\n"
                    f"  Distribution: {stats['distribution']}\n"
                    f"  Total Students: {len(self._students)}\n"
                )
            return report
        except Exception as e:
            print(f"Error generating class overview: {e}")
            return None

    def save_report_to_file(self, report_content, filename):
        """
        Saves a report to a file.
        Args:
            report_content (str): The report content to save.
            filename (str): The filename to save to.
        Returns:
            None
        """
        try:
            if not report_content:
                print("No report content to save.")
                return
            if not filename.endswith('.txt'):
                print("Filename must end with .txt")
                return
            if not isinstance(report_content, str):
                print("Report content must be a string.")
                return
            with open(filename, 'w') as file:
                file.write(report_content)
            print(f"Report saved to {filename}.")
        except Exception as e:
            print(f"Error saving report to file: {e}")

    def display_summary(self):
        """
        Prints key statistics to the console.
        Returns:
            None
        """
        try:
            if not self.check_data_loaded():
                return
            print(f"Total Students: {self.get_student_count()}")
            class_stats = self.calculate_class_statistics()
            if not class_stats:
                print("No class statistics available.")
                return
            print("Class-Wide Statistics:")
            print(f"  Top Performers: {class_stats['top_performers']}")
            print(
                f"  Struggling Students: {class_stats['struggling_students (<60)']}")
            print("Subject Averages:")
            for subject, stats in class_stats['subject_statistics'].items():
                if stats:
                    print(f"  {subject}: {stats['average']:.2f}")
        except Exception as e:
            print(f"Error displaying summary: {e}")
            return
