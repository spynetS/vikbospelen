from django.shortcuts import render
from mail.mail import sendmail
from vikbo import settings



def contact(request):
    try:
        body = (
            f"<p>Namn: {request.POST['name']}</p>\n"
            f"<p>E-post: {request.POST['email']}</p>\n"
            f"<p>Telefonnummer: {request.POST['phone']}</p>\n"
            f"<pre>Meddelande:\n {request.POST['msg']}</pre>"
        )

        # Send mail to inbox/group
        sendmail(
            request.POST["subject"],
            body,
            request.POST['name'],
            request.POST['email'],
            settings.INBOX_EMAIL,
            "Inforeport",
            "html"
        )

        # Send confirmation mail to the user
        confirmation_subject = "Tack för ditt meddelande!"
        confirmation_body = (
            f"Hej {request.POST['name']},<br><br>"
            "Tack för att du kontaktade oss. Vi har mottagit ditt meddelande och "
            "kommer att återkomma så snart som möjligt.<br><br>"
            "Med vänliga hälsningar,<br>"
            "Vikbolandsspelen"
        )
        sendmail(
            confirmation_subject,
            confirmation_body,
            settings.EMAIL_HOST_USER,  # From your email
            settings.EMAIL_HOST_USER,
            request.POST['email'],     # To user email
            None,
            "html"
        )

        return render(request, "components/Alert.html", {"type": "success", "msg": "Meddelandet skickat!"})

    except Exception as e:
        return render(request, "components/Alert.html", {"type": "error", "msg": "Något gick fel! " + str(e)})
