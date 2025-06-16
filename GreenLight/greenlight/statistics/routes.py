from flask import render_template
from flask_login import login_required

from . import stats_bp
from ..models import Loan



@stats_bp.route('/stats/', methods=['GET', 'POST'])
@login_required
def stats():
    """
        Renders the loan statistics page.

        Gathers:
        - Total approved and not approved loan counts.
        - Loan approval breakdown by education level.
    """

    loans = Loan.query.all()
    approved = 0
    not_approved = 0
    education = {}

    # Initialize counters
    for loan in loans:
        if loan.prediction_result >= 50:
            approved += 1
        else:
            not_approved += 1

        # -------------------------------------
        # Group stats by education level
        ed = loan.education
        if ed not in education:
            education[ed] = {'approved': 0, 'not_approved': 0}

        if loan.prediction_result >= 50:
            education[ed]['approved'] += 1
        else:
            education[ed]['not_approved'] += 1


    cols = {
        'approved': approved,
        'not_approved': not_approved
    }



    return render_template('statsPage.html', cols=cols, education=education)


