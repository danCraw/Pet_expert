from app.db.tables import visits, doctors, hospitals, Client
from app.db.tables.clients import clients


def get_review_list_query():
    query = (self.table.select()
    .join(visits, self.table.c.visit_id == visits.c.id, isouter=True)
    .join(doctors, self.table.c.doctor_id == doctors.c.id, isouter=True)
    .join(hospitals, self.table.c.hospital_id == hospitals.c.id, isouter=True)
    .with_only_columns(
        clients.c.name.label('client_name'),
        clients.c.surname.label('client_surname'),
        hospitals.c.name.label('hospital_name'),
        doctors.c.name.label('doctor_name'),
        visits.c.date_of_receipt,
        self.table.c.id,
        self.table.c.liked,
        self.table.c.did_not_liked,
        self.table.c.comment,
        self.table.c.review_time,
        self.table.c.confirmed))