from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout
from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required
from .models import Feedback
from .forms import FeedbackForm
from django.contrib.admin.views.decorators import staff_member_required

# Public welcome page
def welcome(request):
    return render(request, 'feedback/user/welcome.html')

# Submit feedback (public)
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()

            # Send thank-you email
            subject = "Thank you for your feedback!"
            message = (
                f"Hi {feedback.name},\n\n"
                f"Thank you for sharing your feedback under '{feedback.category}'.\n"
                f"We appreciate your input and will use it to improve our services.\n\n"
                "Best regards,\nCustomer Feedback Team"
            )
            recipient_list = [feedback.email]
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")

            return redirect('thank_you')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/user/submit_feedback.html', {'form': form})

# Thank you page after submission
def thank_you(request):
    return render(request, 'feedback/user/thank_you.html')

# Public: list all feedback (no login required)
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-id')  # latest first
    return render(request, 'feedback/admin/view_feedbacks.html', {'feedbacks': feedbacks})

# Admin: feedback report page (staff only)
@staff_member_required(login_url='/admin/login/')
def feedback_report(request):
    category_counts = Feedback.objects.values('category') \
                                      .annotate(count=Count('id')) \
                                      .order_by('category')

    category_avg_rating = Feedback.objects.values('category') \
                                          .annotate(avg_rating=Avg('rating')) \
                                          .order_by('category')

    categories = [item['category'] for item in category_counts]
    counts = [item['count'] for item in category_counts]
    avg_ratings = [item['avg_rating'] if item['avg_rating'] else 0 for item in category_avg_rating]

    category_labels = {
        'product': 'Product Satisfaction',
        'service': 'Service Quality',
        'experience': 'Overall Experience',
    }
    labels = [category_labels.get(cat, cat) for cat in categories]

    context = {
        'labels': labels,
        'counts': counts,
        'avg_ratings': avg_ratings,
    }
    return render(request, 'feedback/admin/feedback_report.html', context)

# Admin dashboard (staff only)
@staff_member_required(login_url='/admin/login/')
def admin_dashboard(request):
    total_feedback = Feedback.objects.count()
    category_counts = Feedback.objects.values('category').annotate(count=Count('id'))
    recent_feedback = Feedback.objects.order_by('-id')[:5]
    avg_rating = Feedback.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    context = {
        'total_feedback': total_feedback,
        'category_counts': category_counts,
        'recent_feedback': recent_feedback,
        'avg_rating': round(avg_rating, 2),
    }
    return render(request, 'feedback/admin/dashboard.html', context)

# Logout view (public)
def user_logout(request):
    logout(request)
    return redirect('welcome')



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Compose email content
        subject = f"Contact Us Message from {name}"
        full_message = f"Sender: {name} <{email}>\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # send to your own email or support email
                fail_silently=False,
            )
            return render(request, 'feedback/user/contact_us.html', {'success': True})
        except Exception as e:
            print(f"Error sending contact email: {e}")
            return render(request, 'feedback/user/contact_us.html', {'error': True})

    return render(request, 'feedback/user/contact_us.html')
def call_contacts(request):
    return render(request, 'feedback/call_contacts.html')
