from email.mime.text import MIMEText

from app.tool.Mailer import smtp


def send_mail(to, board_id, title):
    if board_id == 1:
        msg = MIMEText('새로운 컴퓨터구조 게시물이 올라왔습니다.'
                       '제목 : ' + title)
    elif board_id == 2:
        msg = MIMEText('새로운 컴퓨터네트워크 공지가 올라왔습니다.'
                       '제목 : ' + title)
    else:
        msg = MIMEText('새로운 게시물이 올라왔습니다.')

    msg['Subject'] = 'NCLab 게시물 알리미'
    msg['To'] = to
    smtp.sendmail('Yeongdu Land', to, msg.as_string())
