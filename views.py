from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Question, Choice, Submission


def submit(request):
    if request.method == "POST":
        for question in Question.objects.all():
            choice_id = request.POST.get(f"question_{question.id}")

            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                Submission.objects.create(
                    question=question,
                    choice=choice
                )

        return redirect("show_exam_result")

    return redirect("course_details")


def show_exam_result(request):
    submissions = Submission.objects.all()

    total_questions = Question.objects.count()
    correct_answers = 0

    for submission in submissions:
        if submission.choice.question_id == submission.question_id:
            correct_answers += 1

    context = {
        "submissions": submissions,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
    }

    return render(request, "exam_result.html", context)
