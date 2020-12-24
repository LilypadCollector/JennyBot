from firebase_admin import firestore


def get_note():
    db = firestore.client()
    collection_ref = db.collection('lovenotes')
    current_cycle = db.collection('information').document('lovenotes').get().to_dict()['currentCycle']

    # Notes that have NEVER been used have -1 cycle
    # If none of these exist, then we move onto our used notes.
    unused_query = collection_ref.where('cycle', '==', -1)

    for note_doc in unused_query.stream():
        note_text = note_doc.to_dict()['text']
        note_author = note_doc.to_dict()['author']
        note_doc_ref = collection_ref.document(note_doc.id)
        note_doc_ref.update({
            'cycle': current_cycle
        })

        return note_text, note_author

    # Since no unused notes were found, we move onto our used notes.
    used_query = collection_ref.where('cycle', '<', current_cycle)
    recycle_flag = True  # Initializing. If we ran out of notes, the for loop won't run and this will remain True.

    for note_doc in used_query.stream():
        recycle_flag = False
        note_text = note_doc.to_dict()['text']
        note_author = note_doc.to_dict()['author']
        note_doc_ref = collection_ref.document(note_doc.id)
        note_doc_ref.update({
            'cycle': current_cycle
        })
        return note_text, note_author

    if recycle_flag:
        db.collection('information').document('lovenotes').update({
            'currentCycle': current_cycle + 1
        })
        return "Wowee! We're out of new love notes. Time to recycle!", None


def write_note(msg, author):
    db = firestore.client()
    collection_ref = db.collection('lovenotes')
    doc_ref = collection_ref.add({
        'author': author,
        'text': msg,
        'createdAt': firestore.SERVER_TIMESTAMP,
        'cycle': 0,
    })

    return doc_ref[1].id


def delete_note(doc_id):
    doc_ref = firestore.client().collection('lovenotes').document(doc_id)
    doc_dict = doc_ref.get().to_dict()
    doc_ref.delete()
    return doc_dict


def clear():
    docs = firestore.client().collection('lovenotes').stream()
    deleted_col_ref = firestore.client().collection('deletedLovenotes')
    count = 0
    for doc in docs:
        contents = doc.to_dict()  # Get contents of soon-to-be deleted doc
        deleted_col_ref.document(doc.id).set(contents)  # Move contents to deletedLovenotes collection
        doc.reference.delete()  # Delete from active lovenotes collection (note: copy still exists in deletedLovenotes)
        count += 1

    doc_ref = firestore.client().collection('information').document('lovenotes')
    doc_ref.update({
        'currentCycle': 0,
    })

    return count

def reset_cycle():
    count = 0
    db = firestore.client()
    doc_ref = db.collection('information').document('lovenotes')
    doc_ref.update({
        'currentCycle': 0,
    })

    lovenotes_col_ref = db.collection('lovenotes')
    for doc in lovenotes_col_ref.stream():
        doc.reference.update({
            'cycle': -1,
        })

        count += 1

    return count
