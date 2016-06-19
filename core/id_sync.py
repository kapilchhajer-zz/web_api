from app.models.Ticket import *
from app.models.KYC_Model import TicketPracticeMap
from app import db


def sync(ticket):
    db.session.execute('SET foreign_key_checks = 0;')
    tags = Ticket.get_ticket_tags(ticket.id)
    t = filter(lambda x: x if 'galaxyid' in x.lower() else None, tags)
    if t:
        t = t[0]
        t = t.split('#')[-1]
        if t.isdigit():
            t = int(t)
    else:
        return
    if t == ticket.id:
        return
    tags = TicketTag.query.filter(TicketTag.ticket_id == ticket.id).all()
    comments = TicketComment.query.filter(
        TicketComment.ticket_id == ticket.id).all()
    subs = TicketSubscriber.query.filter(
        TicketSubscriber.ticket_id == ticket.id).all()
    mails = TicketMails.query.filter(TicketMails.ticket_id == ticket.id).all()
    childs = Ticket.query.filter(Ticket.child_of == ticket.id).all()
    ownerships = TicketOwnership.query.filter(
        TicketOwnership.ticket_id == ticket.id).all()
    assignments = TicketAssignment.query.filter(
        TicketAssignment.ticket_id == ticket.id).all()
    ticket_versions_query = 'Update tickets_version set id = {new_id} where id = {old_id}'
    #ticket_ownerships_version_query = 'Update ticket_ownerships_version set ticket_id = {new_id} where ticket_id = {old_id}'
    #ticket_assignments_version_query = 'Update ticket_assignments_version set ticket_id = {new_id} where ticket_id = {old_id}'
    old_id = ticket.id
    ticket.id = t

    for tag in tags:
        tag.ticket_id = t
        db.session.add(tag)
    for comment in comments:
        comment.ticket_id = t
        db.session.add(comment)
    for sub in subs:
        sub.ticket_id = t
        db.session.add(sub)
    for mail in mails:
        mail.ticket_id = t
        db.session.add(mail)
    for child in childs:
        child.child_of = t
        db.session.add(child)
    for ownership in ownerships:
        ownership.ticket_id = t
        db.session.add(ownership)
        for version in ownership.versions.all():
            version.ticket_id = t
            db.session.add(version)
    for assignment in assignments:
        assignment.ticket_id = t
        db.session.add(assignment)
        for version in assignment.versions.all():
            version.ticket_id = t
            db.session.add(version)
    db.session.execute(
        'update ticket_practice_map set ticket_id = {new_id} where ticket_id = {old_id}'.format(
            old_id=old_id,
            new_id=t))
    db.session.execute(ticket_versions_query.format(new_id=t, old_id=old_id))
    db.session.add(ticket)
    db.session.commit()
    #db.session.execute(ticket_versions_query.format(**{'new_id':t, 'old_id': ticket.id}))
    #db.session.execute(ticket_ownerships_version_query.format(**{'new_id':t, 'old_id': ticket.id}))
    #db.session.execute(ticket_assignments_version_query.format(**{'new_id':t, 'old_id': ticket.id}))
    # db.session.commit()
