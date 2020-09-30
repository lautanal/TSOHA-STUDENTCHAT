from db import db
import users, admins

# Viestin sisällön haku
def read_message(message_id):
    sql = "SELECT content FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Viestin kirjoittajan id:n haku
def get_user_id(message_id):
    sql = "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Viestin ketjun id:n haku
def get_topic_id(message_id):
    sql = "SELECT topic_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Ketjun viestien haku
def get_messages(topic_id):
    sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.topic_id=:topic_id AND M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

# Viestien haku tietojen perusteella
def find_messages(user_alias, content):
    user_alias = "%" + user_alias + "%"
    content = "%" + content + "%"
    if (user_alias == ""):
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.user_id=U.id AND M.content LIKE :content ORDER BY M.id"
        result = db.session.execute(sql, {"content":content})
    elif(content == ""):
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.user_id=U.id AND U.alias LIKE :user_alias ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias})
    else:
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.user_id=U.id AND U.alias LIKE :user_alias AND M.content LIKE :content  ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias, "content":content})
    return result.fetchall()

# Uuden viestin talletus tietokantaan
def insert(topic_id, content, ref_msg):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "INSERT INTO messages (content, topic_id, user_id, sent_at, visible, ref_message) VALUES (:content, :topic_id, :user_id, NOW(), true, :ref_msg)"
    db.session.execute(sql, {"content":content, "topic_id":topic_id, "user_id":login_id, "ref_msg":ref_msg})
    db.session.commit()
    return True

# Viestin poistaminen (näkyviltä)
def delete(message_id):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
#    sql = "DELETE FROM messages WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

# Muutetun viestin talletus tietokantaan
def update(message_id, content):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "UPDATE messages SET CONTENT = :content WHERE id = :message_id"
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()
    return True

# Viestin poistaminen (administraattori)
def admin_delete(message_id):
    admin_id = admins.admin_id()
    if admin_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

