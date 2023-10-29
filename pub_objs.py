from db_conn import DBconn

#create object for paths
class paths:
    def __init__(self):
        cur = DBconn()
        cur.cursor.execute('SELECT username, password, login_link, username_input, next_button_path, password_input, login_path, post_path, author_path, id_path, date_path, text_path, post_link_path, retweeted_path, retweetedname_path, retweetedid_path, video_path, twofactor_input, twofactor_btn  FROM your_table_for_paths')
        result = cur.cursor.fetchall()
        cur.cursor.close()
        cur.connection.close()
        for item in result:
            self.username=item[0]
            self.password=item[1]
            self.login_link=item[2]
            self.username_input=item[3]
            self.next_button_path=item[4]
            self.password_input=item[5]
            self.login_path=item[6]
            self.post_path=item[7]
            self.author_path=item[8]
            self.id_path=item[9]
            self.date_path=item[10]
            self.text_path=item[11]
            self.post_link_path=item[12]
            self.retweeted_path=item[13]
            self.retweetedname_path=item[14]
            self.retweetedid_path=item[15]
            self.video_path=item[16]
            self.twofactor_input=item[17]
            self.twofactor_btn=item[18]



