from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, Submission


def submit(request, course_id):
    if request.method == "POST":
        Submission.objects.all().delete()

        for question in Question.objects.all():
            choice_id = request.POST.get(f"question_{question.id}")

            if choice_id:
                choice = get_object_or_404(
                    Choice,
                    id=choice_id,
                    question=question
                )

                Submission.objects.create(
                    question=question,
                    choice=choice
                )

        return redirect(
            "show_exam_result",
            course_id=course_id,
            submission_id=1
        )

    return redirect("course_details", course_id=course_id)


def show_exam_result(request, course_id, submission_id):
    submissions = Submission.objects.select_related(
        "question",
        "choice"
    ).all()

    total_questions = Question.objects.count()
    answered_questions = submissions.count()

    context = {
        "submissions": submissions,
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "correct_answers": answered_questions,
        "score": (
            (answered_questions / total_questions) * 100
            if total_questions > 0 else 0
        ),
    }

    return render(request, "exam_result.html", context)
