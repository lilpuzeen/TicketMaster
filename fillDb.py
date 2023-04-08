from app import db, Ticket
import random
from sqlalchemy import text


def fill_db() -> None:
    ticket_ids = random.sample(range(100000, 999999), 500)

    for ticket_id in ticket_ids:
        ticket = Ticket(ticket_id=str(ticket_id))
        db.session.add(ticket)
        db.session.commit()


def fill_db_from_file() -> None:
    with open("tickets.txt", "r") as f:
        for line in f:
            ticket = Ticket(ticket_id=line.strip())
            db.session.add(ticket)
            db.session.commit()


def check_db_for_duplicates() -> None:
    tickets = Ticket.query.all()
    ticket_ids = [ticket.ticket_id for ticket in tickets]
    if len(ticket_ids) == len(set(ticket_ids)):
        print("No duplicates found")
    else:
        print("Duplicates found")
        

def sell_ticket(ticket_id: str) -> None:
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    ticket.is_sold = True
    db.session.commit()


def ticket_returned(ticket_id: str) -> None:
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    ticket.is_sold = False
    db.session.commit()


def retrieve_non_sold_ticket() -> str:
    ticket = Ticket.query.filter_by(is_sold=False).first()
    ticket.is_sold = True
    db.session.commit()
    return ticket.ticket_id


def add_new_column(col_name: str, col_type: str, default=None) -> None:
    if default:
        db.session.execute(f"ALTER TABLE ticket ADD COLUMN {col_name} {col_type} DEFAULT {default}")
    else:
        db.session.execute(f"ALTER TABLE ticket ADD COLUMN {col_name} {col_type}")
    db.session.commit()
    
    
def retrieve_non_existing_ticket_id() -> int:
    tickets = Ticket.query.all()
    ticket_ids = [ticket.ticket_id for ticket in tickets]
    ticket_ids = [int(ticket_id) for ticket_id in ticket_ids]
    ticket_ids = sorted(ticket_ids)
    for i in range(len(ticket_ids) - 1):
        if ticket_ids[i] + 1 != ticket_ids[i + 1]:
            return ticket_ids[i] + 1
    return ticket_ids[-1] + 1

@DeprecationWarning
def clear_db() -> None:
    tickets = Ticket.query.all()
    for ticket in tickets:
        db.session.delete(ticket)
    db.session.commit()


def set_whole_column_to_value(col_name: str, value: str) -> None:
    db.session.execute(text(f"UPDATE ticket SET {col_name} = {value}"))
    db.session.commit()
    

def reset_db_to_defaults() -> None:
    db.session.execute(text(f"UPDATE ticket SET is_sold = 0"))
    db.session.execute(text(f"UPDATE ticket SET is_used = 0"))
    db.session.commit()

# @DeprecationWarning
def test_case() -> None:
    tickets = Ticket.query.all()
    for i in range(1):
        tickets[i].is_sold = True
    db.session.commit()
    

def save_all_tickets_to_file() -> None:
    tickets = Ticket.query.all()
    with open("tickets.txt", "w") as f:
        for ticket in tickets:
            f.write(f"{ticket.ticket_id}" + "\n")
            

def insert_ticket(ticket_id: str) -> None:
    ticket = Ticket(ticket_id=ticket_id)
    db.session.execute(text(f"INSERT INTO ticket (ticket_id, is_sold, is_used) VALUES ({ticket_id}, {False}, {False})"))
    db.session.commit()


def reset_id() -> None:
    db.session.execute(text(f"ALTER SEQUENCE ticket_id_seq RESTART WITH 1;"))
    db.session.commit()


if __name__ == '__main__':
    # fill_db()
    # check_db_for_duplicates()
    # ticket_returned("1234")
    # print(retrieve_non_sold_ticket())
    # add_new_column("test", "INTEGER", 0)
    # print(retrieve_non_existing_ticket_id())
    # clear_db()
    # set_whole_column_to_value("is_sold", "1")
    # set_whole_column_to_value("is_used", "0")
    # reset_db_to_defaults()
    # test_case()
    # insert_ticket("970277")
    fill_db_from_file()
    # save_all_tickets_to_file()
    # sell_ticket("970277")
    # pass