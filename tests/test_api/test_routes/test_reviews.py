from datetime import datetime

import pytest

from app.models.review import ReviewIn


@pytest.fixture
def review() -> ReviewIn:
    return ReviewIn(id='1',
                    visit_id='1',
                    hospital_id='1',
                    doctor_id='1',
                    client_id='1',
                    liked='liked',
                    did_not_liked='did_not_liked',
                    comment='comment',
                    review_time=datetime.now(),
                    confirmed=True,
    )
