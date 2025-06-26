from grade_analyzer import GradeAnalyzer


def main():
    # Initialize analyzer with your data file
    analyzer = GradeAnalyzer('student_grades.txt')
    analyzer.load_data()

    # Test: Calculate average for a specific student
    print("Average for STU001:", analyzer.calculate_student_average('STU001'))

    # Test: Get top 5 performers
    print("Top 5 performers:", analyzer.get_top_performers(5))

    # Test: Rank courses by difficulty
    print("Courses ranked by difficulty (hardest first):")
    for subject, avg in analyzer.rank_courses_by_difficulty():
        print(f"  {subject}: {avg:.2f}")

    # Test: Display summary
    print("\nClass Summary:")
    analyzer.display_summary()

    # Test: Save class overview report to file
    overview = analyzer.generate_class_overview()
    if overview:
        analyzer.save_report_to_file(overview, 'class_analysis.txt')

    # Test: Find and display subject correlations
    print("\nSubject Correlations (sorted by strength):")
    correlations = analyzer.find_subject_correlations()
    for s1, s2, corr in correlations:
        print(f"{s1} & {s2}: {corr:.2f}")


if __name__ == "__main__":
    main()
